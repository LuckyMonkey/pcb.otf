import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class AssemblyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.objects = {item["id"]: item for item in yaml.safe_load((ROOT / "ontology/hardware.yaml").read_text())["objects"]}
        cls.scene = yaml.safe_load((ROOT / "assemblies/generic_atx_desktop.yaml").read_text())

    def test_atx_scene_has_required_hardware(self):
        object_ids = {layer["object"] for layer in self.scene["layers"]}
        required = {
            "hardware:atx_motherboard", "hardware:cpu_socket", "hardware:cpu", "hardware:vrm",
            "hardware:ddr4_dimm_slot", "hardware:ddr4_dimm", "hardware:pcie_x16_slot", "hardware:gpu",
            "hardware:m2_socket", "hardware:nvme_ssd", "hardware:sata_connector", "hardware:sata_ssd",
            "hardware:atx_24pin", "hardware:cpu_power_8pin", "hardware:pcie_power_8pin",
        }
        self.assertTrue(required.issubset(object_ids))
        self.assertEqual(len(self.scene["layers"]), 31)

    def test_layers_are_resolvable_and_have_technical_views(self):
        instances = set()
        for layer in self.scene["layers"]:
            self.assertNotIn(layer["instance"], instances)
            instances.add(layer["instance"])
            record = self.objects[layer["object"]]
            base = record["glyph"]["base"]
            for view in ("top", "front", "side", "isometric"):
                self.assertTrue((ROOT / "glyphs/technical" / view / f"{base}.svg").is_file())


if __name__ == "__main__":
    unittest.main()
