import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class RelationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.objects = {item["id"] for item in yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())["objects"]}
        cls.data = yaml.safe_load((ROOT / "ontology/relations.yaml").read_text())

    def test_no_dangling_edges(self):
        edges = self.data["edges"]
        self.assertEqual(len(edges), 34)
        for edge in edges:
            self.assertIn(edge["from"], self.objects)
            self.assertIn(edge["to"], self.objects)

    def test_hardware_facts_are_explicit(self):
        edges = {(edge["from"], edge["relation"], edge["to"]) for edge in self.data["edges"]}
        self.assertIn(("hardware:ddr3_dimm", "FITS_IN", "hardware:ddr3_dimm_slot"), edges)
        self.assertIn(("hardware:ddr3_dimm", "INCOMPATIBLE_WITH", "hardware:ddr4_dimm_slot"), edges)
        self.assertIn(("hardware:usb_c", "CARRIES_PROTOCOL", "hardware:usb_protocol"), edges)
        self.assertIn(("hardware:nvme_ssd", "USES_INTERFACE", "hardware:m2_socket"), edges)


if __name__ == "__main__":
    unittest.main()
