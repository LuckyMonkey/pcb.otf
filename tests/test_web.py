import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WebTest(unittest.TestCase):
    def test_registry_search_and_views_are_present(self):
        page = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        app = (ROOT / "docs/app.js").read_text(encoding="utf-8")
        self.assertIn("Search hardware", page)
        self.assertIn('data-pcb-asset-prefix="../"', page)
        self.assertIn("Object.entries(item.attributes", app)
        self.assertIn("item.external_ids", app)
        self.assertIn("iso_svg", app)
        self.assertIn("Copy character", app)
        demo = (ROOT / "demo.html").read_text(encoding="utf-8")
        self.assertIn("assembly-opacity", demo)
        self.assertIn("assembly-explode", demo)
        self.assertIn("docs/assembly.js", demo)

    def test_site_artifact_is_self_contained(self):
        for path in (
            "_site/index.html",
            "_site/demo.html",
            "_site/docs/index.html",
            "_site/docs/assembly.js",
            "_site/dist/PCB.woff2",
            "_site/dist/PCB-Color.woff2",
            "_site/glyphs/iso/usb_c.svg",
            "_site/glyphs/technical/top/atx_motherboard.svg",
            "_site/glyphs/technical/isometric/atx_motherboard.svg",
        ):
            self.assertTrue((ROOT / path).is_file(), path)
        self.assertFalse((ROOT / "_site/dist/png").exists())


if __name__ == "__main__":
    unittest.main()
