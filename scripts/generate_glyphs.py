#!/usr/bin/env python3
"""Generate deterministic top-down, monochrome, color, and isometric SVG masters."""

from __future__ import annotations

import html
from pathlib import Path

import yaml

from hardware_designs import PALETTE
from patent_art import draw
from patent_pen import INK
from technical_art import TECHNICAL_BASES, technical_for


ROOT = Path(__file__).resolve().parents[1]
MONO_INK = PALETTE["ink"]
MONO_PAPER = PALETTE["paper"]

# The technical masters intentionally use a different rendering language from
# the emoji/color glyphs.  They are original vectors, but borrow the visual
# grammar of patent plates and service-manual drawings: thin ink outlines,
# restrained section fills, and visible internal construction.
TECHNICAL_STYLE = {
    # Technical masters are black-on-white drafting plates.  Interiors stay
    # transparent so the assembly can be layered and read as an x-ray; white
    # knockouts are reserved for actual cavities and keyed openings.
    "body": ("none", "1", "#17252c", "5"),
    "detail": ("none", "1", "#17252c", "3"),
    "knockout": ("#ffffff", "0.78", "#17252c", "3"),
    "hatch": ("none", "1", "#17252c", "2"),
}


def source() -> dict:
    return yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())


def mono_parts(parts: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    return [(data, MONO_INK if role == "body" else MONO_PAPER, role) for data, _fill, role in parts]


def svg_text(label: str, parts: list[tuple[str, str, str]], mode: str, view: str, source: str = "pcb-original-art") -> str:
    iso = view == "isometric"
    selected = mono_parts(parts) if mode == "mono" else parts
    # A broad, readable projection: the former shallow matrix made every ISO
    # plate look like a dark sliver once object-fit contain was applied.
    transform = ' transform="matrix(.46 .34 -.46 .34 500 160)"' if iso else ""
    technical = source == "pcb-original-technical-art"
    if technical:
        elements = []
        for data, _fill, role in selected:
            fill, opacity, stroke, width = TECHNICAL_STYLE.get(role, TECHNICAL_STYLE["detail"])
            elements.append(
                f'  <path d="{html.escape(data, quote=True)}" fill="{fill}" fill-opacity="{opacity}" '
                f'stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round" '
                f'vector-effect="non-scaling-stroke" data-role="{role}" data-layer="{role}"/>'
            )
    else:
        elements = [f'  <path d="{html.escape(data, quote=True)}" fill="{fill}" data-role="{role}" data-layer="{role}"/>' for data, fill, role in selected]
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-labelledby="title" data-view="{view}" data-source="{source}">',
        f'  <title id="title">{html.escape(label)}</title>',
        f'  <g fill-rule="evenodd" clip-rule="evenodd" shape-rendering="geometricPrecision"{transform}>',
        *elements,
        "  </g>",
        "</svg>",
        "",
    ])


def patent_svg(label: str, pen, mode: str, view: str, source: str = "pcb-patent-art") -> str:
    """The glyph art: patent-style line drawing, every mark a filled outline (see scripts/patent_pen.py).

    mono  = ink only (the font's outline glyph)
    color = tinted fills under the same ink (the color font's layers)
    """
    transform = ' transform="matrix(.46 .34 -.46 .34 500 160)"' if view == "isometric" else ""
    paths = []
    if mode == "color":
        paths += [f'  <path d="{d}" fill="{tint}" data-role="fill" data-layer="fill"/>' for d, tint in pen.fills]
    paths += [f'  <path d="{d}" fill="{INK}" data-role="body" data-layer="ink"/>' for d in pen.ink]
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-labelledby="title" data-view="{view}" data-source="{source}">',
        f'  <title id="title">{html.escape(label)}</title>',
        f'  <g shape-rendering="geometricPrecision"{transform}>',
        *paths,
        "  </g>",
        "</svg>",
        "",
    ])


def main() -> int:
    data = source()
    for item in data["objects"]:
        base = item["glyph"]["base"]
        name = item["id"].split(":", 1)[1]
        pen = draw(base)
        if pen is None:
            raise SystemExit(f"no patent drawing for {base} (scripts/patent_art.py)")
        # the font masters: one original patent drawing per object
        (ROOT / "glyphs/mono" / f"{name}.svg").write_text(patent_svg(item["label"], pen, "mono", "top"), encoding="utf-8")
        (ROOT / "glyphs/color" / f"{name}.svg").write_text(patent_svg(item["label"], pen, "color", "top"), encoding="utf-8")
        (ROOT / "glyphs/iso" / f"{name}.svg").write_text(patent_svg(item["label"], pen, "color", "isometric"), encoding="utf-8")
        for view in ("top", "front", "side", "isometric"):
            technical_path = ROOT / "glyphs/technical" / view / f"{name}.svg"
            technical_path.parent.mkdir(parents=True, exist_ok=True)
            if base in TECHNICAL_BASES:
                # the assembly plates keep their four constructed views (scripts/technical_art.py)
                technical_path.write_text(svg_text(item["label"], technical_for(base, view), "color", view, "pcb-original-technical-art"), encoding="utf-8")
            else:
                technical_path.write_text(patent_svg(item["label"], pen, "mono", view, "pcb-original-technical-art"), encoding="utf-8")
    print(f"generated {len(data['objects'])} monochrome, color, and isometric SVG masters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
