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
    print(f"SVG masters OK: {count} vector files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
