# Using PCB.OTF 🧩

PCB uses semantic text as the portable interface:

```text
🧩 Install the :usb_c: connector.
💾 Put the :ddr4_dimm: in the :ddr4_dimm_slot:.
🕰️ Keep the :isa_slot: in a retro-computing diagram.
```

Without PCB.OTF, the colon-delimited names remain readable. With the font's
`liga` feature, the names shape into hardware glyphs. The ordinary emoji are
standard Unicode examples; PCB symbols are emoji-like renderings, not official
Unicode emoji or USB/PCI-SIG certification marks.

## Webfont

```html
<link rel="stylesheet" href="dist/pcb.css">
<span class="pcb" role="img" aria-label="USB Type-C connector">:usb_c:</span>
```

The direct PUA character is available for applications that need one character:

```html
<span class="pcb-emoji" role="img" aria-label="PCI Express x16 slot">&#xE13A;</span>
```

Keep the semantic shortcode or an explicit accessible label. A screen reader
cannot infer that a project-assigned `U+E13A` means “PCI Express x16 slot.” ♿

## Top-down and isometric SVGs

Every registry record points to a monochrome SVG, a color/top-down SVG, and an
angled/isometric SVG:

```js
import { get } from "pcb-otf";

const usb = get("hardware:usb_c");
usb.svg;       // monochrome vector
usb.color_svg; // top-down/color vector
usb.iso_svg;   // angled/isometric vector
usb.technical_top_svg;
usb.technical_front_svg;
usb.technical_side_svg;
usb.technical_iso_svg;
```

The isometric master is a deterministic geometric view of the same canonical
object, not a second identity. Applications can use either renderer in diagrams,
cards, or hardware assemblies. 📐

## Layered assemblies

Assemblies are compositions of canonical objects, not new Unicode identities:

```js
import { assembly, instances } from "pcb-otf";

const scene = assembly("assembly:generic_atx_desktop");
const parts = instances("assembly:generic_atx_desktop");
```

The specimen renderer layers technical SVG views with explicit position, scale,
z-order, opacity, and exploded offsets. Isometric is the default: a CSS 3D
plane rotates the same registry-backed parts together, while assembly-level
route overlays show power, memory, storage, and cooling connections. The same
scene can render as a top-down plate, front/side profile, or isometric X-ray
view. Use the font for compact symbols and labels; use technical SVG masters
when physical detail matters. 🧰

## Graph API

```js
import { compatibleWith, connectionsFor, get, search } from "pcb-otf";

get("hardware:m2_socket");
search("memory_generation");
compatibleWith("hardware:ddr3_dimm");
connectionsFor("hardware:usb_c");
```

Compatibility is explicit graph data. PCB does not infer that every M.2 device is
NVMe or that socket identity alone guarantees CPU support. 🔌

## Build locally

```sh
make install   # once
make test      # build fonts, previews, site, and tests
make site      # write _site/ for static deployment
```
