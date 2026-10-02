window.PCB_ASSEMBLIES = [
  {
    "id": "assembly:generic_atx_desktop",
    "label": "Generic ATX desktop assembly",
    "description": "A vendor-neutral ATX board composed from canonical PCB.OTF objects.",
    "viewBox": [
      1280,
      900
    ],
    "default_view": "isometric",
    "default_opacity": 0.86,
    "layers": [
      {
        "instance": "motherboard",
        "object": "hardware:atx_motherboard",
        "view": "top",
        "x": 40,
        "y": 40,
        "width": 1120,
        "height": 820,
        "z": 0,
        "opacity": 0.58,
        "group": "board",
        "explode": [
          0,
          0
        ]
      },
      {
        "instance": "mounting_hole_1",
        "object": "hardware:mounting_hole",
        "view": "top",
        "x": 90,
        "y": 90,
        "width": 90,
        "height": 90,
        "z": 1,
        "opacity": 0.9,
        "group": "board",
        "explode": [
          -12,
          -10
        ]
      },
      {
        "instance": "mounting_hole_2",
        "object": "hardware:mounting_hole",
        "view": "top",
        "x": 1020,
        "y": 90,
        "width": 90,
        "height": 90,
        "z": 1,
        "opacity": 0.9,
        "group": "board",
        "explode": [
          12,
          -10
        ]
      },
      {
        "instance": "mounting_hole_3",
        "object": "hardware:mounting_hole",
        "view": "top",
        "x": 90,
        "y": 720,
        "width": 90,
        "height": 90,
        "z": 1,
        "opacity": 0.9,
        "group": "board",
        "explode": [
          -12,
          10
        ]
      },
      {
        "instance": "mounting_hole_4",
        "object": "hardware:mounting_hole",
        "view": "top",
        "x": 1020,
        "y": 720,
        "width": 90,
        "height": 90,
        "z": 1,
        "opacity": 0.9,
        "group": "board",
        "explode": [
          12,
          10
        ]
      },
      {
        "instance": "cpu_socket",
        "object": "hardware:cpu_socket",
        "view": "top",
        "x": 350,
        "y": 205,
        "width": 280,
        "height": 260,
        "z": 6,
        "opacity": 0.94,
        "group": "compute",
        "explode": [
          0,
          -18
        ]
      },
      {
        "instance": "cpu",
        "object": "hardware:cpu",
        "view": "top",
        "x": 375,
        "y": 230,
        "width": 230,
        "height": 210,
        "z": 8,
        "opacity": 0.96,
        "group": "compute",
        "explode": [
          0,
          -34
        ]
      },
      {
        "instance": "vrm",
        "object": "hardware:vrm",
        "view": "top",
        "x": 205,
        "y": 185,
        "width": 145,
        "height": 310,
        "z": 5,
        "opacity": 0.92,
        "group": "power",
        "explode": [
          -24,
          -12
        ]
      },
      {
        "instance": "heatsink",
        "object": "hardware:heatsink",
        "view": "top",
        "x": 675,
        "y": 175,
        "width": 190,
        "height": 165,
        "z": 5,
        "opacity": 0.84,
        "group": "cooling",
        "explode": [
          26,
          -14
        ]
      },
      {
        "instance": "fan",
        "object": "hardware:fan",
        "view": "top",
        "x": 705,
        "y": 200,
        "width": 130,
        "height": 130,
        "z": 7,
        "opacity": 0.8,
        "group": "cooling",
        "explode": [
          38,
          -26
        ]
      },
      {
        "instance": "chipset",
        "object": "hardware:chipset",
        "view": "top",
        "x": 520,
        "y": 600,
        "width": 150,
        "height": 150,
        "z": 5,
        "opacity": 0.9,
        "group": "compute",
        "explode": [
          0,
          18
        ]
      },
      {
        "instance": "dimm_slot_1",
        "object": "hardware:ddr4_dimm_slot",
        "view": "top",
        "x": 720,
        "y": 390,
        "width": 310,
        "height": 48,
        "z": 4,
        "opacity": 0.78,
        "group": "memory",
        "explode": [
          20,
          0
        ]
      },
      {
        "instance": "dimm_slot_2",
        "object": "hardware:ddr4_dimm_slot",
        "view": "top",
        "x": 720,
        "y": 455,
        "width": 310,
        "height": 48,
        "z": 4,
        "opacity": 0.78,
        "group": "memory",
        "explode": [
          20,
          0
        ]
      },
      {
        "instance": "dimm_slot_3",
        "object": "hardware:ddr4_dimm_slot",
        "view": "top",
        "x": 720,
        "y": 520,
        "width": 310,
        "height": 48,
        "z": 4,
        "opacity": 0.78,
        "group": "memory",
        "explode": [
          20,
          0
        ]
      },
      {
        "instance": "dimm_slot_4",
        "object": "hardware:ddr4_dimm_slot",
        "view": "top",
        "x": 720,
        "y": 585,
        "width": 310,
        "height": 48,
        "z": 4,
        "opacity": 0.78,
        "group": "memory",
        "explode": [
          20,
          0
        ]
      },
      {
        "instance": "dimm_a",
        "object": "hardware:ddr4_dimm",
        "view": "top",
        "x": 730,
        "y": 394,
        "width": 290,
        "height": 40,
        "z": 7,
        "opacity": 0.92,
        "group": "memory",
        "explode": [
          42,
          -12
        ]
      },
      {
        "instance": "dimm_b",
        "object": "hardware:ddr4_dimm",
        "view": "top",
        "x": 730,
        "y": 524,
        "width": 290,
        "height": 40,
        "z": 7,
        "opacity": 0.92,
        "group": "memory",
        "explode": [
          42,
          12
        ]
      },
      {
        "instance": "pcie_x16_slot",
        "object": "hardware:pcie_x16_slot",
        "view": "top",
        "x": 195,
        "y": 650,
        "width": 520,
        "height": 62,
        "z": 4,
        "opacity": 0.82,
        "group": "expansion",
        "explode": [
          0,
          24
        ]
      },
      {
        "instance": "pcie_x1_slot",
        "object": "hardware:pcie_x1_slot",
        "view": "top",
        "x": 220,
        "y": 745,
        "width": 270,
        "height": 45,
        "z": 4,
        "opacity": 0.82,
        "group": "expansion",
        "explode": [
          0,
          28
        ]
      },
      {
        "instance": "gpu",
        "object": "hardware:gpu",
        "view": "top",
        "x": 255,
        "y": 660,
        "width": 480,
        "height": 96,
        "z": 8,
        "opacity": 0.92,
        "group": "expansion",
        "explode": [
          0,
          52
        ]
      },
      {
        "instance": "m2_socket",
        "object": "hardware:m2_socket",
        "view": "top",
        "x": 330,
        "y": 535,
        "width": 245,
        "height": 46,
        "z": 4,
        "opacity": 0.82,
        "group": "storage",
        "explode": [
          -18,
          34
        ]
      },
      {
        "instance": "nvme",
        "object": "hardware:nvme_ssd",
        "view": "top",
        "x": 350,
        "y": 540,
        "width": 220,
        "height": 38,
        "z": 8,
        "opacity": 0.92,
        "group": "storage",
        "explode": [
          -28,
          54
        ]
      },
      {
        "instance": "sata_connector",
        "object": "hardware:sata_connector",
        "view": "top",
        "x": 900,
        "y": 690,
        "width": 105,
        "height": 80,
        "z": 5,
        "opacity": 0.88,
        "group": "storage",
        "explode": [
          28,
          28
        ]
      },
      {
        "instance": "sata_drive",
        "object": "hardware:sata_ssd",
        "view": "top",
        "x": 1030,
        "y": 665,
        "width": 145,
        "height": 95,
        "z": 7,
        "opacity": 0.92,
        "group": "storage",
        "explode": [
          54,
          34
        ]
      },
      {
        "instance": "atx_power",
        "object": "hardware:atx_24pin",
        "view": "top",
        "x": 930,
        "y": 245,
        "width": 115,
        "height": 235,
        "z": 6,
        "opacity": 0.9,
        "group": "power",
        "explode": [
          32,
          -14
        ]
      },
      {
        "instance": "cpu_power",
        "object": "hardware:cpu_power_8pin",
        "view": "top",
        "x": 185,
        "y": 115,
        "width": 105,
        "height": 90,
        "z": 6,
        "opacity": 0.9,
        "group": "power",
        "explode": [
          -24,
          -22
        ]
      },
      {
        "instance": "pcie_power",
        "object": "hardware:pcie_power_8pin",
        "view": "top",
        "x": 620,
        "y": 760,
        "width": 105,
        "height": 90,
        "z": 6,
        "opacity": 0.9,
        "group": "power",
        "explode": [
          18,
          40
        ]
      },
      {
        "instance": "coin_cell",
        "object": "hardware:coin_cell_battery",
        "view": "top",
        "x": 760,
        "y": 690,
        "width": 82,
        "height": 82,
        "z": 6,
        "opacity": 0.9,
        "group": "power",
        "explode": [
          22,
          42
        ]
      },
      {
        "instance": "usb_a",
        "object": "hardware:usb_a",
        "view": "top",
        "x": 1070,
        "y": 300,
        "width": 70,
        "height": 105,
        "z": 6,
        "opacity": 0.88,
        "group": "io",
        "explode": [
          50,
          -10
        ]
      },
      {
        "instance": "rj45",
        "object": "hardware:rj45",
        "view": "top",
        "x": 1070,
        "y": 430,
        "width": 70,
        "height": 105,
        "z": 6,
        "opacity": 0.88,
        "group": "io",
        "explode": [
          50,
          0
        ]
      },
      {
        "instance": "audio",
        "object": "hardware:audio_jack_35mm",
        "view": "top",
        "x": 1070,
        "y": 560,
        "width": 70,
        "height": 105,
        "z": 6,
        "opacity": 0.88,
        "group": "io",
        "explode": [
          50,
          10
        ]
      }
    ],
    "connections": [
      {
        "id": "cpu_power_route",
        "from": "cpu_power",
        "to": "cpu_socket",
        "label": "CPU_PWR",
        "kind": "power"
      },
      {
        "id": "atx_power_route",
        "from": "atx_power",
        "to": "motherboard",
        "label": "ATX_PWR",
        "kind": "power"
      },
      {
        "id": "pcie_power_route",
        "from": "pcie_power",
        "to": "gpu",
        "label": "PCIe_PWR",
        "kind": "power"
      },
      {
        "id": "memory_route_a",
        "from": "dimm_a",
        "to": "dimm_slot_1",
        "label": "DDR4_A",
        "kind": "signal"
      },
      {
        "id": "memory_route_b",
        "from": "dimm_b",
        "to": "dimm_slot_3",
        "label": "DDR4_B",
        "kind": "signal"
      },
      {
        "id": "nvme_route",
        "from": "nvme",
        "to": "m2_socket",
        "label": "NVMe",
        "kind": "signal"
      },
      {
        "id": "sata_route",
        "from": "sata_drive",
        "to": "sata_connector",
        "label": "SATA",
        "kind": "signal"
      },
      {
        "id": "fan_route",
        "from": "fan",
        "to": "cpu_socket",
        "label": "FAN_PWM",
        "kind": "cooling"
      }
    ]
  }
];
