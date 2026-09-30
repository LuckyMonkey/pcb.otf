# Release checklist 🚀

- [ ] Review `review_required: true` objects with sourced hardware references.
- [ ] Run `make clean && make test` from a clean checkout.
- [ ] Verify two clean font builds are byte-identical where tooling permits.
- [ ] Test shortcode shaping and PUA output in Chromium and Firefox.
- [ ] Test top-down and isometric previews on mobile and dark backgrounds.
- [ ] Test screen-reader labels and missing-font shortcode fallback.
- [ ] Confirm compatibility examples do not overclaim vendor support.
- [ ] Update `project.yaml`, `CHANGELOG.md`, and `CITATION.cff` together.
- [ ] Tag `v1.0.0` only after object IDs and PUA assignments are frozen.

After 1.0, released object IDs and codepoint/object pairs are append-only. Labels,
aliases, and glyph geometry may improve, but a released PUA codepoint must never
be reused for another hardware object. 🔒
