#!/usr/bin/env python3
"""Generate deterministic top-down, monochrome, color, and isometric SVG masters."""

from __future__ import annotations

import html
from pathlib import Path

import yaml

from hardware_designs import PALETTE, design_for
from technical_art import TECHNICAL_BASES, technical_for


ROOT = Path(__file__).resolve().parents[1]
MONO_INK = PALETTE["ink"]
MONO_PAPER = PALETTE["paper"]

# The technical masters intentionally use a different rendering language from
# the emoji/color glyphs.  They are original vectors, but borrow the visual
# grammar of patent plates and service-manual drawings: thin ink outlines,
# restrained section fills, and visible internal construction.
TECHNICAL_STYLE = {
    "body": ("#edf0ea", "0.10", "#21343b", "12"),
    "detail": ("#bd7446", "0.18", "#46565b", "8"),
    "knockout": ("#f7f2e8", "0.90", "#21343b", "10"),
}


def source() -> dict:
    return yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())


def mono_parts(parts: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    return [(data, MONO_INK if role == "body" else MONO_PAPER, role) for data, _fill, role in parts]


def svg_text(label: str, parts: list[tuple[str, str, str]], mode: str, view: str, source: str = "pcb-original-art") -> str:
    iso = view == "isometric"
    selected = mono_parts(parts) if mode == "mono" else parts
    transform = ' transform="matrix(.56 .20 -.56 .20 500 300)"' if iso else ""
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
        f'  <g fill-rule="evenodd" clip-rule="evenodd"{transform}>',
        *elements,
        "  </g>",
        "</svg>",
        "",
    ])


def main() -> int:
    data = source()
    for item in data["objects"]:
        base = item["glyph"]["base"]
        name = item["id"].split(":", 1)[1]
        if base in TECHNICAL_BASES:
            for view in ("top", "front", "side", "isometric"):
                parts = technical_for(base, view)
                mode = "color"
                technical_path = ROOT / "glyphs/technical" / view / f"{name}.svg"
                technical_path.parent.mkdir(parents=True, exist_ok=True)
                technical_path.write_text(svg_text(item["label"], parts, mode, view, "pcb-original-technical-art"), encoding="utf-8")
            # Keep the font masters as compact filled artwork. The technical
            # linework is a separate renderer used by the catalog and assembly
            # plates, so the downloadable font remains a useful color/mono font.
            (ROOT / "glyphs/color" / f"{name}.svg").write_text(svg_text(item["label"], technical_for(base, "top"), "color", "top"), encoding="utf-8")
            (ROOT / "glyphs/mono" / f"{name}.svg").write_text(svg_text(item["label"], technical_for(base, "top"), "mono", "top"), encoding="utf-8")
            (ROOT / "glyphs/iso" / f"{name}.svg").write_text(svg_text(item["label"], technical_for(base, "isometric"), "color", "isometric"), encoding="utf-8")
            continue
        parts = design_for(base)
        # Every registry object gets a technical plate asset. For objects that
        # do not yet have a bespoke construction drawing, the original vector
        # master is rendered through the same drafting treatment. This keeps
        # the catalog complete without pretending that a generic resistor or
        # protocol glyph has a fabricated mechanical side profile.
        for view in ("top", "front", "side", "isometric"):
            technical_path = ROOT / "glyphs/technical" / view / f"{name}.svg"
            technical_path.parent.mkdir(parents=True, exist_ok=True)
            technical_path.write_text(svg_text(item["label"], parts, "color", view, "pcb-original-technical-art"), encoding="utf-8")
        for mode, view, directory in (("mono", "top", "glyphs/mono"), ("color", "top", "glyphs/color"), ("color", "isometric", "glyphs/iso")):
            path = ROOT / directory / f"{name}.svg"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(svg_text(item["label"], parts, mode, view), encoding="utf-8")
    print(f"generated {len(data['objects'])} monochrome, color, and isometric SVG masters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
