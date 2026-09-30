"""Original, compact engineering-drawing vectors for PCB.OTF."""

from __future__ import annotations


PALETTE = {
    "pcb": "#1f554d",
    "copper": "#b86f3f",
    "metal": "#c8cbc4",
    "ceramic": "#d8d0bd",
    "silicon": "#293642",
    "blue": "#5b83a0",
    "amber": "#d3a44c",
    "red": "#b85d4e",
    "paper": "#f5f0e6",
    "ink": "#17252c",
}


def part(path: str, fill: str, role: str = "body") -> tuple[str, str, str]:
    return path, fill, role


def rr(x: int, y: int, w: int, h: int, r: int, fill: str, role: str = "body") -> tuple[str, str, str]:
    return part(f"M{x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} H{x+r} Q{x} {y+h} {x} {y+h-r} V{y+r} Q{x} {y} {x+r} {y} Z", fill, role)


def circle(cx: int, cy: int, r: int, fill: str, role: str = "body") -> tuple[str, str, str]:
    return part(f"M{cx-r} {cy} A{r} {r} 0 1 0 {cx+r} {cy} A{r} {r} 0 1 0 {cx-r} {cy} Z", fill, role)


def line(x1: int, y1: int, x2: int, y2: int, width: int, fill: str, role: str = "detail") -> tuple[str, str, str]:
    return part(f"M{x1} {y1} H{x2} V{y2} H{x1} Z", fill, role) if y1 == y2 else part(f"M{x1} {y1} L{x2} {y1} L{x2} {y2} L{x1} {y2} Z", fill, role)


def resistor(fill: str = PALETTE["ceramic"]) -> list[tuple[str, str, str]]:
    return [
        line(100, 500, 270, 520, 20, PALETTE["metal"]),
        rr(270, 390, 460, 220, 70, fill),
        part("M330 400 L375 600 M430 400 L475 600 M530 400 L575 600 M630 400 L675 600", PALETTE["copper"], "detail"),
        line(730, 500, 900, 520, 20, PALETTE["metal"]),
    ]


def chip(pins: int = 6, body: str = PALETTE["silicon"], accent: str = PALETTE["copper"]) -> list[tuple[str, str, str]]:
    result = [rr(250, 250, 500, 500, 40, body)]
    for x in (285, 390, 495, 600, 705):
        result.append(rr(x, 155, 24, 95, 8, PALETTE["metal"], "detail"))
        result.append(rr(x, 750, 24, 95, 8, PALETTE["metal"], "detail"))
    for y in (285, 390, 495, 600, 705):
        result.append(rr(155, y, 95, 24, 8, PALETTE["metal"], "detail"))
        result.append(rr(750, y, 95, 24, 8, PALETTE["metal"], "detail"))
    result.append(circle(350, 350, 36, accent, "detail"))
    result.append(rr(410, 430, 180, 80, 16, PALETTE["blue"], "detail"))
    return result


def package(kind: str) -> list[tuple[str, str, str]]:
    if kind == "dip":
        result = [rr(255, 245, 490, 510, 34, PALETTE["ceramic"])]
        for y in (300, 400, 500, 600, 700):
            result += [rr(165, y, 90, 28, 8, PALETTE["metal"], "detail"), rr(745, y, 90, 28, 8, PALETTE["metal"], "detail")]
        return result + [part("M440 245 Q500 320 560 245", PALETTE["ink"], "detail")]
    if kind in {"qfp", "qfn"}:
        result = [rr(260, 260, 480, 480, 38, PALETTE["silicon"])]
        for p in (300, 390, 480, 570, 660):
            result += [rr(p, 150, 22, 110, 5, PALETTE["metal"], "detail"), rr(p, 740, 22, 110, 5, PALETTE["metal"], "detail"), rr(150, p, 110, 22, 5, PALETTE["metal"], "detail"), rr(740, p, 110, 22, 5, PALETTE["metal"], "detail")]
        if kind == "qfn": result.append(rr(425, 425, 150, 150, 18, PALETTE["copper"], "detail"))
        return result
    if kind == "bga":
        result = [rr(230, 230, 540, 540, 32, PALETTE["silicon"])]
        for x in (315, 405, 495, 585, 675):
            for y in (315, 405, 495, 585, 675):
                result.append(circle(x, y, 20, PALETTE["amber"], "detail"))
        return result
    if kind == "lga":
        result = [rr(230, 230, 540, 540, 32, PALETTE["silicon"])]
        for x in (300, 390, 480, 570, 660):
            for y in (300, 390, 480, 570, 660):
                result.append(rr(x, y, 34, 16, 4, PALETTE["metal"], "detail"))
        return result
    return chip()


def board(kind: str = "board") -> list[tuple[str, str, str]]:
    result = [rr(120, 150, 760, 700, 42, PALETTE["pcb"])]
    for x, y in ((190, 220), (810, 220), (190, 780), (810, 780)):
        result += [circle(x, y, 45, PALETTE["metal"], "detail"), circle(x, y, 20, PALETTE["ink"], "knockout")]
    if kind == "motherboard":
        result += [rr(355, 280, 290, 220, 18, PALETTE["silicon"]), rr(340, 560, 320, 50, 8, PALETTE["metal"], "detail")]
        result += [rr(185, 290, 110, 24, 4, PALETTE["metal"], "detail"), rr(185, 345, 110, 24, 4, PALETTE["metal"], "detail"), rr(680, 315, 150, 34, 4, PALETTE["metal"], "detail")]
    elif kind == "pcb":
        result += [part("M210 320 H790 V350 H210 Z M210 470 H600 V500 H210 Z M420 500 V700 H450 V500 Z M600 350 V700 H630 V350 Z", PALETTE["copper"], "detail")]
    else:
        result += [part("M180 330 H820 V355 H180 Z M180 500 H700 V525 H180 Z M330 525 V730 H355 V525 Z", PALETTE["copper"], "detail")]
    return result


def memory(generation: str) -> list[tuple[str, str, str]]:
    accent = {"ddr3": PALETTE["blue"], "ddr4": PALETTE["amber"], "ddr5": PALETTE["red"]}[generation]
    notch = {"ddr3": 455, "ddr4": 500, "ddr5": 545}[generation]
    result = [rr(145, 315, 710, 370, 20, PALETTE["pcb"]), part(f"M{notch} 685 H{notch+55} V745 H{notch} Z", PALETTE["paper"], "knockout")]
    for x in (230, 330, 430, 530, 630, 730):
        result.append(rr(x, 365, 70, 180, 10, accent))
    for x in range(170, 840, 28): result.append(rr(x, 690, 12, 44, 2, PALETTE["gold"] if "gold" in PALETTE else PALETTE["amber"], "detail"))
    return result


def slot(kind: str) -> list[tuple[str, str, str]]:
    width = {"pcie_x1_slot": 360, "pcie_x16_slot": 680, "ddr3_dimm_slot": 600, "ddr4_dimm_slot": 630, "ddr5_dimm_slot": 660, "isa_slot": 680, "pci_slot": 600, "agp_slot": 520}.get(kind, 560)
    x = 500 - width // 2
    result = [rr(x, 390, width, 180, 25, PALETTE["silicon"])]
    for p in range(x + 30, x + width - 10, 28): result.append(rr(p, 585, 12, 55, 2, PALETTE["copper"], "detail"))
    notch = x + width // 2
    result.append(part(f"M{notch-30} 390 H{notch+30} V470 H{notch-30} Z", PALETTE["paper"], "knockout"))
    return result


def connector(kind: str) -> list[tuple[str, str, str]]:
    sizes = {"usb_a": (390, 300, 220, 400), "usb_c": (370, 330, 260, 340), "hdmi": (300, 360, 400, 280), "displayport": (310, 340, 380, 320), "rj45": (300, 300, 400, 390), "audio_jack_35mm": (390, 240, 220, 520), "sata_connector": (260, 360, 480, 260), "ide_connector": (230, 340, 540, 310), "scsi_connector": (220, 320, 560, 350), "vga": (240, 300, 520, 380), "ps2": (330, 300, 340, 380), "atx_24pin": (270, 250, 460, 500), "cpu_power_8pin": (330, 260, 340, 470), "pcie_power_8pin": (330, 260, 340, 470)}
    x, y, w, h = sizes.get(kind, (260, 300, 480, 380))
    result = [rr(x, y, w, h, 36, PALETTE["metal"])]
    if kind == "usb_c": result.append(rr(x + 35, y + 100, w - 70, h - 200, 90, PALETTE["ink"], "knockout"))
    elif kind == "audio_jack_35mm": result += [circle(500, 500, 120, PALETTE["ink"], "knockout"), circle(500, 500, 58, PALETTE["metal"], "detail")]
    elif kind in {"rj45", "vga", "ps2"}:
        for row in range(2 if kind != "vga" else 3):
            for col in range(4 if kind != "vga" else 5): result.append(circle(x + 80 + col * 78, y + 105 + row * 90, 17, PALETTE["amber"], "detail"))
    else:
        for row in range(2):
            for col in range(4 if "power" in kind else 6): result.append(circle(x + 70 + col * ((w - 140) // 5), y + 115 + row * ((h - 230) if h > 300 else 80), 18, PALETTE["ink"], "knockout"))
    return result


def disk(kind: str) -> list[tuple[str, str, str]]:
    if kind == "hdd": return [rr(170, 220, 660, 560, 38, PALETTE["metal"]), circle(500, 500, 205, PALETTE["silicon"]), circle(500, 500, 66, PALETTE["metal"], "detail"), line(500, 500, 710, 365, 22, PALETTE["copper"], "detail")]
    if kind in {"nvme_ssd", "sata_ssd", "sd_card"}: return board(kind)[:1] + [rr(200, 300, 600, 400, 18, PALETTE["pcb"]), rr(285, 390, 150, 150, 12, PALETTE["silicon"], "detail"), rr(505, 390, 150, 150, 12, PALETTE["silicon"], "detail"), part("M200 600 H800 V630 H200 Z", PALETTE["copper"], "detail")]
    return connector(kind)


def design_for(name: str) -> list[tuple[str, str, str]]:
    if name == "resistor": return resistor()
    if name == "variable_resistor": return resistor(PALETTE["blue"]) + [part("M430 250 L650 390 L620 420 L400 280 Z", PALETTE["red"], "detail")]
    if name == "potentiometer": return [circle(500, 500, 260, PALETTE["ceramic"]), circle(500, 500, 80, PALETTE["copper"], "detail"), line(500, 150, 500, 300, 28, PALETTE["metal"]), line(250, 700, 750, 700, 28, PALETTE["metal"])]
    if name == "ceramic_capacitor": return [line(270, 500, 430, 500, 22, PALETTE["metal"]), line(570, 500, 730, 500, 22, PALETTE["metal"]), rr(415, 250, 45, 500, 12, PALETTE["ceramic"]), rr(540, 250, 45, 500, 12, PALETTE["ceramic"])]
    if name == "electrolytic_capacitor": return [rr(280, 230, 440, 540, 130, PALETTE["ceramic"]), line(500, 270, 500, 430, 26, PALETTE["red"], "detail"), line(420, 350, 580, 350, 26, PALETTE["red"], "detail"), line(500, 770, 500, 880, 22, PALETTE["metal"])]
    if name == "inductor": return [line(110, 500, 220, 500, 22, PALETTE["metal"]), part("M220 500 Q260 300 300 500 Q340 700 380 500 Q420 300 460 500 Q500 700 540 500 Q580 300 620 500 Q660 700 700 500", PALETTE["copper"], "body"), line(700, 500, 890, 500, 22, PALETTE["metal"])]
    if name == "transformer": return [rr(220, 260, 190, 480, 40, PALETTE["ceramic"]), rr(590, 260, 190, 480, 40, PALETTE["ceramic"]), line(475, 200, 475, 800, 35, PALETTE["metal"]), line(525, 200, 525, 800, 35, PALETTE["metal"])]
    if name in {"fuse", "thermistor"}: return resistor(PALETTE["ceramic"] if name == "fuse" else PALETTE["blue"])
    if name in {"diode", "led", "photodiode"}: return [line(120, 500, 360, 500, 22, PALETTE["metal"]), part("M360 350 L650 500 L360 650 Z", PALETTE["red"] if name == "led" else PALETTE["ceramic"]), line(650, 340, 650, 660, 34, PALETTE["ink"]), line(650, 500, 880, 500, 22, PALETTE["metal"])] + ([part("M330 250 L410 330 L370 360 Z M700 250 L620 330 L660 360 Z", PALETTE["amber"], "detail")] if name == "photodiode" else [])
    if name in {"npn_transistor", "pnp_transistor", "mosfet"}: return [circle(500, 500, 230, PALETTE["silicon"]), line(210, 500, 350, 500, 30, PALETTE["metal"]), line(500, 270, 500, 380, 30, PALETTE["metal"]), line(500, 620, 500, 730, 30, PALETTE["metal"]), part("M430 390 L600 500 L430 610 Z", PALETTE["copper"], "detail")]
    if name in {"voltage_regulator", "op_amp", "oscillator", "logic_ic", "microcontroller", "microprocessor", "fpga", "cpu", "gpu", "chipset"}: return chip(body=PALETTE["silicon"], accent=PALETTE["amber"] if name in {"cpu", "gpu"} else PALETTE["copper"])
    if name in {"dip", "soic", "qfp", "qfn", "bga", "lga", "to220"}: return package(name)
    if name in {"pcb", "substrate", "copper_layer", "solder_mask", "silkscreen", "motherboard"}: return board(name)
    if name == "trace": return [part("M140 650 H320 V550 H520 V350 H860 V410 H570 V610 H370 V710 H140 Z", PALETTE["copper"])]
    if name == "differential_pair": return [part("M120 610 H300 L440 470 H850 V500 H450 L310 640 H120 Z M120 700 H330 L470 560 H850 V590 H480 L340 730 H120 Z", PALETTE["copper"])]
    if name == "ground_plane": return [rr(150, 180, 700, 640, 42, PALETTE["pcb"]), circle(350, 500, 100, PALETTE["metal"], "detail"), circle(650, 500, 100, PALETTE["metal"], "detail")]
    if name in {"via", "plated_through_hole", "pad", "test_point", "mounting_hole", "fiducial", "thermal_pad"}: return [circle(500, 500, 270, PALETTE["copper"] if name in {"pad", "thermal_pad"} else PALETTE["metal"]), circle(500, 500, 140, PALETTE["ink"] if name in {"via", "plated_through_hole", "mounting_hole"} else PALETTE["amber"], "detail")]
    if name == "jumper": return [rr(250, 300, 500, 260, 30, PALETTE["ceramic"]), circle(390, 430, 50, PALETTE["metal"], "detail"), circle(610, 430, 50, PALETTE["metal"], "detail")]
    if name == "bga_footprint": return package("bga")
    if name in {"ddr3_dimm", "ddr4_dimm", "ddr5_dimm"}: return memory(name[:4])
    if name in {"ddr3_dimm_slot", "ddr4_dimm_slot", "ddr5_dimm_slot", "pcie_x1_slot", "pcie_x16_slot", "isa_slot", "pci_slot", "agp_slot"}: return slot(name)
    if name in {"m2_socket"}: return slot("pcie_x1_slot")
    if name in {"nvme_ssd", "sata_ssd", "hdd", "sd_card"}: return disk(name)
    if name in {"usb_a", "usb_c", "hdmi", "displayport", "rj45", "audio_jack_35mm", "sata_connector", "atx_24pin", "cpu_power_8pin", "pcie_power_8pin", "ide_connector", "scsi_connector", "vga", "ps2"}: return connector(name)
    if name in {"fan"}: return [circle(500, 500, 310, PALETTE["metal"]), circle(500, 500, 85, PALETTE["copper"], "detail"), part("M500 460 Q670 260 610 500 Q670 740 500 540 Q330 740 390 500 Q330 260 500 460 Z", PALETTE["blue"], "detail")]
    if name == "heatsink": return [rr(270, 280, 460, 440, 20, PALETTE["metal"])] + [rr(x, 160, 28, 600, 5, PALETTE["copper"], "detail") for x in (300, 380, 460, 540, 620, 700)]
    if name in {"wifi_nic", "ethernet_nic"}: return board("pcb") + [rr(330, 350, 340, 220, 16, PALETTE["silicon"], "detail")]
    if name in {"router", "switch", "atx_psu"}: return [rr(160, 280, 680, 440, 36, PALETTE["silicon"]), *[circle(300 + i * 90, 520, 28, PALETTE["amber"], "detail") for i in range(5)]]
    if name == "antenna": return [line(500, 760, 500, 290, 26, PALETTE["metal"]), circle(500, 220, 90, PALETTE["copper"]), part("M350 300 Q500 120 650 300 L620 330 Q500 190 380 330 Z", PALETTE["blue"], "detail")]
    if name == "coin_cell_battery": return [circle(500, 500, 260, PALETTE["metal"]), circle(500, 500, 210, PALETTE["ceramic"], "detail"), line(500, 300, 500, 410, 24, PALETTE["red"], "detail"), line(445, 355, 555, 355, 24, PALETTE["red"], "detail")]
    if name.endswith("_protocol") or name in {"x86_64", "arm64", "riscv"}: return [circle(500, 500, 260, PALETTE["blue"]), part("M280 500 H720 M500 280 V720 M350 350 L650 650 M650 350 L350 650", PALETTE["paper"], "detail")]
    if name.endswith("_cable"): return [part("M120 500 Q300 180 500 500 T880 500 L830 560 Q680 470 500 560 T170 560 Z", PALETTE["blue"]), circle(150, 530, 60, PALETTE["metal"], "detail"), circle(850, 530, 60, PALETTE["metal"], "detail")]
    return chip()
