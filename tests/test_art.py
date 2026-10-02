"""The glyph art: one original patent-style drawing per object (no shared generic shapes)."""

import hashlib
import re
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from patent_art import ART  # noqa: E402


class ArtTest(unittest.TestCase):
    def setUp(self):
        self.items = yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())["objects"]

    def test_every_object_has_its_own_drawing(self):
        self.assertEqual({i["glyph"]["base"] for i in self.items} - set(ART), set())
        seen = {}
        for item in self.items:
            name = item["id"].split(":", 1)[1]
            text = (ROOT / "glyphs/mono" / f"{name}.svg").read_text()
            body = "".join(re.findall(r' d="([^"]+)"', text))
            digest = hashlib.sha256(body.encode()).hexdigest()
            self.assertNotIn(digest, seen, f"{name} draws exactly like {seen.get(digest)}")
            seen[digest] = name

    def test_mono_glyphs_are_line_art_in_one_ink(self):
        for item in self.items:
            name = item["id"].split(":", 1)[1]
            text = (ROOT / "glyphs/mono" / f"{name}.svg").read_text()
            self.assertIn('data-source="pcb-patent-art"', text)
            self.assertEqual(set(re.findall(r'fill="(#[0-9a-f]{6})"', text)), {"#17252c"}, name)
            self.assertGreaterEqual(text.count("<path"), 4, f"{name} is too plain to be a full-detail drawing")


if __name__ == "__main__":
    unittest.main()
