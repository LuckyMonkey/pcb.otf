#!/usr/bin/env python3
"""Generate browser-safe assembly manifests from YAML scenes."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    scenes = []
    for path in sorted((ROOT / "assemblies").glob("*.yaml")):
        scenes.append(yaml.safe_load(path.read_text(encoding="utf-8")))
    (ROOT / "docs/assemblies.js").write_text(
        "window.PCB_ASSEMBLIES = " + json.dumps(scenes, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"generated {len(scenes)} assembly scene manifests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
