# Accessibility ♿

PUA characters are not self-describing. Do not expose a bare PCB character as
the only accessible content.

```html
<span class="pcb" role="img" aria-label="USB Type-C connector">:usb_c:</span>
```

The semantic shortcode remains readable when the font is missing. For direct PUA
output, keep the canonical object label in `aria-label` and avoid presenting a
screen reader with “Private Use Character E141.”

Color is never the only distinction: connector geometry, technical metadata, and
monochrome vector outlines remain available. The specimen's top-down and
isometric views use empty `alt` text inside a labeled assembly because the page
already supplies the semantic group description.
