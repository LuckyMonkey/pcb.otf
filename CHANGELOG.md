# Changelog

## Unreleased

- **Glyph art overhaul: one patent-style drawing per object, at full detail.** Every one of the 104 objects now has
  its own original line drawing (scripts/patent_art.py) instead of a few shared generic shapes - the CPU, GPU,
  chipset, FPGA, microcontroller and memory chips used to be the same "square with a dot", and the mono font was
  solid silhouettes. Drawings follow how each thing is recognised: boards, slots and packages from above,
  connectors by their mating face, components read by profile (LED, capacitor can, DIMM) from the side.
- One drawing language: heavy outline, medium parts, fine hatching (the patent-plate convention for cut surfaces).
  scripts/patent_pen.py draws every line as a filled outline with a known winding, so the same art is the SVG, the
  mono font's outline glyph and the color font's layers - holes stay holes in browsers, TrueType and CFF.
- The color font is the same line art with muted plate tints under the ink.
- The ATX assembly plates keep their four constructed views (scripts/technical_art.py); every other object's
  technical plate is now its patent drawing.
- tests/test_art.py: every object has a drawing, no two objects draw alike, mono glyphs are one-ink line art.

- Reframed the ATX assembly canvas around the real board bounds so the board and
  attached parts read at a useful scale instead of floating in excess whitespace.
- Fixed front and side assembly views so their orthographic technical drawings are
  not projected a second time by CSS 3D transforms.
- Increased default X-ray legibility, quieted route labels, separated layer toggles
  into their own control row, and made the inspector responsive before it can clip.
- Added the generic ATX desktop assembly with 31 semantic layers, technical
  top/front/side/isometric masters, X-ray opacity, exploded mode, and object
  inspection.
- Added three append-only hardware objects: ATX motherboard, CPU socket, and VRM.
- Initial PCB.OTF vertical slice now contains 104 semantic hardware objects, 17 ontology
  groups, 39 typed relations, 728 deterministic SVG masters, mono/color fonts,
  PUA mappings, shortcode ligatures, metadata APIs, PNG exports, and a dual-view
  specimen website.
- Documented the next art direction: PCB-native technical plates first, larger
  computer assemblies afterward.
- Added the illustrated parts-catalog specimen: patent-sheet drawing plates,
  full-registry technical SVG fallbacks, and a semantic ligature/PUA font specimen.
- Kept compact filled font masters separate from the outlined technical catalog
  renderer so the catalog can become more detailed without making the font noisy.
- Fixed the webfont CSS newline bug so browser `@font-face` and `liga` shaping
  rules parse correctly; HarfBuzz and browser assets now agree on shortcode output.
- Made isometric the default assembly view with a CSS 3D plane, coherent image
  sizing, eight validated connection routes, and exploded Z-depth.

## 0.1.0 - 2026-09-30

- Established the independent hardware symbol system and append-only U+E100 range.
