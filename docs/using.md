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
```

The isometric master is a deterministic geometric view of the same canonical
object, not a second identity. Applications can use either renderer in diagrams,
cards, or hardware assemblies. 📐

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
