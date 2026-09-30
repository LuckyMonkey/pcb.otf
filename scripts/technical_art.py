"""Technical-plate vector masters for the first ATX assembly objects."""

from __future__ import annotations

from hardware_designs import PALETTE, circle, line, part, rr


TECHNICAL_BASES = {
    "atx_motherboard", "mounting_hole", "cpu_socket", "cpu", "vrm", "heatsink", "fan", "chipset",
    "ddr4_dimm_slot", "ddr4_dimm", "pcie_x16_slot", "gpu", "pcie_x1_slot", "m2_socket", "nvme_ssd",
    "sata_connector", "sata_ssd", "atx_24pin", "cpu_power_8pin", "pcie_power_8pin", "coin_cell_battery",
    "usb_a", "rj45", "audio_jack_35mm",
}

INK = PALETTE["ink"]
METAL = PALETTE["metal"]
PCB = PALETTE["pcb"]
COPPER = PALETTE["copper"]
SILICON = PALETTE["silicon"]
CERAMIC = PALETTE["ceramic"]
BLUE = PALETTE["blue"]
AMBER = PALETTE["amber"]
PAPER = PALETTE["paper"]


def hatch(x: int, y: int, w: int, h: int, spacing: int = 24, fill: str = COPPER) -> list[tuple[str, str, str]]:
    return [line(x + offset, y, x + offset + h, y + h, 7, fill, "detail") for offset in range(-h, w, spacing)]


def hole(cx: int, cy: int, r: int = 30) -> list[tuple[str, str, str]]:
    return [circle(cx, cy, r, METAL), circle(cx, cy, r - 12, INK, "knockout")]


def board() -> list[tuple[str, str, str]]:
    result = [rr(90, 80, 820, 840, 24, PCB)]
    for cx, cy in ((135, 125), (865, 125), (135, 875), (865, 875)):
        result.extend(hole(cx, cy, 34))
    result.extend([
        rr(210, 165, 78, 540, 8, COPPER, "detail"),
        rr(720, 150, 82, 560, 8, COPPER, "detail"),
        rr(310, 750, 480, 42, 7, COPPER, "detail"),
        rr(325, 210, 345, 300, 12, PAPER, "knockout"),
        rr(340, 225, 315, 270, 8, SILICON, "detail"),
    ])
    result.extend(hatch(155, 545, 690, 110, 42, COPPER))
    result.extend([
        part("M180 720 H330 V680 H620 V720 H850", COPPER, "detail"),
        part("M290 145 V330 H650 V145", COPPER, "detail"),
        part("M650 510 V660 H840", COPPER, "detail"),
    ])
    return result


def cpu_socket() -> list[tuple[str, str, str]]:
    result = [rr(220, 210, 560, 560, 20, METAL), rr(265, 255, 470, 470, 10, INK, "knockout"), rr(305, 295, 390, 390, 8, CERAMIC, "detail")]
    for x in range(285, 730, 44):
        result += [rr(x, 185, 18, 25, 3, COPPER, "detail"), rr(x, 790, 18, 25, 3, COPPER, "detail")]
    for y in range(285, 730, 44):
        result += [rr(185, y, 25, 18, 3, COPPER, "detail"), rr(790, y, 25, 18, 3, COPPER, "detail")]
    return result


def cpu() -> list[tuple[str, str, str]]:
    result = [rr(250, 250, 500, 500, 14, SILICON), rr(285, 285, 430, 430, 8, METAL, "detail"), rr(330, 330, 340, 340, 5, CERAMIC, "detail"), part("M380 380 H620 V620 H380 Z", INK, "knockout")]
    for x in range(310, 720, 58):
        result += [rr(x, 210, 18, 40, 3, METAL, "detail"), rr(x, 750, 18, 40, 3, METAL, "detail")]
    for y in range(310, 720, 58):
        result += [rr(210, y, 40, 18, 3, METAL, "detail"), rr(750, y, 40, 18, 3, METAL, "detail")]
    result.append(circle(315, 315, 12, COPPER, "detail"))
    return result


def vrm() -> list[tuple[str, str, str]]:
    result = [rr(250, 140, 500, 720, 18, CERAMIC)]
    for x in (300, 420, 540, 660):
        result += [rr(x, 210, 70, 170, 8, SILICON, "detail"), rr(x + 8, 420, 54, 250, 5, COPPER, "detail")]
    result.extend(hatch(278, 690, 430, 74, 28, COPPER))
    return result


def dimm_slot() -> list[tuple[str, str, str]]:
    return [rr(120, 420, 760, 160, 16, METAL), rr(155, 455, 690, 90, 4, INK, "knockout"), rr(475, 420, 42, 160, 4, CERAMIC, "detail")]


def dimm() -> list[tuple[str, str, str]]:
    result = [part("M140 450 H820 V530 H140 Z", PCB), rr(155, 385, 650, 100, 6, METAL, "detail"), part("M170 450 H790 V500 H170 Z", COPPER, "detail")]
    for x in range(185, 790, 45):
        result.append(rr(x, 395, 30, 72, 3, SILICON, "detail"))
    result.append(part("M465 450 V530 H520 V450", PAPER, "knockout"))
    return result


def expansion_slot(length: int) -> list[tuple[str, str, str]]:
    return [rr(100, 430, length, 140, 8, METAL), rr(125, 465, length - 50, 70, 3, INK, "knockout"), rr(230, 430, 38, 140, 3, CERAMIC, "detail")]


def gpu() -> list[tuple[str, str, str]]:
    result = [rr(110, 360, 780, 280, 14, PCB), rr(155, 405, 250, 190, 8, SILICON, "detail"), rr(470, 400, 310, 200, 8, METAL, "detail"), *[circle(x, 500, 32, BLUE, "detail") for x in (520, 620, 720)], part("M150 575 H850", COPPER, "detail")]
    result += [rr(90, 385, 34, 230, 4, METAL, "detail"), rr(860, 430, 45, 130, 4, METAL, "detail")]
    result += [circle(145, 390, 12, COPPER, "detail"), circle(145, 610, 12, COPPER, "detail"), circle(855, 390, 12, COPPER, "detail"), circle(855, 610, 12, COPPER, "detail")]
    result += [rr(x, 640, 22, 70, 2, COPPER, "detail") for x in range(170, 840, 34)]
    return result


def m2_socket() -> list[tuple[str, str, str]]:
    return [rr(120, 430, 760, 140, 10, METAL), rr(155, 460, 690, 80, 3, INK, "knockout"), rr(480, 430, 40, 140, 2, CERAMIC, "detail")]


def nvme() -> list[tuple[str, str, str]]:
    return [part("M130 440 H850 V560 H130 Z", PCB), rr(180, 465, 110, 70, 4, COPPER, "detail"), rr(360, 465, 110, 70, 4, SILICON, "detail"), rr(540, 465, 110, 70, 4, SILICON, "detail"), part("M790 440 V560 H850", PAPER, "knockout")]


def drive() -> list[tuple[str, str, str]]:
    return [rr(180, 230, 640, 540, 22, METAL), rr(250, 300, 500, 380, 12, SILICON, "detail"), rr(320, 370, 360, 240, 180, PAPER, "knockout"), rr(490, 485, 20, 20, 20, COPPER, "detail")]


def connector(kind: str) -> list[tuple[str, str, str]]:
    dimensions = {"usb_a": (230, 350, 420, 300), "rj45": (220, 300, 460, 400), "audio_jack_35mm": (300, 270, 300, 460), "atx_24pin": (290, 160, 420, 680), "cpu_power_8pin": (330, 260, 340, 480), "pcie_power_8pin": (330, 260, 340, 480), "sata_connector": (270, 300, 460, 400)}
    x, y, w, h = dimensions[kind]
    result = [rr(x, y, w, h, 14, CERAMIC)]
    if kind == "usb_a":
        result += [rr(x + 55, y + 55, w - 110, h - 110, 8, INK, "knockout"), rr(x + 105, y + 125, w - 210, 35, 6, METAL, "detail")]
    elif kind == "rj45":
        result += [rr(x + 45, y + 55, w - 90, h - 110, 8, INK, "knockout"), *[circle(x + 100 + i * 70, y + h - 75, 14, AMBER, "detail") for i in range(5)]]
    elif kind == "audio_jack_35mm":
        result += [circle(x + w // 2, y + 175, 90, INK, "knockout"), circle(x + w // 2, y + 175, 38, METAL, "detail"), line(x + 50, y + 300, x + w - 50, y + 300, 16, COPPER, "detail")]
    elif kind == "sata_connector":
        result += [rr(x + 45, y + 60, w - 90, h - 120, 5, INK, "knockout"), *[line(x + 80 + i * 26, y + 95, x + 80 + i * 26, y + h - 95, 8, COPPER, "detail") for i in range(12)]]
    else:
        result += [rr(x + 40, y + 45, w - 80, h - 90, 5, INK, "knockout")]
        for px in range(x + 75, x + w - 45, 55):
            for py in range(y + 80, y + h - 35, 70):
                result.append(circle(px, py, 12, COPPER, "detail"))
    return result


def fan() -> list[tuple[str, str, str]]:
    return [circle(500, 500, 320, METAL), circle(500, 500, 75, COPPER, "detail"), part("M500 440 Q710 260 620 500 Q710 740 500 560 Q290 740 380 500 Q290 260 500 440 Z", BLUE, "detail"), circle(500, 500, 30, INK, "knockout")]


def heatsink() -> list[tuple[str, str, str]]:
    return [rr(250, 315, 500, 370, 10, METAL), *[rr(x, 180, 26, 640, 3, COPPER, "detail") for x in range(285, 720, 62)], hatch(285, 330, 420, 280, 42, PAPER)[0]]


def chipset() -> list[tuple[str, str, str]]:
    return [rr(260, 260, 480, 480, 12, SILICON), rr(315, 315, 370, 370, 5, METAL, "detail"), part("M380 380 H620 V620 H380 Z", INK, "knockout")]


def coin_cell() -> list[tuple[str, str, str]]:
    return [circle(500, 500, 260, METAL), circle(500, 500, 210, CERAMIC, "detail"), line(500, 300, 500, 410, 24, PALETTE["red"], "detail"), line(445, 355, 555, 355, 24, PALETTE["red"], "detail")]


def mounting_hole() -> list[tuple[str, str, str]]:
    return hole(500, 500, 280)


def profile(name: str, side: bool = False) -> list[tuple[str, str, str]]:
    if name in {"atx_motherboard", "motherboard"}:
        return [rr(120, 430 if side else 400, 760, 110 if side else 180, 8, PCB), line(145, 425 if side else 390, 855, 425 if side else 390, 10, COPPER, "detail"), *hole(180, 480 if side else 490, 24)]
    if name in {"cpu", "cpu_socket", "chipset", "vrm"}:
        return [rr(260, 340, 480, 220, 10, SILICON if name == "cpu" else METAL), rr(320, 375, 360, 95, 5, CERAMIC, "detail"), line(290, 560, 710, 560, 16, COPPER, "detail")]
    if name in {"ddr4_dimm", "ddr4_dimm_slot"}:
        return [rr(180, 350, 640, 270, 8, PCB), line(190, 600, 810, 600, 12, COPPER, "detail"), rr(230, 390, 540, 120, 4, SILICON if name == "ddr4_dimm" else INK, "detail" if name == "ddr4_dimm" else "knockout")]
    if name in {"pcie_x16_slot", "pcie_x1_slot", "m2_socket", "sata_connector"}:
        return [rr(150, 430, 700, 140, 6, METAL), rr(180, 455, 640, 70, 2, INK, "knockout"), line(220, 425, 780, 425, 12, COPPER, "detail")]
    if name in {"gpu", "nvme_ssd", "sata_ssd"}:
        return [rr(150, 380, 700, 250, 12, METAL), rr(220, 425, 560, 120, 6, SILICON, "detail"), line(180, 615, 820, 615, 14, COPPER, "detail")]
    if name in {"heatsink", "fan"}:
        return [rr(200, 300, 600, 300, 10, METAL), *[rr(x, 230, 24, 440, 2, COPPER, "detail") for x in range(240, 780, 70)]]
    if name == "mounting_hole":
        return [rr(300, 380, 400, 240, 10, METAL), rr(350, 430, 300, 140, 4, INK, "knockout")]
    return connector(name if name in {"usb_a", "rj45", "audio_jack_35mm", "atx_24pin", "cpu_power_8pin", "pcie_power_8pin"} else "usb_a")


def technical_for(name: str, view: str = "top") -> list[tuple[str, str, str]]:
    if view in {"front", "side"}:
        return profile(name, side=view == "side")
    if name == "atx_motherboard": return board()
    if name == "mounting_hole": return mounting_hole()
    if name == "cpu_socket": return cpu_socket()
    if name == "cpu": return cpu()
    if name == "vrm": return vrm()
    if name == "heatsink": return heatsink()
    if name == "fan": return fan()
    if name == "chipset": return chipset()
    if name == "ddr4_dimm_slot": return dimm_slot()
    if name == "ddr4_dimm": return dimm()
    if name == "pcie_x16_slot": return expansion_slot(760)
    if name == "pcie_x1_slot": return expansion_slot(430)
    if name == "gpu": return gpu()
    if name == "m2_socket": return m2_socket()
    if name == "nvme_ssd": return nvme()
    if name == "sata_connector": return connector(name)
    if name == "sata_ssd": return drive()
    if name in {"usb_a", "rj45", "audio_jack_35mm", "atx_24pin", "cpu_power_8pin", "pcie_power_8pin"}: return connector(name)
    if name == "coin_cell_battery": return coin_cell()
    raise KeyError(name)
