#!/usr/bin/env python3
"""Write the PCB webfont CSS package and synchronized specimen version."""

import re
import shutil
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    css = """@font-face {\n  font-family: \"PCB\";\n  src: url(\"./PCB.woff2\") format(\"woff2\");\n  font-weight: 400;\n  font-style: normal;\n  font-display: swap;\n}\n@font-face {\n  font-family: \"PCB Color\";\n  src: url(\"./PCB-Color.woff2\") format(\"woff2\");\n  font-weight: 400;\n  font-style: normal;\n  font-display: swap;\n}\n.pcb { font-family: \"PCB\", sans-serif; font-variant-ligatures: common-ligatures; }\n.pcb-emoji { font-family: \"PCB Color\", \"PCB\", sans-serif; font-variant-ligatures: common-ligatures; }\n"""
    css = css.replace(
        '.pcb { font-family: "PCB", sans-serif; font-variant-ligatures: common-ligatures; }\\n.pcb-emoji { font-family: "PCB Color", "PCB", sans-serif; font-variant-ligatures: common-ligatures; }\\n',
        '.pcb { font-family: "PCB", sans-serif; font-variant-ligatures: common-ligatures; font-feature-settings: "liga" 1; text-rendering: optimizeLegibility; }\\n.pcb-emoji { font-family: "PCB", "PCB Color", sans-serif; font-variant-ligatures: common-ligatures; font-feature-settings: "liga" 1; text-rendering: optimizeLegibility; }\\n.pcb-color { font-family: "PCB Color", "PCB", sans-serif; font-variant-ligatures: common-ligatures; font-feature-settings: "liga" 1; }\\n',
    )
    # The compact CSS template historically used escaped newlines. Normalize
    # them before writing so browsers parse @font-face and shaping rules.
    css = css.replace(chr(92) + "n", chr(10))
    css += chr(10) + '.pcb { font-feature-settings: "liga" 1; text-rendering: optimizeLegibility; }' + chr(10)
    css += '.pcb-emoji { font-family: "PCB", "PCB Color", sans-serif; font-feature-settings: "liga" 1; text-rendering: optimizeLegibility; }' + chr(10)
    css += '.pcb-color { font-family: "PCB Color", "PCB", sans-serif; font-feature-settings: "liga" 1; }' + chr(10)
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist/pcb.css").write_text(css, encoding="utf-8")
    assets = ROOT / "docs/assets"
    assets.mkdir(parents=True, exist_ok=True)
    for filename in ("PCB.woff2", "PCB-Color.woff2"):
        shutil.copy2(ROOT / "dist" / filename, assets / filename)
    assets.joinpath("pcb.css").write_text(css, encoding="utf-8")
    index = ROOT / "docs/index.html"
    text = index.read_text(encoding="utf-8")
    version = yaml.safe_load((ROOT / "project.yaml").read_text())["version"]
    text = re.sub(r"PCB\.OTF / [0-9]+\.[0-9]+\.[0-9]+", f"PCB.OTF / {version}", text)
    index.write_text(text, encoding="utf-8")
    print("wrote dist/pcb.css")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
