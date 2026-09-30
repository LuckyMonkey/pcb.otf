# Contributing 🛠️

The canonical object is an entry in `ontology/hardware.yaml`; a glyph is only one
renderer of it. Add the object, attributes, relation edges, and provenance first,
then add or revise the deterministic vector design. Never recycle a released PUA
codepoint. Keep connector, protocol, socket, device, and package identities
separate.

Run `make test` before opening a change. The build needs Python 3, the packages in
`requirements.txt`, and either `rsvg-convert` or ImageMagick (`magick`/`convert`)
for PNG previews. GitHub CI installs the rasterizers automatically.

Generated files are refreshed by the build rather than edited by hand. Relation
validation must remain zero-dangling; if a specification is uncertain, set
`review_required: true` and cite a source instead of inventing compatibility.
