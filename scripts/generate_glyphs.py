#!/usr/bin/env python3
"""Generate deterministic top-down, monochrome, color, and isometric SVG masters."""

from __future__ import annotations

import html
from pathlib import Path

import yaml

from hardware_designs import PALETTE, design_for


ROOT = Path(__file__).resolve().parents[1]
MONO_INK = PALETTE["ink"]
MONO_PAPER = PALETTE["paper"]


def source() -> dict:
    return yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())


def mono_parts(parts: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    return [(data, MONO_INK if role == "body" else MONO_PAPER, role) for data, _fill, role in parts]


def svg_text(label: str, parts: list[tuple[str, str, str]], mode: str) -> str:
    iso = mode == "iso"
    selected = mono_parts(parts) if mode == "mono" else parts
    transform = ' transform="matrix(.56 .20 -.56 .20 500 300)"' if iso else ""
    elements = [f'  <path d="{html.escape(data, quote=True)}" fill="{fill}" data-role="{role}"/>' for data, fill, role in selected]
    return "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-labelledby="title" data-source="pcb-original-art">',
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
        parts = design_for(base)
        for mode, key, directory in (("mono", "monochrome", "glyphs/mono"), ("color", "color", "glyphs/color"), ("iso", "isometric", "glyphs/iso")):
            path = ROOT / directory / f"{item['id'].split(':', 1)[1]}.svg"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(svg_text(item["label"], parts, mode), encoding="utf-8")
    print(f"generated {len(data['objects'])} monochrome, color, and isometric SVG masters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
