# Changelog

## Unreleased

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
