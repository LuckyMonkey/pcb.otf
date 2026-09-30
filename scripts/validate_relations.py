#!/usr/bin/env python3
"""Fail on unknown relation types, duplicate edges, or ghost hardware nodes."""

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ontology = yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())
    relations = yaml.safe_load((ROOT / "ontology/relations.yaml").read_text())
    objects = {item["id"] for item in ontology["objects"]}
    definitions = {item["id"] for item in relations["relations"]}
    edges = set()
    for edge in relations.get("edges", []):
        key = (edge.get("from"), edge.get("relation"), edge.get("to"))
        if key in edges:
            raise SystemExit(f"relation validation failed: duplicate edge {key}")
        edges.add(key)
        if edge.get("from") not in objects or edge.get("to") not in objects:
            raise SystemExit(f"relation validation failed: ghost node in {key}")
        if edge.get("relation") not in definitions:
            raise SystemExit(f"relation validation failed: unknown relation {edge.get('relation')}")
    print(f"relations OK: {len(edges)} typed edges, {len(definitions)} relation types, zero dangling nodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
