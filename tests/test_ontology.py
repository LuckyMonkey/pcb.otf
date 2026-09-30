import csv
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class OntologyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())
        cls.objects = cls.data["objects"]
        cls.by_id = {item["id"]: item for item in cls.objects}

    def test_mvp_inventory_and_unique_identity(self):
        self.assertGreaterEqual(len(self.objects), 100)
        self.assertEqual(len(self.objects), len(self.by_id))
        for required in ("hardware:resistor", "hardware:usb_c", "hardware:ddr3_dimm", "hardware:m2_socket", "hardware:pcie_x16_slot"):
            self.assertIn(required, self.by_id)

    def test_graph_targets_resolve(self):
        group_ids = {group["id"] for group in self.data["groups"]}
        for item in self.objects:
            self.assertIn(item["parent"], group_ids, item["id"])
            for field in ("interfaces", "compatible_with", "incompatible_with"):
                for target in item.get(field, []):
                    self.assertIn(target, self.by_id, f"{item['id']} -> {field} -> {target}")

    def test_pua_registry_is_one_to_one(self):
        codepoints = [item["unicode_pua"] for item in self.objects]
        shortcodes = [item["shortcode"] for item in self.objects]
        self.assertEqual(len(codepoints), len(set(codepoints)))
        self.assertEqual(len(shortcodes), len(set(shortcodes)))
        with (ROOT / "registry/codepoints.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), len(self.objects))
        self.assertEqual({row["id"] for row in rows}, set(self.by_id))

    def test_every_object_has_three_vector_views(self):
        for item in self.objects:
            stem = item["id"].split(":", 1)[1]
            for directory in ("mono", "color", "iso"):
                path = ROOT / "glyphs" / directory / f"{stem}.svg"
                self.assertTrue(path.is_file(), path)
                self.assertIn("viewBox=\"0 0 1000 1000\"", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
