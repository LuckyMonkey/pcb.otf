# PCB.OTF art direction

The 0.1.0 artwork is a deliberately compact vector vocabulary. It proves the
object → identity → relation → glyph pipeline, but it is not yet a collection
of canonical mechanical illustrations. The silhouettes are closer to a
technical icon set than to a patent plate or a service-manual drawing.

That distinction is intentional and should remain visible in project language.
Do not describe the current masters as manufacturer-accurate drawings.

## Drawing target

The next artwork pass should feel like an open technical archive assembled from
the visual language of:

- patent plates and public-domain technical drawings;
- IBM, Tektronix, and service-manual diagrams;
- component datasheet package drawings;
- PCB silkscreen and assembly documentation;
- standards diagrams where the geometry is publicly documented.

The result should be original vector artwork, not a copied scan or vendor logo.
Each object should have a stable drawing grammar:

- top view for footprint, keying, contacts, holes, and pin arrangement;
- front/side profile where height or insertion geometry matters;
- angled/isometric view for assembled depth and physical relationships;
- section or knockout detail where a cavity, notch, pad, via, or layer matters;
- monochrome linework that remains legible without color.

## Priority order

### Pass 1: PCB-native vocabulary

Finish the board as an object before expanding the computer catalog:

1. substrate, copper layers, solder mask, silkscreen, traces, differential pairs;
2. pads, annular rings, vias, plated holes, test points, fiducials, mounting holes;
3. footprints, thermal pads, BGA fields, edge connectors, castellated holes;
4. passive footprints and package families with real pin/contact geometry;
5. internal headers, power connectors, fan headers, and board-level sockets.

### Pass 2: components and interfaces

Redraw passives, semiconductors, packages, connectors, ports, slots, and cables
as orthographic technical plates. Preserve distinctions such as USB-C connector
versus USB protocol, M.2 socket versus NVMe, and PCIe slot width versus protocol.

### Pass 3: computer assemblies

Only after the PCB vocabulary is strong, add larger hardware objects:

- generic logic boards and motherboard families;
- standard-era board layouts such as B75 and Z97, represented generically and
  without vendor marks;
- disc drives with top, front, and side profiles;
- server chassis, racks, backplanes, power supplies, and cooling assemblies;
- historical boards and peripherals.

Specific board models should be separate semantic objects or metadata packs. They
must not replace the durable generic objects in the base font.

## Source and provenance rule

Use public technical references for geometry and terminology, then redraw the
artwork as clean deterministic SVG. Record the source in `ontology/sources.yaml`
and the object’s `provenance` field. Wikipedia may guide discovery, but the final
geometry should be checked against a datasheet, standard, open-hardware file, or
historical manual whenever one is available.

The project must not reproduce proprietary vendor illustrations, certification
marks, or logos. A drawing can be technically recognizable without being a copy.

## Current status

PCB.OTF 0.1.0 has the complete semantic vertical slice and a broad starter
registry. Its artwork should be treated as prototype symbol masters. Future
releases should improve the vector plates in place while keeping object IDs,
shortcodes, and released PUA assignments stable.
