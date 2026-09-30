# PCB.OTF 🧩

[![Build](https://github.com/LuckyMonkey/pcb.otf/actions/workflows/ci.yml/badge.svg)](https://github.com/LuckyMonkey/pcb.otf/actions/workflows/ci.yml)
[![Pages](https://github.com/LuckyMonkey/pcb.otf/actions/workflows/pages.yml/badge.svg)](https://github.com/LuckyMonkey/pcb.otf/actions/workflows/pages.yml)
[![Live specimen](https://img.shields.io/badge/specimen-live-ad633d)](https://luckymonkey.github.io/pcb.otf/)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Fonts: OFL](https://img.shields.io/badge/fonts-OFL--1.1-d3a44c.svg)](font/OFL.txt)

PCB.OTF is an open semantic symbol system for computer hardware and electronics.

Computing hardware has rich physical and technical identity, but general-purpose
typography represents most of it poorly or not at all. PCB.OTF gives components,
ports, sockets, slots, PCB structures, memory types, storage interfaces, power,
cooling, networking, and historic hardware stable identities, Unicode-compatible
representations, semantic shortcodes, vector glyphs, and emoji-like rendering.

It is not Wingdings. Ordinary letters stay ordinary. A PCIe slot is not an icon;
it is a hardware object that happens to have a glyph. 🔌

## See it live 🚀

- **[Open the assembly demo](https://luckymonkey.github.io/pcb.otf/)** — top-down
  and angled/isometric computer views made from registry-backed objects.
- **[Search the full registry](https://luckymonkey.github.io/pcb.otf/docs/)** —
  inspect every object in both views, attributes, relation edges, and PUA mapping.
- **[Browse the source](https://github.com/LuckyMonkey/pcb.otf)** — independent
  from Fridge and suitable for downstream hardware graphs.

```text
🧩 A computer is an assembly of related hardware objects.
🔌 Install the :usb_c: connector.
💾 Put the :ddr4_dimm: in the :ddr4_dimm_slot:.
🕰️ Document the :isa_slot: beside the :pcie_x16_slot:.
```

The emoji above are ordinary Unicode examples. The colon-delimited tokens are
PCB semantic text; the font shapes them when selected. Without the font, the
source remains readable. PCB symbols are emoji-like renderings, not official
Unicode emoji or standards-body logos.

## MVP coverage

The initial vertical slice contains 104 canonical objects and 39 typed relation
edges across:

- passives and semiconductors;
- IC packages;
- PCB substrate, copper, traces, vias, pads, planes, footprints, and fiducials;
- motherboard, CPU, GPU, chipset, memory generations and DIMM slots;
- PCIe, ISA, PCI, AGP, M.2, SATA, IDE, and SCSI;
- USB-A, USB-C, HDMI, DisplayPort, VGA, PS/2, RJ45, audio, and power connectors;
- NVMe, SATA SSD, HDD, SD card, cables, power, cooling, networking, architectures,
  and historical hardware. The generic ATX assembly uses 31 layered object
  instances from the first computer-hardware plate.

The object model deliberately distinguishes connector geometry from protocol,
socket from device, memory generation from module form factor, and physical slot
width from negotiated electrical lanes. Compatibility claims remain explicit
relation data rather than guesses. 🔬

The 0.1.0 artwork is intentionally a prototype symbol vocabulary, not a set of
manufacturer-accurate or patent-plate illustrations. The next art pass starts
with PCB-native geometry—footprints, pads, vias, traces, packages, connectors,
and board features—using original orthographic and isometric vector drawings.
Larger computer assemblies such as B75/Z97-era boards, drives, and server racks
follow that foundation. See [`docs/art-direction.md`](docs/art-direction.md).

## Usage

```html
<link rel="stylesheet" href="./dist/pcb.css">

<span class="pcb" role="img" aria-label="USB Type-C connector">:usb_c:</span>
<span class="pcb-emoji" role="img" aria-label="PCI Express x16 slot">:pcie_x16_slot:</span>
```

The JavaScript helper exposes the registry and graph:

```js
import { get, search, compatibleWith, connectionsFor } from "pcb-otf";

get("hardware:usb_c");
search("DDR4");
compatibleWith("hardware:ddr3_dimm");
connectionsFor("hardware:m2_socket");
```

Read [`docs/using.md`](docs/using.md) for semantic fallback, accessibility,
top-down/isometric SVG use, and PUA copy behavior. ♿

## Build

```sh
make install   # once: creates .venv and installs open Python dependencies
make build     # validate, generate technical/fallback SVG masters, compile fonts, export PNGs
make test      # build the deployable site and run ontology/font/shaping/web tests
make site      # write the compact GitHub Pages artifact to _site/
make clean
```

The project version is authoritative in `project.yaml`. Build tools are open
source; no proprietary font application is required. PNG export needs either
`rsvg-convert` or ImageMagick. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Identity and Unicode

The hardware object is canonical. Its ID survives changes to labels, filenames,
glyph outlines, and language. `registry/codepoints.csv` is append-only after a
release. The current project-assigned PUA range is U+E100–U+E167; these are valid
Unicode code points but are not official Unicode Consortium hardware characters.
`unicode-proposal/` documents the future-standardization strategy.

## Artwork and licensing

PCB.OTF uses original deterministic SVG engineering drawings inspired by service
manuals, silkscreen conventions, catalogs, and datasheet geometry. It does not
copy vendor logos or certification marks. Source code, ontology, metadata, SVGs,
and docs are MIT; generated font artifacts are OFL-1.1. See `LICENSE` and
`font/OFL.txt`.

## Repository map 📚

- `ontology/` — hardware objects, source references, and typed relations.
- `registry/` — append-only PUA, shortcode, alias, and compatibility tables.
- `glyphs/` — mono, color/top-down, and angled/isometric SVG masters.
- `dist/` — PCB TTF/OTF/COLRv1/WOFF2 artifacts and CSS.
- `packages/js/` — generated metadata and graph helper API.
- `docs/` — searchable object registry and usage guidance.
- `.github/workflows/` — clean-runner CI and Pages deployment.

## Status

This is an independently usable 0.1.0 MVP, not a claim that every historical
package, connector, or vendor compatibility rule is complete. Objects marked
`review_required: true` need a sourced hardware review before 1.0. Stable object
IDs and released PUA assignments must not be casually recycled. 🛠️
