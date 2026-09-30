#!/usr/bin/env python3
"""Create a clean public release archive without developer state."""

from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

import yaml


ROOT = Path(__file__).resolve().parents[1]


def project_version() -> str:
    return str(yaml.safe_load((ROOT / "project.yaml").read_text())["version"])


def main() -> int:
    version = project_version()
    release_dir = ROOT / "release"
    release_dir.mkdir(exist_ok=True)
    archive = release_dir / f"PCB.OTF-{version}.zip"
    if archive.exists():
        archive.unlink()

    include = [
        "README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md", "SECURITY.md", "CITATION.cff", "Makefile",
        "project.yaml", "requirements.txt", "demo.html",
        "ontology", "registry", "assemblies", "glyphs/mono", "glyphs/color", "glyphs/iso", "glyphs/technical",
        "packages/js", "scripts", "docs", "unicode-proposal", "dist",
    ]
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for relative in include:
            source = ROOT / relative
            paths = [source] if source.is_file() else sorted(path for path in source.rglob("*") if path.is_file())
            for path in paths:
                if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
                    continue
                if path.suffix in {".pyc", ".log"}:
                    continue
                bundle.write(path, Path("PCB.OTF") / version / path.relative_to(ROOT))
    print(f"wrote {archive} ({archive.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
