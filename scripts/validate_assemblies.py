#!/usr/bin/env python3
"""Validate scene references and deterministic assembly transforms."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TECHNICAL_VIEWS = {"top", "front", "side", "isometric"}


def main() -> int:
    ontology = yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())
    objects = {item["id"]: item for item in ontology["objects"]}
    checked = 0
    for path in sorted((ROOT / "assemblies").glob("*.yaml")):
        scene = yaml.safe_load(path.read_text())
        if not scene.get("id", "").startswith("assembly:"):
            raise SystemExit(f"invalid assembly ID: {path}")
        layers = scene.get("layers", [])
        instances = set()
        for layer in layers:
            instance = layer.get("instance")
            object_id = layer.get("object")
            if not instance or instance in instances:
                raise SystemExit(f"duplicate/missing instance in {path}: {instance}")
            instances.add(instance)
            if object_id not in objects:
                raise SystemExit(f"dangling object reference in {path}: {object_id}")
            if layer.get("view") not in TECHNICAL_VIEWS:
                raise SystemExit(f"invalid view in {path}: {layer.get('view')}")
            if not 0 <= float(layer.get("opacity", 1)) <= 1:
                raise SystemExit(f"invalid opacity in {path}: {instance}")
            if int(layer.get("z", 0)) < 0:
                raise SystemExit(f"negative z-order in {path}: {instance}")
            base = objects[object_id]["glyph"]["base"]
            view = layer["view"]
            svg = ROOT / "glyphs/technical" / view / f"{base}.svg"
            if not svg.is_file():
                raise SystemExit(f"missing technical scene asset: {svg}")
            checked += 1
    print(f"assemblies OK: {checked} layers, zero dangling object references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
