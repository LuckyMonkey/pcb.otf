import json
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
class JavaScriptPackageTest(unittest.TestCase):
    def test_lookup_search_and_graph_api(self):
        script = """
const pcb = require('./packages/js');
const usb = pcb.get('hardware:usb_c');
if (!usb || usb.shortcode !== ':usb_c:') process.exit(1);
if (pcb.resolveShortcode(':ddr4_dimm:').id !== 'hardware:ddr4_dimm') process.exit(2);
if (!pcb.search('memory_generation').some((item) => item.id === 'hardware:ddr4_dimm')) process.exit(3);
if (!pcb.connectionsFor('hardware:nvme_ssd').some((edge) => edge.to === 'hardware:m2_socket')) process.exit(4);
console.log(JSON.stringify({objects: pcb.registry.length, usb: usb.char, parents: pcb.parents('hardware:ddr4_dimm')}));
"""
        result = subprocess.run(["node", "-e", script], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["objects"], 101)
        self.assertEqual(payload["parents"], ["hardware:memory"])


if __name__ == "__main__":
    unittest.main()
