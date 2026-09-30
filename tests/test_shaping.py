import unittest
from pathlib import Path

import uharfbuzz as hb


ROOT = Path(__file__).resolve().parents[1]


def shape(font_path: Path, text: str):
    blob = hb.Blob.from_file_path(str(font_path))
    face = hb.Face(blob)
    font = hb.Font(face)
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(font, buffer)
    return [info.codepoint for info in buffer.glyph_infos], face


class ShapingTest(unittest.TestCase):
    def test_semantic_tokens_shape_without_touching_prose(self):
        path = ROOT / "dist/PCB.ttf"
        glyphs, _ = shape(path, "Install :usb_c: beside :ddr4_dimm:.")
        self.assertIn("hardware_usb_c", _glyph_names(path, glyphs))
        self.assertIn("hardware_ddr4_dimm", _glyph_names(path, glyphs))
        plain, _ = shape(path, "usb_c ddr4_dimm")
        self.assertNotIn("hardware_usb_c", _glyph_names(path, plain))
        self.assertNotIn("hardware_ddr4_dimm", _glyph_names(path, plain))

    def test_woff2_shaping_preserves_surrounding_text(self):
        glyphs, _ = shape(ROOT / "dist/PCB.woff2", "A :pcie_x16_slot: Z")
        names = _glyph_names(ROOT / "dist/PCB.woff2", glyphs)
        self.assertIn("hardware_pcie_x16_slot", names)
        self.assertGreater(len(names), 3)


def _glyph_names(font_path: Path, glyph_indices):
    from fontTools.ttLib import TTFont

    with TTFont(font_path) as font:
        order = font.getGlyphOrder()
        return [order[index] for index in glyph_indices if index < len(order)]


if __name__ == "__main__":
    unittest.main()
