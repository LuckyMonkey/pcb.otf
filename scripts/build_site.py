#!/usr/bin/env python3
"""Assemble the compact deployable PCB.OTF specimen artifact."""

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


def main() -> int:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    shutil.copy2(ROOT / "demo.html", SITE / "index.html")
    # Keep the source filename available too: registry links work both from a
    # checkout and from the generated Pages artifact.
    shutil.copy2(ROOT / "demo.html", SITE / "demo.html")
    for filename in ("README.md", "CHANGELOG.md", "LICENSE"):
        shutil.copy2(ROOT / filename, SITE / filename)
    shutil.copytree(ROOT / "docs", SITE / "docs", dirs_exist_ok=True)
    shutil.copytree(ROOT / "glyphs/color", SITE / "glyphs/color", dirs_exist_ok=True)
    shutil.copytree(ROOT / "glyphs/iso", SITE / "glyphs/iso", dirs_exist_ok=True)
    shutil.copytree(ROOT / "glyphs/technical", SITE / "glyphs/technical", dirs_exist_ok=True)
    dist = SITE / "dist"
    dist.mkdir()
    for filename in ("PCB.woff2", "PCB-Color.woff2", "pcb.css"):
        shutil.copy2(ROOT / "dist" / filename, dist / filename)
    print("wrote _site")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
