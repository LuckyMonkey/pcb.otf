import unittest
from pathlib import Path

import yaml
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]


class FontTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())["objects"]

    def test_outline_fonts_have_expected_cmap_and_no_letter_hijack(self):
        expected = {int(item["unicode_pua"], 16): "hardware_" + item["id"].split(":", 1)[1] for item in self.items}
        for name in ("PCB.ttf", "PCB.otf", "PCB.woff2"):
            with TTFont(ROOT / "dist" / name) as font:
                cmap = font.getBestCmap()
                for codepoint, glyph_name in expected.items():
                    self.assertEqual(cmap.get(codepoint), glyph_name, (name, codepoint))
                self.assertNotEqual(cmap.get(ord("A")), "hardware_resistor")
                self.assertIn("GSUB", font)

    def test_otf_is_real_cff_and_color_is_colrv1(self):
        for name in ("PCB.otf", "PCB-Color.otf"):
            with TTFont(ROOT / "dist" / name) as font:
                self.assertIn("CFF ", font, name)
                self.assertNotIn("glyf", font, name)
        for name in ("PCB-Color.ttf", "PCB-Color.woff2"):
            with TTFont(ROOT / "dist" / name) as font:
                self.assertEqual(font["COLR"].version, 1, name)
                self.assertIn("CPAL", font, name)


if __name__ == "__main__":
    unittest.main()
