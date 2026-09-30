PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.PHONY: all build test validate site release clean install

all: build

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

validate:
	$(PYTHON) scripts/validate_ontology.py
	$(PYTHON) scripts/validate_relations.py
	$(PYTHON) scripts/generate_glyphs.py
	$(PYTHON) scripts/validate_glyphs.py
	$(PYTHON) scripts/validate_assemblies.py

build: validate
	$(PYTHON) scripts/generate_registry.py
	$(PYTHON) scripts/generate_assemblies.py
	$(PYTHON) scripts/build_font.py
	$(PYTHON) scripts/subset_webfonts.py
	$(PYTHON) scripts/validate_fonts.py
	$(PYTHON) scripts/export_png.py
	$(PYTHON) scripts/build_docs.py

site: build
	$(PYTHON) scripts/build_site.py

release: build
	$(PYTHON) scripts/build_release.py

test: site
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

clean:
	rm -rf dist/png _site
	rm -f font/sources/*.fea font/sources/*.json
