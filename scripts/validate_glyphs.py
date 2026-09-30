#!/usr/bin/env python3
"""Validate deterministic PCB.OTF SVG masters and semantic layer roles."""

from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]
PATH_RE = re.compile(r'<path\b[^>]*\bd="[^"]+"[^>]*/>')


def main() -> int:
    data = yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())
    count = 0
    for item in data["objects"]:
        name = item["id"].split(":", 1)[1]
        for directory in ("glyphs/mono", "glyphs/color", "glyphs/iso"):
            path = ROOT / directory / f"{name}.svg"
            if not path.is_file():
                raise SystemExit(f"missing SVG master: {path}")
            text = path.read_text(encoding="utf-8")
            if 'viewBox="0 0 1000 1000"' not in text or not PATH_RE.search(text):
                raise SystemExit(f"malformed SVG master: {path}")
            if directory != "glyphs/iso" and 'data-role="body"' not in text:
                raise SystemExit(f"SVG has no body role: {path}")
            count += 1
        if item["glyph"]["base"] in {
            "atx_motherboard", "mounting_hole", "cpu_socket", "cpu", "vrm", "heatsink", "fan", "chipset",
            "ddr4_dimm_slot", "ddr4_dimm", "pcie_x16_slot", "gpu", "pcie_x1_slot", "m2_socket", "nvme_ssd",
            "sata_connector", "sata_ssd", "atx_24pin", "cpu_power_8pin", "pcie_power_8pin", "coin_cell_battery",
            "usb_a", "rj45", "audio_jack_35mm",
        }:
            for view in ("top", "front", "side", "isometric"):
                path = ROOT / "glyphs/technical" / view / f"{name}.svg"
                if not path.is_file() or 'data-source="pcb-original-technical-art"' not in path.read_text(encoding="utf-8"):
                    raise SystemExit(f"missing technical SVG master: {path}")
                count += 1
    print(f"SVG masters OK: {count} vector files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
