#!/usr/bin/env python3
"""Validate the canonical hardware object model and append-only PUA registry."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^hardware:[a-z0-9_]+$")
TOKEN_RE = re.compile(r"^:[a-z0-9_]+:$")
PUA_RE = re.compile(r"^E[0-9A-F]{3,5}$")


def fail(message: str) -> None:
    raise SystemExit(f"ontology validation failed: {message}")


def main() -> int:
    data = yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())
    project = yaml.safe_load((ROOT / "project.yaml").read_text())
    if data.get("namespace") != "hardware" or str(data.get("version")) != str(project.get("version")):
        fail("namespace/version does not match project.yaml")
    groups = data.get("groups", [])
    group_ids = {group.get("id") for group in groups}
    if not group_ids or "hardware:computer_hardware" not in group_ids:
        fail("hardware:computer_hardware root group is required")
    for group in groups:
        if not ID_RE.fullmatch(str(group.get("id"))):
            fail(f"bad group ID: {group.get('id')}")
        if group.get("parent") is not None and group["parent"] not in group_ids:
            fail(f"unknown group parent: {group['parent']}")
    objects = data.get("objects", [])
    object_ids = {item.get("id") for item in objects}
    if len(object_ids) != len(objects):
        fail("duplicate object ID")
    ids = group_ids | object_ids
    codepoints: dict[str, str] = {}
    shortcodes: set[str] = set()
    source_data = yaml.safe_load((ROOT / "ontology/sources.yaml").read_text())
    source_ids = set(source_data.get("sources", {}))
    for item in objects:
        identifier = item.get("id")
        if not ID_RE.fullmatch(str(identifier)):
            fail(f"bad object ID: {identifier}")
        for key in ("label", "category", "system", "parent", "aliases", "attributes", "interfaces", "compatible_with", "incompatible_with", "unicode_pua", "ligature", "shortcode", "glyph", "provenance", "review_required"):
            if key not in item:
                fail(f"{identifier} missing {key}")
        if item["parent"] not in ids:
            fail(f"unknown parent {item['parent']} for {identifier}")
        for field in ("interfaces", "compatible_with", "incompatible_with"):
            if not isinstance(item[field], list):
                fail(f"{identifier} {field} must be a list")
            for target in item[field]:
                if target not in object_ids:
                    fail(f"{identifier} {field} points to missing object {target}")
        for source in item["provenance"]:
            if source not in source_ids:
                fail(f"{identifier} points to missing provenance source {source}")
        pua = str(item["unicode_pua"]).upper()
        if not PUA_RE.fullmatch(pua) or pua in codepoints:
            fail(f"bad or duplicate PUA codepoint {pua}")
        codepoints[pua] = identifier
        if not TOKEN_RE.fullmatch(item["shortcode"]) or item["shortcode"] != item["ligature"] or item["shortcode"] in shortcodes:
            fail(f"bad or duplicate shortcode for {identifier}")
        shortcodes.add(item["shortcode"])
        if not item["glyph"].get("base") or not item["glyph"].get("monochrome") or not item["glyph"].get("color"):
            fail(f"incomplete glyph mapping for {identifier}")
        if not isinstance(item["review_required"], bool):
            fail(f"review_required must be boolean for {identifier}")

    registry = ROOT / "registry/codepoints.csv"
    if registry.exists():
        with registry.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        old_by_id = {row["id"]: row["codepoint"].upper().removeprefix("U+") for row in rows}
        old_by_cp = {row["codepoint"].upper().removeprefix("U+"): row["id"] for row in rows}
        current = {item["id"]: str(item["unicode_pua"]).upper() for item in objects}
        for identifier, pua in old_by_id.items():
            if identifier not in current or current[identifier] != pua:
                fail(f"released mapping moved or disappeared: {identifier}")
        for pua, identifier in old_by_cp.items():
            if pua in codepoints and codepoints[pua] != identifier:
                fail(f"released codepoint reused: {pua}")
    print(f"ontology OK: {len(objects)} hardware objects, {len(groups)} groups, {len(shortcodes)} shortcodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
