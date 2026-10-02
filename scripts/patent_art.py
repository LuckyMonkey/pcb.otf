"""PCB.OTF glyph art: one original patent-style drawing per object, at full detail.

Every object has its own drawing (no shared generic chip). Views follow how the thing is recognised: boards, slots
and packages from above; connectors by their mating face; components that are read by profile (an LED, a capacitor
can, a DIMM) from the side. The drawing language is the patent plate: heavy outline, medium parts, fine hatching.
See patent_pen.py for why every mark is a filled outline.
"""

from __future__ import annotations

import math

from patent_pen import FINE, HEAVY, MED, Pen

ART: dict[str, callable] = {}


def art(name):
    def wrap(fn):
        ART[name] = fn
        return fn
    return wrap


def draw(base: str) -> Pen | None:
    fn = ART.get(base)
    if not fn:
        return None
    p = Pen()
    fn(p)
    return p


# ======================================================================================================== passives
def _axial(p, x0=240, x1=760, y=500, h=150, tint="plastic"):
    p.line(80, y, x0, y, MED)
    p.line(x1, y, 920, y, MED)
    # a bulged body: end caps slightly fatter than the middle
    pts = []
    for i in range(41):
        t = i / 40
        x = x0 + (x1 - x0) * t
        bulge = h / 2 * (0.86 + 0.14 * (math.cos(t * math.pi * 2) + 1) / 2)
        pts.append((x, y - bulge))
    for i in range(40, -1, -1):
        t = i / 40
        x = x0 + (x1 - x0) * t
        bulge = h / 2 * (0.86 + 0.14 * (math.cos(t * math.pi * 2) + 1) / 2)
        pts.append((x, y + bulge))
    p.shape(pts, HEAVY, tint)


@art("resistor")
def _(p):
    _axial(p)
    for x, w in ((330, 34), (400, 34), (470, 34), (650, 26)):
        p.fillrect(x, 430, w, 140)
    p.line(600, 438, 600, 562, FINE)


@art("variable_resistor")
def _(p):
    _axial(p)
    for x in (330, 400, 470):
        p.fillrect(x, 430, 30, 140)
    p.arrow(260, 700, 760, 300, MED, 46)


@art("potentiometer")
def _(p):
    p.box(250, 250, 500, 420, 40, "plastic")
    p.circle(500, 440, 150, HEAVY, "metal")
    p.circle(500, 440, 70, MED)
    p.fillrect(470, 330, 60, 110)          # the D-shaft's flat, a slot
    p.arc(500, 440, 115, 140, 400, FINE)
    for x in (360, 500, 640):
        p.rect(x - 18, 670, 36, 200, 6, MED, "metal")
    for x in (290, 710):
        p.circle(x, 300, 18, FINE)


@art("ceramic_capacitor")
def _(p):
    p.circle(500, 380, 230, HEAVY, "blue")
    p.circle(500, 380, 190, FINE)
    for x in (430, 570):
        p.line(x, 560, x, 920, MED)
        p.line(x, 590, x + (x - 500) * .3, 640, FINE)
    p.hatch_circle(500, 380, 150, 34, 30)


@art("electrolytic_capacitor")
def _(p):
    p.box(330, 120, 340, 640, 34, "blue")
    p.rect(330, 120, 90, 640, 0, MED, "dark")        # the polarity sleeve stripe
    for y in (230, 330, 430, 530, 630):
        p.line(355, y, 395, y, MED)
    p.line(330, 210, 670, 210, FINE)                   # the rolled crimp
    p.line(330, 230, 670, 230, FINE)
    p.line(450, 120, 550, 120, MED)
    for x, y1 in ((440, 900), (560, 860)):
        p.line(x, 760, x, y1, MED)


@art("inductor")
def _(p):
    p.circle(500, 500, 330, HEAVY, "dark")
    p.circle(500, 500, 150, HEAVY, "paper")
    for i in range(28):
        a = 2 * math.pi * i / 28
        p.line(500 + 160 * math.cos(a), 500 + 160 * math.sin(a), 500 + 320 * math.cos(a + .08), 500 + 320 * math.sin(a + .08), MED)
    p.line(170, 500, 70, 500, MED)
    p.line(830, 500, 930, 500, MED)


@art("transformer")
def _(p):
    p.box(150, 230, 700, 540, 0, "metal")
    for y in range(260, 760, 26):
        p.line(150, y, 850, y, FINE)
    p.rect(250, 330, 500, 340, 0, MED, "paper")      # the window in the E-I stack
    for x0 in (290, 520):
        p.box(x0, 300, 190, 400, 24, "copper")
        for y in range(330, 690, 30):
            p.line(x0 + 10, y, x0 + 180, y + 14, FINE)
    for x in (320, 420, 580, 680):
        p.line(x, 770, x, 900, MED)


@art("fuse")
def _(p):
    p.box(250, 400, 500, 200, 90, "glass")
    p.rect(160, 380, 120, 240, 18, HEAVY, "metal")
    p.rect(720, 380, 120, 240, 18, HEAVY, "metal")
    p.path([(280, 500), (360, 470), (430, 530), (500, 470), (570, 530), (640, 470), (720, 500)], MED)
    p.line(300, 430, 700, 430, FINE)
    p.line(80, 500, 160, 500, MED)
    p.line(840, 500, 920, 500, MED)


@art("thermistor")
def _(p):
    p.circle(500, 340, 190, HEAVY, "red")
    p.circle(500, 340, 150, FINE)
    for x in (440, 560):
        p.line(x, 520, x, 900, MED)
    p.path([(320, 600), (380, 600), (680, 160)], MED)     # the thermistor's hockey stick
    p.line(470, 340, 530, 340, FINE)


@art("crystal")
def _(p):
    p.box(250, 300, 500, 300, 150, "metal")
    p.rect(290, 330, 420, 240, 120, MED)
    p.rect(380, 395, 240, 110, 30, FINE, "glass")
    for x in (420, 580):
        p.line(x, 600, x, 900, MED)


# ==================================================================================================== semiconductors
@art("diode")
def _(p):
    p.line(80, 500, 280, 500, MED)
    p.line(720, 500, 920, 500, MED)
    p.box(280, 410, 440, 180, 20, "dark")
    p.fillrect(610, 410, 56, 180)                       # cathode band
    p.path([(380, 450), (380, 550), (500, 500)], FINE, closed=True)
    p.line(500, 450, 500, 550, FINE)


@art("led")
def _(p):
    p.box(330, 140, 340, 470, 170, "red")
    p.rect(300, 560, 400, 60, 8, HEAVY, "red")         # flange
    p.path([(420, 560), (420, 400), (470, 360), (470, 560)], MED)   # anvil
    p.path([(560, 560), (560, 380)], MED)               # post
    p.line(470, 360, 560, 380, FINE)
    p.line(440, 620, 440, 920, MED)                     # cathode (short)
    p.line(560, 620, 560, 880, MED)
    p.line(300, 590, 330, 590, FINE)                    # the flat on the cathode side


@art("photodiode")
def _(p):
    p.box(300, 330, 400, 400, 30, "dark")
    p.circle(500, 530, 110, HEAVY, "glass")
    p.rect(470, 500, 60, 60, 4, FINE)
    for x in (430, 570):
        p.line(x, 730, x, 920, MED)
    for dx in (0, 110):
        p.arrow(130 + dx, 90, 330 + dx, 290, MED)


def _transistor_symbol(p, pnp=False):
    p.circle(500, 500, 300, HEAVY, "paper")
    p.line(120, 500, 400, 500, MED)
    p.line(400, 330, 400, 670, HEAVY)
    p.line(400, 420, 640, 260, MED)
    p.line(640, 260, 640, 100, MED)
    p.line(400, 580, 640, 740, MED)
    p.line(640, 740, 640, 900, MED)
    if not pnp:
        p.solid([(640, 740), (560, 732), (600, 668)])
    else:
        p.solid([(410, 588), (488, 600), (450, 664)])


@art("npn_transistor")
def _(p):
    _transistor_symbol(p)


@art("pnp_transistor")
def _(p):
    _transistor_symbol(p, pnp=True)


@art("mosfet")
def _(p):
    p.circle(500, 500, 300, HEAVY, "paper")
    p.line(120, 620, 380, 620, MED)
    p.line(380, 380, 380, 620, MED)                     # gate
    for y in (380, 500, 620):
        p.line(430, y - 45, 430, y + 45, HEAVY)          # enhancement channel, broken
    p.line(430, 380, 640, 380, MED)
    p.line(640, 380, 640, 100, MED)
    p.line(430, 620, 640, 620, MED)
    p.line(640, 620, 640, 900, MED)
    p.line(430, 500, 640, 500, MED)
    p.line(640, 500, 640, 620, MED)
    p.solid([(440, 500), (500, 470), (500, 530)])
    p.path([(700, 380), (700, 620)], FINE)               # the body diode
    p.solid([(700, 520), (675, 470), (725, 470)])
    p.line(675, 520, 725, 520, FINE)
    p.line(640, 380, 700, 380, FINE)
    p.line(640, 620, 700, 620, FINE)


@art("voltage_regulator")
def _(p):
    # SOT-223: one wide tab, three pins
    p.box(260, 330, 480, 330, 12, "dark")
    p.rect(330, 170, 340, 160, 6, HEAVY, "metal")
    for x in (330, 470, 610):
        p.rect(x, 660, 60, 180, 6, MED, "metal")
    p.circle(310, 610, 16, FINE)
    p.path([(420, 420), (580, 420), (580, 560), (420, 560)], FINE, closed=True)
    p.line(380, 490, 420, 490, FINE)
    p.line(580, 490, 620, 490, FINE)
    p.line(500, 560, 500, 600, FINE)


@art("op_amp")
def _(p):
    p.box(310, 160, 380, 680, 18, "dark")
    p.arc(500, 160, 50, 0, 180, MED)
    for i in range(4):
        y = 250 + i * 160
        p.rect(220, y, 90, 40, 6, MED, "metal")
        p.rect(690, y, 90, 40, 6, MED, "metal")
    p.path([(400, 380), (400, 620), (610, 500)], MED, closed=True)
    p.line(420, 440, 450, 440, FINE)
    p.line(420, 560, 450, 560, FINE)
    p.line(435, 545, 435, 575, FINE)


@art("oscillator")
def _(p):
    p.box(200, 260, 600, 480, 40, "metal")
    p.rect(240, 300, 520, 400, 24, MED)
    p.solid([(240, 300), (330, 300), (240, 390)])        # pin-1 corner marker
    for x, y in ((270, 740), (690, 740)):
        p.rect(x, y, 40, 150, 6, MED, "metal")
    p.path([(330, 520), (380, 440), (430, 600), (480, 440), (530, 600), (580, 440), (630, 600), (670, 520)], MED)


@art("logic_ic")
def _(p):
    # SOIC-14 with a NAND gate engraved: logic you can see
    p.box(300, 200, 400, 600, 10, "dark")
    p.line(300, 260, 700, 260, FINE)                      # bevel edge (pin-1 side)
    for i in range(7):
        y = 230 + i * 82
        p.rect(220, y, 80, 30, 4, FINE, "metal")
        p.rect(700, y, 80, 30, 4, FINE, "metal")
    p.path([(390, 400), (480, 400)], MED)
    p.arc(480, 500, 100, -90, 90, MED)
    p.path([(390, 400), (390, 600), (480, 600)], MED)
    p.circle(598, 500, 18, MED)
    p.circle(330, 230, 10, FINE)


def _qfp(p, x, y, s, n, tint="dark", pin=56):
    p.box(x, y, s, s, 8, tint)
    pitch = (s - 80) / (n - 1)
    for i in range(n):
        o = 40 + i * pitch
        p.rect(x + o - 7, y - pin, 14, pin, 2, FINE, "metal")
        p.rect(x + o - 7, y + s, 14, pin, 2, FINE, "metal")
        p.rect(x - pin, y + o - 7, pin, 14, 2, FINE, "metal")
        p.rect(x + s, y + o - 7, pin, 14, 2, FINE, "metal")


@art("microcontroller")
def _(p):
    _qfp(p, 240, 240, 520, 11)
    p.circle(300, 300, 18, MED)
    p.dashed_rect(400, 400, 200, 200)                    # the die, seen through
    for i in range(6):
        p.line(400 + i * 40, 400, 330 + i * 60, 260, FINE)
    p.line(240, 290, 290, 240, MED)                       # chamfered pin-1 corner


@art("microprocessor")
def _(p):
    # a ceramic PGA: the classic CPU from below
    p.box(150, 150, 700, 700, 14, "plastic")
    p.grid_dots(200, 200, 13, 13, 50, 10, skip=lambda i, j: 3 <= i <= 9 and 3 <= j <= 9)
    p.rect(330, 330, 340, 340, 8, HEAVY, "metal")       # the die cavity lid
    p.hatch(350, 350, 300, 300, 40, 45)
    p.solid([(150, 150), (230, 150), (150, 230)])        # pin-1 corner


@art("fpga")
def _(p):
    p.box(150, 150, 700, 700, 10, "pcb")
    p.rect(230, 230, 540, 540, 6, HEAVY, "silicon")
    for i in range(1, 9):
        p.line(230 + i * 60, 230, 230 + i * 60, 770, FINE)   # the logic fabric
        p.line(230, 230 + i * 60, 770, 230 + i * 60, FINE)
    for (i, j) in ((1, 1), (2, 5), (4, 3), (6, 6), (7, 2), (5, 7)):
        p.fillrect(236 + i * 60, 236 + j * 60, 48, 48)
    p.solid([(150, 150), (220, 150), (150, 220)])


@art("cpu")
def _(p):
    # a modern LGA desktop CPU: substrate, keyed notches, integrated heat spreader with ears
    p.box(130, 170, 740, 660, 10, "pcb")
    for y in (300, 640):
        p.fillrect(130, y, 30, 60)                          # orientation notches
        p.fillrect(840, y, 30, 60)
    ihs = [(260, 230), (740, 230), (740, 300), (800, 300), (800, 700), (740, 700), (740, 770), (260, 770),
           (260, 700), (200, 700), (200, 300), (260, 300)]
    p.shape(ihs, HEAVY, "metal")
    p.rect(300, 340, 400, 320, 16, FINE)
    p.solid([(150, 190), (210, 190), (150, 250)])          # gold triangle: pin 1
    for x in range(330, 680, 70):
        p.rect(x, 790, 34, 22, 3, FINE, "metal")            # the land-side capacitors peek out


@art("gpu")
def _(p):
    p.box(120, 120, 760, 760, 10, "pcb")
    p.rect(170, 170, 660, 660, 4, MED)                      # the stiffener ring
    p.rect(310, 310, 380, 380, 4, HEAVY, "silicon")        # the bare die
    p.hatch(330, 330, 340, 340, 34, 60)
    for k in range(9):
        o = 330 + k * 40
        for x, y in ((o, 230), (o, 740), (230, o), (740, o)):
            p.rect(x - 9, y - 14, 18, 28, 3, FINE, "metal")


@art("chipset")
def _(p):
    p.box(170, 170, 660, 660, 10, "pcb")
    p.rect(420, 300, 260, 220, 6, HEAVY, "silicon")
    p.hatch(434, 314, 232, 192, 30, 45)
    p.rect(250, 610, 500, 150, 6, MED)
    for x in range(280, 740, 52):
        for y in (640, 700):
            p.rect(x, y, 30, 20, 3, FINE, "metal")
    p.solid([(170, 170), (240, 170), (170, 240)])
    p.circle(300, 330, 40, MED)


# ========================================================================================================== packages
@art("dip")
def _(p):
    p.box(330, 120, 340, 760, 16, "dark")
    p.arc(500, 120, 52, 0, 180, MED)
    for i in range(7):
        y = 180 + i * 100
        for x0, sign in ((330, -1), (670, 1)):
            x1 = x0 + sign * 60
            p.shape([(x0, y), (x1, y), (x1, y + 50), (x0, y + 50)], MED, "metal")
            p.line(x1 + sign * 0, y + 25, x1 + sign * 90, y + 25, MED)
    p.circle(400, 200, 16, FINE)


@art("soic")
def _(p):
    p.box(340, 210, 320, 580, 10, "dark")
    p.line(340, 270, 660, 270, FINE)
    for i in range(8):
        y = 240 + i * 70
        p.path([(340, y), (290, y), (270, y + 26), (210, y + 26)], MED)
        p.path([(660, y), (710, y), (730, y + 26), (790, y + 26)], MED)
    p.circle(380, 240, 12, FINE)


@art("qfp")
def _(p):
    _qfp(p, 250, 250, 500, 13, "dark", 70)
    p.circle(310, 310, 22, MED)
    p.line(250, 300, 300, 250, MED)


@art("qfn")
def _(p):
    p.box(220, 220, 560, 560, 6, "dark")
    for k in range(8):
        o = 290 + k * 60
        p.rect(o - 12, 220, 24, 60, 3, FINE, "metal")
        p.rect(o - 12, 720, 24, 60, 3, FINE, "metal")
        p.rect(220, o - 12, 60, 24, 3, FINE, "metal")
        p.rect(720, o - 12, 60, 24, 3, FINE, "metal")
    p.dashed_rect(360, 360, 280, 280, MED)               # the exposed thermal pad, hidden line
    p.solid([(220, 220), (300, 220), (220, 300)])


@art("bga")
def _(p):
    p.box(150, 150, 700, 700, 10, "pcb")
    p.grid_dots(210, 210, 12, 12, 52.7, 16, skip=lambda i, j: i == 0 and j == 0)
    p.solid([(150, 150), (195, 150), (150, 195)])


@art("lga")
def _(p):
    p.box(150, 150, 700, 700, 10, "pcb")
    for i in range(12):
        for j in range(12):
            if 4 <= i <= 7 and 4 <= j <= 7:
                continue
            p.rect(196 + i * 52.7, 202 + j * 52.7, 30, 18, 3, FINE, "gold")
    p.rect(390, 390, 220, 220, 6, FINE)
    for x in range(410, 600, 40):
        for y in (420, 470, 520, 570):
            p.rect(x, y, 20, 14, 2, FINE)
    p.solid([(150, 150), (215, 150), (150, 215)])


@art("to220")
def _(p):
    p.box(300, 110, 400, 300, 10, "metal")
    p.circle(500, 220, 60, HEAVY)
    p.box(300, 400, 400, 280, 10, "dark")
    p.line(300, 440, 700, 440, FINE)
    for x in (370, 500, 630):
        p.path([(x, 680), (x, 740), (x, 900)], HEAVY)
        p.line(x - 22, 740, x + 22, 740, FINE)


# ============================================================================================================ boards
def _hole(p, x, y):
    p.circle(x, y, 26, MED, "metal")
    p.circle(x, y, 13, FINE)


@art("pcb")
def _(p):
    p.box(110, 170, 780, 660, 30, "pcb")
    for x, y in ((160, 220), (840, 220), (160, 780), (840, 780)):
        _hole(p, x, y)
    p.rect(300, 330, 160, 160, 6, MED, "silicon")
    p.rect(580, 560, 130, 60, 6, MED, "plastic")
    p.path([(460, 410), (540, 410), (600, 470), (600, 560)], MED)
    p.path([(380, 490), (380, 620), (440, 680), (700, 680)], MED)
    p.path([(300, 400), (240, 400), (240, 300), (520, 300)], FINE)
    for x, y in ((540, 410), (700, 680), (520, 300), (240, 700)):
        p.circle(x, y, 18, FINE)


def _board(p, x, y, w, h, atx=False):
    p.box(x, y, w, h, 8, "pcb")
    # socket, DIMMs, chipset, PCIe, rear I/O, power
    p.rect(x + w * .28, y + h * .14, w * .28, w * .28, 6, MED, "metal")
    p.rect(x + w * .33, y + h * .14 + w * .05, w * .18, w * .18, 4, FINE)
    for k in range(4 if atx else 2):
        p.rect(x + w * .68 + k * w * .05, y + h * .08, w * .03, h * .5, 2, MED, "plastic")
    p.rect(x + w * .58, y + h * .64, w * .14, w * .14, 4, MED, "silicon")
    for k in range(3 if atx else 2):
        yy = y + h * (.66 + k * .1)
        p.rect(x + w * .06, yy, w * .48, h * .04, 2, MED, "dark")
    p.rect(x + w * .02, y + h * .06, w * .14, h * .42, 4, MED, "metal")
    for k in range(5):
        p.rect(x + w * .045, y + h * (.09 + k * .075), w * .09, h * .05, 2, FINE)
    p.rect(x + w * .92, y + h * .3, w * .05, h * .3, 2, MED, "plastic")


@art("motherboard")
def _(p):
    _board(p, 110, 160, 780, 680)
    for x, y in ((150, 200), (850, 200), (150, 800), (850, 800)):
        _hole(p, x, y)


@art("atx_motherboard")
def _(p):
    # ATX: 305 x 244 mm, nine mounting holes in their standard places
    w, h = 820, 656
    x, y = 90, 172
    _board(p, x, y, w, h, atx=True)
    s = w / 305
    for hx, hy in ((6.35, 10.16), (163.83, 10.16), (288.29, 10.16), (6.35, 165.1), (163.83, 165.1), (288.29, 165.1),
                   (6.35, 237.49), (163.83, 237.49), (288.29, 237.49)):
        _hole(p, x + hx * s, y + hy * s)


# ======================================================================================================= PCB features
def _stack(p, layers, x=120, w=760, y=300):
    """A board cross-section, top to bottom: (height, kind) with kind in core | copper | mask | silk."""
    for hgt, kind in layers:
        if kind == "core":
            p.rect(x, y, w, hgt, 0, MED, "pcb")
            p.hatch(x, y, w, hgt, 30, 45)
        elif kind == "copper":
            p.rect(x, y, w, hgt, 0, MED, "copper")
            p.hatch(x, y, w, hgt, 14, 135)
        elif kind == "mask":
            p.rect(x, y, w, hgt, 0, MED, "pcb")
        elif kind == "silk":
            p.rect(x, y, w, hgt, 0, FINE, "paper")
        y += hgt
    return y


@art("substrate")
def _(p):
    _stack(p, [(80, "core"), (240, "core"), (80, "core")])
    for y in (380, 620):
        p.line(120, y, 880, y, HEAVY)                        # the glass weave plies
    p.box(120, 300, 760, 400)


@art("copper_layer")
def _(p):
    _stack(p, [(70, "copper"), (300, "core"), (70, "copper")], y=280)
    p.box(120, 280, 760, 440)
    p.arrow(700, 170, 700, 270, MED)
    p.arrow(700, 830, 700, 730, MED)


@art("solder_mask")
def _(p):
    y = _stack(p, [(260, "core")], y=470)
    for x in (200, 420, 640):
        p.rect(x, 410, 160, 60, 0, MED, "copper")
    pts = [(120, 470)]
    for x in (200, 420, 640):
        pts += [(x - 20, 470), (x - 20, 390), (x + 180, 390), (x + 180, 470)]
    pts += [(880, 470), (880, 440), (120, 440)]
    p.path([(120, 440), (180, 440), (180, 380), (380, 380), (380, 440), (400, 440), (400, 380), (600, 380), (600, 440),
            (620, 440), (620, 380), (820, 380), (820, 440), (880, 440)], HEAVY)
    p.box(120, 470, 760, 260)


@art("silkscreen")
def _(p):
    p.box(110, 150, 780, 700, 20, "pcb")
    p.dashed_rect(250, 280, 280, 200, MED)
    p.rect(310, 330, 60, 100, 4, MED, "copper")
    p.rect(410, 330, 60, 100, 4, MED, "copper")
    p.circle(650, 600, 120, MED)
    p.line(650, 470, 650, 520, MED)
    p.fillrect(560, 460, 30, 30)
    p.line(580, 700, 720, 700, MED)                          # the polarity bar
    p.line(200, 760, 330, 760, MED)
    p.path([(220, 720), (260, 690), (300, 720)], FINE)


@art("trace")
def _(p):
    for y0, y1 in ((280, 520), (400, 640), (520, 760)):
        p.rect(110, y0 - 40, 120, 80, 10, MED, "copper")
        p.rect(770, y1 - 40, 120, 80, 10, MED, "copper")
        p.path([(230, y0), (430, y0), (430 + (y1 - y0), y1), (770, y1)], 30)


@art("differential_pair")
def _(p):
    # a tightly coupled pair; the inner trace carries the length-tuning accordion
    for x in (90, 830):
        p.rect(x, 400, 80, 60, 8, MED, "copper")
        p.rect(x, 540, 80, 60, 8, MED, "copper")
    p.path([(170, 430), (260, 430), (300, 470), (700, 470), (740, 430), (830, 430)], 22)
    pts = [(170, 570), (260, 570), (300, 530), (360, 530)]
    for k in range(4):
        x = 360 + k * 80
        pts += [(x, 530), (x, 640), (x + 40, 640), (x + 40, 530)]
    pts += [(700, 530), (740, 570), (830, 570)]
    p.path(pts, 22)
    p.line(330, 500, 330, 500, FINE)


@art("ground_plane")
def _(p):
    p.box(120, 120, 760, 760, 0, "copper")
    p.hatch(120, 120, 760, 760, 40, 45)
    p.circle(500, 500, 150, HEAVY, "paper")                  # clearance
    p.circle(500, 500, 70, MED, "copper")
    for a in (45, 135, 225, 315):                               # thermal relief spokes
        r = math.radians(a)
        p.line(500 + 70 * math.cos(r), 500 + 70 * math.sin(r), 500 + 150 * math.cos(r), 500 + 150 * math.sin(r), 34)


@art("via")
def _(p):
    p.circle(500, 500, 230, HEAVY, "copper")
    p.circle(500, 500, 110, HEAVY, "paper")
    p.hatch_circle(500, 500, 225, 26, 45)
    p.circle(500, 500, 110, HEAVY, "paper")
    p.rect(80, 470, 200, 60, 0, MED, "copper")
    p.rect(720, 470, 200, 60, 0, MED, "copper")


@art("plated_through_hole")
def _(p):
    _stack(p, [(60, "copper"), (360, "core"), (60, "copper")], y=260)
    p.rect(400, 240, 200, 520, 0, HEAVY, "paper")          # the drilled barrel
    for x in (400, 572):
        p.rect(x, 240, 28, 520, 0, MED, "copper")           # its plating
    p.rect(320, 230, 360, 40, 0, MED, "copper")
    p.rect(320, 730, 360, 40, 0, MED, "copper")
    p.box(120, 260, 760, 480)


@art("pad")
def _(p):
    p.box(160, 330, 260, 340, 18, "copper")
    p.box(580, 330, 260, 340, 18, "copper")
    p.rect(130, 300, 320, 400, 30, FINE)                    # mask opening
    p.rect(550, 300, 320, 400, 30, FINE)
    p.line(290, 670, 290, 880, 40)
    p.line(710, 330, 710, 120, 40)


@art("test_point")
def _(p):
    p.circle(500, 640, 200, HEAVY, "copper")
    p.circle(500, 640, 240, FINE)
    p.circle(500, 640, 50, MED)
    p.path([(500, 120), (500, 420), (470, 480), (500, 560), (530, 480), (500, 420)], MED)     # the probe tip
    p.rect(450, 60, 100, 120, 10, MED, "metal")


@art("fiducial")
def _(p):
    p.circle(500, 500, 330, MED)                               # keep-out
    p.circle(500, 500, 230, HEAVY)                             # mask opening
    p.dot(500, 500, 110)                                       # the bare copper dot
    for a in (0, 90, 180, 270):
        r = math.radians(a)
        p.line(500 + 360 * math.cos(r), 500 + 360 * math.sin(r), 500 + 430 * math.cos(r), 500 + 430 * math.sin(r), FINE)


@art("bga_footprint")
def _(p):
    p.rect(150, 150, 700, 700, 0, FINE)
    for i in range(6):
        for j in range(6):
            x, y = 230 + i * 108, 230 + j * 108
            p.circle(x, y, 30, MED, "copper")
            if i < 5 and j < 5:
                p.line(x, y, x + 54, y + 54, 14)                # dog-bone to the via
                p.circle(x + 54, y + 54, 14, FINE)


@art("thermal_pad")
def _(p):
    p.rect(160, 160, 680, 680, 0, FINE)
    for k in range(8):
        o = 260 + k * 68
        p.rect(o - 14, 170, 28, 70, 3, MED, "copper")
        p.rect(o - 14, 760, 28, 70, 3, MED, "copper")
        p.rect(170, o - 14, 70, 28, 3, MED, "copper")
        p.rect(760, o - 14, 70, 28, 3, MED, "copper")
    p.box(300, 300, 400, 400, 6, "copper")
    for i in range(4):
        for j in range(4):
            p.circle(360 + i * 93, 360 + j * 93, 20, MED)


# ======================================================================================================= mechanical
@art("jumper")
def _(p):
    p.box(250, 520, 500, 220, 6, "dark")
    for x in (375, 625):
        p.rect(x - 28, 300, 56, 520, 4, MED, "gold")
    p.box(260, 200, 480, 300, 30, "plastic")                 # the shunt cap
    p.rect(300, 240, 400, 100, 16, FINE)
    p.line(500, 200, 500, 500, FINE)


@art("mounting_hole")
def _(p):
    p.circle(500, 500, 300, HEAVY, "copper")
    p.circle(500, 500, 160, HEAVY, "paper")
    for k in range(8):
        a = 2 * math.pi * k / 8
        p.circle(500 + 230 * math.cos(a), 500 + 230 * math.sin(a), 24, MED)
    p.circle(500, 500, 380, FINE)


# ===================================================================================================== memory modules
def _dimm(p, notch, chips=8, ddr4=False, ddr5=False, x=70, w=860, y=300, h=300):
    edge = []
    if ddr4:   # DDR4's edge bows: the middle pins are longer
        for i in range(31):
            t = i / 30
            edge.append((x + w * t, y + h + 12 * math.sin(math.pi * t)))
    else:
        edge = [(x, y + h), (x + w, y + h)]
    nx = x + w * notch
    bottom = []
    for pt in edge[::-1] if False else edge:
        bottom.append(pt)
    pts = [(x, y), (x + w, y), (x + w, y + h)] + [pt for pt in edge[::-1] if nx + 18 < pt[0] < x + w]
    pts += [(nx + 18, y + h), (nx + 18, y + h - 40), (nx - 18, y + h - 40), (nx - 18, y + h)]
    pts += [pt for pt in edge[::-1] if x < pt[0] < nx - 18] + [(x, y + h)]
    p.shape(pts, HEAVY, "pcb")
    for side in (x + 10, x + w - 40):
        p.rect(side, y + 150, 30, 50, 15, MED)               # latch cut-outs
    p.gold_fingers(x + 30, y + h - 60, int((w - 60) / 14), 14, 9, 50, notch=nx)
    groups = [range(chips)] if not ddr5 else [range(chips // 2), range(chips // 2, chips)]
    cw = 70
    gap = (w - 120 - chips * cw) / (chips + (1 if ddr5 else 0))
    cx = x + 60
    for gi, g in enumerate(groups):
        for _ in g:
            p.rect(cx, y + 50, cw, 120, 4, MED, "silicon")
            p.circle(cx + 12, y + 62, 5, FINE)
            cx += cw + gap
        if ddr5 and gi == 0:
            p.rect(cx - gap / 2 + 4, y + 70, gap - 8 + cw * 0 + 30, 70, 4, MED, "dark")   # PMIC
            cx += gap
    p.rect(x + w / 2 - 40, y + 190, 80, 40, 4, FINE, "silicon")   # SPD


@art("memory_module")
def _(p):
    _dimm(p, .5, 8)


@art("ddr3_dimm")
def _(p):
    _dimm(p, .40, 8)


@art("ddr4_dimm")
def _(p):
    _dimm(p, .47, 8, ddr4=True)


@art("ddr5_dimm")
def _(p):
    _dimm(p, .5, 10, ddr5=True)


# ============================================================================================================== slots
def _slot(p, length, key, y=430, h=140, x=None, latch=(True, True), segments=None, tint="dark", ribs=True):
    x = x if x is not None else (1000 - length) / 2
    p.box(x, y, length, h, 10, tint)
    p.rect(x + 24, y + 50, length - 48, h - 100, 4, MED, "paper")       # the card channel
    if ribs:
        k = x + 34
        while k < x + length - 34:
            p.line(k, y + 54, k, y + h - 54, FINE)
            k += 14
    for kx in ([key] if isinstance(key, float) else key or []):
        p.fillrect(x + length * kx - 10, y + 40, 20, h - 80)
    if latch[0]:
        p.rect(x - 60, y - 20, 60, h + 40, 14, MED, "plastic")
        p.line(x - 40, y + 10, x - 40, y + h - 10, FINE)
    if latch[1]:
        p.rect(x + length, y - 20, 60, h + 40, 14, MED, "plastic")
        p.line(x + length + 40, y + 10, x + length + 40, y + h - 10, FINE)
    return x


@art("ddr3_dimm_slot")
def _(p):
    _slot(p, 760, .40, tint="blue")


@art("ddr4_dimm_slot")
def _(p):
    _slot(p, 760, .47, tint="dark")


@art("ddr5_dimm_slot")
def _(p):
    _slot(p, 780, .50, latch=(False, True), tint="dark")
    p.rect(110, 400, 30, 200, 6, MED)                         # fixed end on DDR5 single-latch slots


@art("pcie_x1_slot")
def _(p):
    _slot(p, 420, .30, y=390, h=220, latch=(False, False))


@art("pcie_x16_slot")
def _(p):
    x = _slot(p, 820, .13, latch=(False, True))
    p.rect(x + 820, 410, 70, 180, 10, MED, "plastic")


@art("isa_slot")
def _(p):
    _slot(p, 560, [], x=80, latch=(False, False))
    _slot(p, 230, [], x=680, latch=(False, False))


@art("pci_slot")
def _(p):
    _slot(p, 640, .81, latch=(False, False), tint="paper")


@art("agp_slot")
def _(p):
    x = _slot(p, 560, [.27, .58], x=260, latch=(False, False), tint="plastic")
    p.rect(x + 560, 400, 50, 200, 10, MED, "plastic")          # the retention tab


# ============================================================================================================ sockets
@art("m2_socket")
def _(p):
    p.box(120, 380, 300, 240, 10, "dark")
    p.rect(150, 450, 240, 100, 4, MED, "paper")
    k = 160
    while k < 380:
        p.line(k, 460, k, 540, FINE)
        k += 12
    p.fillrect(320, 440, 22, 120)                             # the M key
    p.dashed(420, 500, 760, 500, FINE)
    p.circle(820, 500, 70, HEAVY, "metal")                   # standoff
    p.circle(820, 500, 30, MED)
    p.line(420, 500, 440, 500, MED)


@art("cpu_socket")
def _(p):
    p.box(160, 160, 600, 680, 10, "metal")                   # load plate frame
    p.rect(250, 260, 420, 480, 6, HEAVY, "dark")
    for i in range(14):
        for j in range(16):
            if 4 <= i <= 9 and 5 <= j <= 10:
                continue
            p.dot(275 + i * 28, 285 + j * 28, 5)
    p.rect(390, 420, 140, 160, 4, FINE)
    p.line(820, 200, 820, 840, HEAVY)                          # the lever
    p.path([(820, 840), (760, 870), (700, 870)], HEAVY)
    p.circle(820, 200, 26, MED)
    for x, y in ((200, 200), (720, 200), (200, 800), (720, 800)):
        p.circle(x, y, 18, FINE)


# ============================================================================================================ storage
@art("nvme_ssd")
def _(p):
    p.box(80, 360, 840, 280, 8, "pcb")
    p.arc(920, 500, 36, 90, 270, HEAVY)                       # half-moon screw notch
    p.gold_fingers(100, 410, 12, 14, 9, 180, notch=None)
    p.fillrect(225, 410, 18, 180)                              # M key
    p.gold_fingers(250, 410, 4, 14, 9, 180)
    p.rect(330, 410, 140, 140, 6, MED, "silicon")            # controller
    p.circle(345, 425, 6, FINE)
    for x in (520, 700):
        p.rect(x, 395, 150, 210, 6, MED, "silicon")          # NAND
    p.rect(330, 570, 90, 40, 4, FINE, "silicon")


@art("sata_ssd")
def _(p):
    p.box(150, 120, 700, 760, 24, "metal")
    for x, y in ((200, 240), (800, 240), (200, 760), (800, 760)):
        p.circle(x, y, 18, MED)
    p.rect(260, 180, 480, 560, 16, FINE)
    p.rect(260, 870, 240, 40, 4, MED, "dark")                # SATA data
    p.rect(540, 870, 200, 40, 4, MED, "dark")                # SATA power
    p.line(300, 360, 700, 360, FINE)
    p.line(300, 400, 600, 400, FINE)


@art("hdd")
def _(p):
    p.box(170, 80, 660, 840, 30, "metal")
    p.circle(500, 400, 270, HEAVY, "glass")
    p.circle(500, 400, 80, MED)
    p.circle(500, 400, 40, FINE)
    for a in range(0, 360, 60):
        r = math.radians(a)
        p.circle(500 + 60 * math.cos(r), 400 + 60 * math.sin(r), 6, FINE)
    p.circle(700, 720, 70, MED)                                # actuator pivot
    p.path([(700, 720), (600, 560), (470, 430)], HEAVY)        # arm to the head
    p.rect(620, 760, 150, 110, 12, MED, "dark")              # voice coil
    for x, y in ((210, 120), (790, 120), (210, 880), (790, 880), (500, 880)):
        p.circle(x, y, 16, FINE)


# ========================================================================================================= connectors
def _shell(p, pts, t=HEAVY, tint="metal"):
    p.shape(pts, t, tint)


@art("sata_connector")
def _(p):
    p.shape([(160, 360), (840, 360), (840, 640), (240, 640), (240, 560), (160, 560)], HEAVY, "dark")
    p.shape([(200, 420), (800, 420), (800, 580), (280, 580), (280, 500), (200, 500)], MED, "paper")
    for k in range(7):
        p.rect(320 + k * 66, 440, 36, 60, 3, FINE, "gold")


@art("usb_a")
def _(p):
    p.box(160, 300, 680, 400, 16, "metal")
    p.rect(200, 340, 600, 320, 8, MED)
    p.rect(240, 380, 520, 120, 6, MED, "plastic")           # the tongue
    for k in range(4):
        p.rect(290 + k * 120, 470, 60, 26, 3, FINE, "gold")
    for x in (300, 700):
        p.rect(x - 30, 560, 60, 40, 4, FINE)                  # retention dimples


@art("usb_c")
def _(p):
    p.box(150, 360, 700, 280, 140, "metal")
    p.rect(190, 400, 620, 200, 100, MED)
    p.rect(300, 470, 400, 60, 10, MED, "plastic")
    for k in range(12):
        p.rect(318 + k * 31, 478, 16, 18, 2, FINE, "gold")
        p.rect(318 + k * 31, 504, 16, 18, 2, FINE, "gold")


@art("hdmi")
def _(p):
    p.shape([(150, 340), (850, 340), (850, 560), (760, 660), (240, 660), (150, 560)], HEAVY, "metal")
    p.shape([(195, 380), (805, 380), (805, 545), (735, 620), (265, 620), (195, 545)], MED)
    p.rect(260, 440, 480, 70, 6, MED, "plastic")
    for k in range(10):
        p.rect(272 + k * 46, 450, 22, 20, 2, FINE, "gold")
        p.rect(295 + k * 46, 484, 22, 20, 2, FINE, "gold")


@art("displayport")
def _(p):
    p.shape([(150, 340), (850, 340), (850, 660), (230, 660), (150, 580)], HEAVY, "metal")
    p.shape([(195, 380), (805, 380), (805, 620), (250, 620), (195, 565)], MED)
    p.rect(260, 450, 480, 70, 6, MED, "plastic")
    for k in range(10):
        p.rect(272 + k * 46, 460, 22, 20, 2, FINE, "gold")
        p.rect(295 + k * 46, 494, 22, 20, 2, FINE, "gold")


@art("rj45")
def _(p):
    p.box(200, 200, 600, 640, 14, "metal")
    p.shape([(270, 300), (730, 300), (730, 640), (580, 640), (580, 720), (420, 720), (420, 640), (270, 640)], MED, "dark")
    for k in range(8):
        p.line(312 + k * 54, 310, 312 + k * 54, 420, FINE)
        p.dot(312 + k * 54, 420, 8)
    p.rect(230, 760, 90, 50, 6, MED, "blue")                 # link / activity LEDs
    p.rect(680, 760, 90, 50, 6, MED, "gold")


@art("audio_jack_35mm")
def _(p):
    p.box(220, 220, 560, 560, 30, "dark")
    p.circle(500, 500, 200, HEAVY, "metal")                  # the threaded nut
    for a in range(0, 360, 20):
        r = math.radians(a)
        p.line(500 + 165 * math.cos(r), 500 + 165 * math.sin(r), 500 + 200 * math.cos(r), 500 + 200 * math.sin(r), FINE)
    p.circle(500, 500, 110, MED)
    p.dot(500, 500, 60)


def _molex(p, cols, rows=2, latch="top", gap=None):
    pitch = 600 / cols
    w = pitch * cols + 40
    x0 = (1000 - w) / 2
    y0 = 500 - (rows * 120 + 40) / 2
    p.box(x0, y0, w, rows * 120 + 40, 12, "plastic")
    for i in range(cols):
        for j in range(rows):
            x = x0 + 20 + i * pitch + (12 if gap is not None and i >= gap else 0)
            y = y0 + 20 + j * 120
            square = (i + j) % 2 == 0
            if square:
                p.rect(x + 6, y + 10, pitch - 12, 100, 6, MED, "paper")
            else:
                p.shape([(x + 6, y + 40), (x + pitch / 2, y + 10), (x + pitch - 6, y + 40), (x + pitch - 6, y + 110), (x + 6, y + 110)], MED, "paper")
            p.circle(x + pitch / 2, y + 66, 12, FINE)
    lx = 500 - 50
    ly = y0 - 70 if latch == "top" else y0 + rows * 120 + 40
    p.rect(lx, ly, 100, 70, 8, MED, "plastic")
    p.line(lx + 20, ly + 35, lx + 80, ly + 35, FINE)


@art("atx_24pin")
def _(p):
    _molex(p, 12)


@art("cpu_power_8pin")
def _(p):
    _molex(p, 4)


@art("pcie_power_8pin")
def _(p):
    _molex(p, 4, latch="bottom", gap=3)                       # 6+2: the last column is a separate block


@art("ide_connector")
def _(p):
    p.box(90, 360, 820, 280, 8, "dark")
    p.fillrect(460, 620, 80, 20)                              # key slot
    for i in range(20):
        for j in range(2):
            if i == 9 and j == 1:
                continue                                       # pin 20: removed, keyed
            p.dot(140 + i * 38, 450 + j * 100, 11)
    p.rect(120, 410, 760, 180, 4, FINE)


@art("scsi_connector")
def _(p):
    p.shape([(140, 330), (860, 330), (800, 670), (200, 670)], HEAVY, "metal")
    p.shape([(200, 380), (800, 380), (755, 620), (245, 620)], MED, "dark")
    for k in range(25):
        p.dot(230 + k * 22.5, 450, 6)
        p.dot(255 + k * 20.5, 545, 6)
    for x in (80, 920):
        p.circle(x, 500, 40, MED, "metal")


@art("vga")
def _(p):
    p.shape([(180, 330), (820, 330), (760, 670), (240, 670)], HEAVY, "metal")
    p.shape([(230, 375), (770, 375), (720, 625), (280, 625)], MED, "dark")
    for row, (n, x0, step) in enumerate(((5, 330, 85), (5, 350, 75), (5, 330, 85))):
        for k in range(n):
            p.circle(x0 + k * step, 430 + row * 70, 14, FINE)
    for x in (100, 900):
        p.circle(x, 500, 48, MED, "metal")
        p.circle(x, 500, 18, FINE)


@art("ps2")
def _(p):
    p.circle(500, 500, 320, HEAVY, "metal")
    p.circle(500, 500, 260, MED, "dark")
    p.fillrect(470, 240, 60, 90)                              # the key
    for a in (150, 210, 120, 240, 60, 300):
        r = math.radians(a + 90)
        p.circle(500 + 150 * math.cos(r), 500 + 150 * math.sin(r), 22, MED, "gold")
    p.rect(450, 640, 100, 60, 6, MED)


# ============================================================================================================ cooling
@art("fan")
def _(p):
    p.box(110, 110, 780, 780, 70, "dark")
    p.circle(500, 500, 360, MED)
    for x, y in ((170, 170), (830, 170), (170, 830), (830, 830)):
        p.circle(x, y, 30, MED)
    p.circle(500, 500, 110, HEAVY, "metal")
    for k in range(7):
        a0 = 2 * math.pi * k / 7
        pts = []
        for i in range(9):
            t = i / 8
            r = 110 + 240 * t
            a = a0 + 0.9 * t
            pts.append((500 + r * math.cos(a), 500 + r * math.sin(a)))
        for i in range(8, -1, -1):
            t = i / 8
            r = 110 + 240 * t
            a = a0 + 0.9 * t + 0.42 - 0.2 * t
            pts.append((500 + r * math.cos(a), 500 + r * math.sin(a)))
        p.shape(pts, MED, "plastic")
    p.circle(500, 500, 40, FINE)


@art("heatsink")
def _(p):
    p.box(120, 230, 760, 540, 6, "metal")
    for x in range(150, 860, 30):
        p.line(x, 250, x, 750, FINE)                           # fins, seen from above
    for y in (360, 500, 640):
        p.rect(100, y - 26, 800, 52, 26, MED, "copper")      # heat pipes
    p.rect(380, 300, 240, 400, 8, HEAVY)                       # the base block (hidden line would hide the fins)


# ===================================================================================================== expansion cards
def _card(p, ports=None):
    p.box(160, 230, 700, 430, 12, "pcb")
    p.gold_fingers(330, 620, 9, 14, 9, 70)
    p.fillrect(468, 620, 14, 80)
    p.rect(110, 160, 60, 600, 4, HEAVY, "metal")              # the bracket
    p.line(110, 160, 60, 160, HEAVY)
    return p


@art("wifi_nic")
def _(p):
    _card(p)
    for y in (300, 520):
        p.rect(60, y, 60, 80, 6, MED, "gold")                  # RP-SMA jacks
        p.line(60, y + 40, 20, y + 40, MED)
    p.rect(420, 300, 300, 230, 8, HEAVY, "metal")            # RF shield can
    for x in range(440, 710, 30):
        p.circle(x, 320, 6, FINE)
    for y in (330, 550):
        p.line(170, y, 410, y, FINE)


@art("ethernet_nic")
def _(p):
    _card(p)
    p.rect(170, 300, 160, 170, 8, MED, "metal")               # the RJ45, through the bracket
    p.rect(200, 340, 100, 90, 4, FINE)
    p.rect(400, 300, 150, 150, 6, MED, "silicon")            # controller
    p.circle(415, 315, 6, FINE)
    p.rect(600, 300, 180, 90, 6, MED, "dark")                # magnetics
    for k in range(4):
        p.rect(600 + k * 45, 470, 30, 40, 4, FINE, "metal")


# ========================================================================================================== networking
@art("router")
def _(p):
    p.box(120, 470, 760, 260, 30, "plastic")
    for x in (240, 500, 760):
        p.line(x, 470, x, 120, HEAVY)                          # antennas
        p.rect(x - 22, 420, 44, 50, 8, MED, "dark")
        for y in (180, 240, 300):
            p.line(x - 10, y, x + 10, y, FINE)
    for k in range(6):
        p.circle(230 + k * 60, 620, 14, MED)
    for k in range(4):
        p.rect(600 + k * 60, 590, 44, 60, 4, FINE, "dark")


@art("switch")
def _(p):
    p.box(70, 350, 860, 300, 12, "metal")
    for k in range(8):
        x = 160 + k * 90
        p.shape([(x, 430), (x + 70, 430), (x + 70, 520), (x + 50, 520), (x + 50, 540), (x + 20, 540), (x + 20, 520), (x, 520)], MED, "dark")
        p.circle(x + 15, 580, 8, FINE)
        p.circle(x + 55, 580, 8, FINE)
    p.circle(110, 400, 14, MED)


@art("antenna")
def _(p):
    p.rect(420, 760, 160, 120, 10, HEAVY, "gold")            # SMA nut
    for x in (440, 480, 520, 560):
        p.line(x, 770, x, 870, FINE)
    p.rect(450, 680, 100, 80, 10, MED, "metal")              # the hinge
    p.circle(500, 720, 22, FINE)
    p.shape([(460, 680), (540, 680), (525, 120), (500, 90), (475, 120)], HEAVY, "dark")
    for y in range(200, 640, 60):
        p.line(470, y, 530, y, FINE)


# ============================================================================================================== power
@art("atx_psu")
def _(p):
    p.box(80, 200, 840, 600, 12, "metal")
    p.circle(330, 500, 230, HEAVY)
    for r in (70, 130, 190):
        p.circle(330, 500, r, FINE)
    for a in range(0, 360, 45):
        rr = math.radians(a)
        p.line(330 + 30 * math.cos(rr), 500 + 30 * math.sin(rr), 330 + 225 * math.cos(rr), 500 + 225 * math.sin(rr), FINE)
    p.shape([(640, 300), (820, 300), (820, 400), (790, 430), (670, 430), (640, 400)], MED, "dark")   # IEC C14
    for x in (690, 730, 770):
        p.rect(x - 8, 340, 16, 50, 2, FINE, "metal")
    p.rect(680, 500, 100, 140, 8, MED, "dark")                # rocker switch
    p.line(690, 570, 770, 570, FINE)
    for x, y in ((120, 240), (880, 240), (120, 760), (880, 760)):
        p.circle(x, y, 18, MED)


@art("coin_cell_battery")
def _(p):
    p.circle(500, 520, 300, HEAVY, "metal")
    p.circle(500, 520, 260, FINE)
    p.line(500, 420, 500, 620, HEAVY)
    p.line(400, 520, 600, 520, HEAVY)
    p.shape([(380, 180), (620, 180), (650, 260), (350, 260)], MED, "metal")    # the holder's spring clip
    p.line(500, 180, 500, 120, MED)


@art("vrm")
def _(p):
    p.box(110, 200, 780, 600, 10, "pcb")
    for k in range(4):
        x = 170 + k * 180
        p.rect(x, 250, 140, 140, 8, MED, "dark")              # chokes
        p.circle(x + 70, 320, 34, FINE)
        p.rect(x + 10, 430, 120, 90, 6, MED, "silicon")       # power stage
        p.circle(x + 40, 650, 40, MED, "metal")               # output caps
        p.circle(x + 105, 650, 40, MED, "metal")
        p.line(x + 70, 390, x + 70, 430, FINE)


# ============================================================================================== protocols (as diagrams)
def _wave(p, y, bits, x0=140, step=60, h=70, t=MED):
    pts = [(x0, y + (0 if bits[0] else h))]
    for i, b in enumerate(bits):
        yy = y + (0 if b else h)
        pts.append((x0 + i * step, yy))
        pts.append((x0 + (i + 1) * step, yy))
    p.path(pts, t)


@art("usb_protocol")
def _(p):
    bits = [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1]
    _wave(p, 300, bits)                                        # D+
    _wave(p, 470, [1 - b for b in bits])                       # D-: the mirror
    p.rect(140, 640, 240, 110, 10, MED, "blue")              # SYNC | PID | DATA | CRC
    p.rect(380, 640, 120, 110, 10, MED)
    p.rect(500, 640, 240, 110, 10, MED, "paper")
    p.rect(740, 640, 120, 110, 10, MED)
    p.line(140, 260, 860, 260, FINE)


@art("pcie_protocol")
def _(p):
    p.box(110, 220, 170, 560, 12, "silicon")
    p.box(720, 220, 170, 560, 12, "silicon")
    for k in range(4):
        y = 280 + k * 125
        p.arrow(290, y, 710, y, MED, 28)                       # TX
        p.arrow(710, y + 45, 290, y + 45, FINE, 22)           # RX
    p.dashed(500, 230, 500, 790, FINE)


@art("nvme_protocol")
def _(p):
    for x0, tint in ((170, "blue"), (560, "paper")):           # submission and completion queues: rings
        p.circle(x0 + 135, 470, 170, HEAVY, tint)
        p.circle(x0 + 135, 470, 90, MED)
        for k in range(12):
            a = 2 * math.pi * k / 12
            p.line(x0 + 135 + 90 * math.cos(a), 470 + 90 * math.sin(a), x0 + 135 + 170 * math.cos(a), 470 + 170 * math.sin(a), FINE)
    p.arrow(440, 360, 560, 360, MED)
    p.arrow(560, 580, 440, 580, MED)
    p.rect(330, 720, 340, 90, 10, MED)                         # the doorbell
    p.dot(500, 765, 22)


@art("sata_protocol")
def _(p):
    p.box(110, 300, 160, 400, 12, "dark")
    p.box(730, 300, 160, 400, 12, "dark")
    for y, d in ((420, 1), (580, -1)):
        for off in (-18, 18):
            p.line(270, y + off, 730, y + off, MED)
        p.arrow(420 if d > 0 else 580, y, 580 if d > 0 else 420, y, FINE, 26)
    for x in (300, 700):
        p.rect(x - 10, 380, 20, 240, 4, FINE)


# ======================================================================================== architectures (as floorplans)
@art("x86_64")
def _(p):
    p.box(140, 140, 720, 720, 10, "silicon")
    for i in range(2):
        for j in range(2):
            p.rect(190 + i * 330, 190 + j * 240, 290, 200, 6, MED, "paper")   # four big cores
            p.hatch(200 + i * 330, 200 + j * 240, 90, 180, 20, 45)
    p.rect(190, 680, 620, 130, 6, MED, "metal")               # shared L3
    for k in range(1, 12):
        p.line(190 + k * 52, 690, 190 + k * 52, 800, FINE)


@art("arm64")
def _(p):
    p.box(140, 140, 720, 720, 10, "silicon")
    for i in range(2):
        p.rect(190 + i * 200, 190, 170, 260, 6, MED, "paper")             # big cores
    for i in range(2):
        for j in range(2):
            p.rect(620 + i * 100, 190 + j * 130, 80, 110, 6, MED)         # LITTLE cores
    p.rect(190, 500, 620, 120, 6, MED, "metal")               # cluster cache
    p.rect(190, 660, 300, 150, 6, MED, "blue")                # GPU
    p.rect(520, 660, 290, 150, 6, MED)                         # NPU / ISP
    p.hatch(530, 670, 270, 130, 24, 135)


@art("riscv")
def _(p):
    for k, label_h in enumerate((0, 1, 2, 3, 4)):              # the classic five-stage pipeline
        x = 90 + k * 170
        p.rect(x, 380, 140, 240, 10, HEAVY if k == 2 else MED, "paper" if k != 2 else "blue")
        if k < 4:
            p.arrow(x + 140, 500, x + 170, 500, FINE, 16)
    p.path([(780, 620), (780, 760), (160, 760), (160, 620)], MED)   # writeback
    p.solid([(160, 620), (140, 660), (180, 660)])
    for k in range(5):
        p.line(110 + k * 170, 440, 210 + k * 170, 440, FINE)


# ============================================================================================================ cables
@art("usb_c_cable")
def _(p):
    p.rect(110, 440, 150, 120, 60, HEAVY, "metal")           # the plug
    p.rect(260, 400, 220, 200, 40, HEAVY, "plastic")         # overmold
    for x in range(300, 460, 30):
        p.line(x, 410, x, 590, FINE)
    pts = [(480, 500)]
    for i in range(1, 21):
        t = i / 20
        pts.append((480 + 400 * t, 500 + 260 * t * t))
    for off in (-22, 22):
        p.path([(x, y + off) for x, y in pts], MED)


@art("sata_cable")
def _(p):
    for x0, flip in ((90, 1), (690, -1)):
        p.shape([(x0, 300), (x0 + 220, 300), (x0 + 220, 470), (x0 + (60 if flip > 0 else 160), 470), (x0 + (60 if flip > 0 else 160), 420), (x0, 420)], HEAVY, "dark")
        for k in range(7):
            p.line(x0 + 30 + k * 26, 330, x0 + 30 + k * 26, 390, FINE)
    pts = [(200, 470), (200, 620), (500, 720), (800, 620), (800, 470)]
    for off in (-24, 24):
        p.path([(x + off, y) for x, y in pts], MED)


@art("ethernet_cable")
def _(p):
    p.box(120, 380, 330, 240, 12, "glass")                   # the clear plug
    for k in range(8):
        p.rect(150 + k * 36, 400, 20, 80, 3, FINE, "gold")
    p.shape([(220, 380), (380, 380), (330, 300), (250, 300)], MED, "glass")   # latch
    p.rect(450, 410, 160, 180, 40, HEAVY, "blue")             # strain-relief boot
    pts = [(610, 500)]
    for i in range(1, 15):
        t = i / 14
        pts.append((610 + 290 * t, 500 + 240 * t * t))
    for off in (-24, 24):
        p.path([(x, y + off) for x, y in pts], MED)


# ============================================================================================================== media
@art("sd_card")
def _(p):
    p.shape([(220, 100), (680, 100), (800, 220), (800, 900), (220, 900)], HEAVY, "blue")
    for k in range(8):
        p.rect(280 + k * 58, 140, 40, 120, 4, MED, "gold")
    p.rect(195, 420, 40, 160, 6, MED, "paper")               # write-protect slider
    p.line(195, 500, 235, 500, FINE)
    p.rect(300, 360, 420, 460, 16, FINE)                       # label area
