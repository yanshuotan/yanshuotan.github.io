# Makefile for academic website and CV management
# ────────────────────────────────────────────────────────────────────────────
# Usage:
#   make cv       - Generate output/cv.tex and compile to output/cv.pdf
#   make site     - Process data → site/_data/, then serve Jekyll locally
#   make data     - Re-process all YAML data into site/_data/ only
#   make build    - Build Jekyll site into site/_site/ (no serve)
#   make all      - Generate CV + build Jekyll site
#   make clean    - Remove generated files
# ────────────────────────────────────────────────────────────────────────────

PYTHON     ?= python
PDFLATEX   := pdflatex
JEKYLL     := bundle exec jekyll

DATA_DIR   := data
SCRIPTS    := scripts
SITE_DIR   := site
OUTPUT_DIR := output
TEX_FILE   := $(OUTPUT_DIR)/cv.tex
PDF_FILE   := $(OUTPUT_DIR)/cv.pdf

.PHONY: all cv data site build clean help

## all: Generate CV and build Jekyll site
all: cv build

## cv: Render cv.tex from YAML and compile to PDF
cv: $(TEX_FILE)
	@echo "Compiling $(TEX_FILE) → $(PDF_FILE) …"
	@cd $(OUTPUT_DIR) && $(PDFLATEX) -interaction=nonstopmode cv.tex > /dev/null && \
	  $(PDFLATEX) -interaction=nonstopmode cv.tex > /dev/null
	@cp $(PDF_FILE) $(SITE_DIR)/assets/cv.pdf
	@echo "✓  PDF ready at $(PDF_FILE)"

$(TEX_FILE): $(wildcard $(DATA_DIR)/*.yaml) templates/cv.tex.j2 $(SCRIPTS)/generate_cv.py
	@mkdir -p $(OUTPUT_DIR)
	@$(PYTHON) $(SCRIPTS)/generate_cv.py

## data: Process YAML data → site/_data/
data: $(wildcard $(DATA_DIR)/*.yaml) $(SCRIPTS)/generate_site.py
	@$(PYTHON) $(SCRIPTS)/generate_site.py

## site: Process data and serve Jekyll locally (with live reload)
site: data
	@echo "Starting Jekyll dev server at http://localhost:4000 …"
	@cd $(SITE_DIR) && $(JEKYLL) serve --livereload

## build: Process data and build Jekyll site (no serve)
build: data
	@echo "Building Jekyll site …"
	@cd $(SITE_DIR) && $(JEKYLL) build
	@echo "✓  Site built at $(SITE_DIR)/_site/"

## clean: Remove generated outputs
clean:
	@rm -rf $(OUTPUT_DIR)/*.tex $(OUTPUT_DIR)/*.pdf $(OUTPUT_DIR)/*.log \
	         $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.out
	@rm -rf $(SITE_DIR)/_data/*.yaml $(SITE_DIR)/_site/
	@echo "✓  Cleaned generated files."

## help: Show this help message
help:
	@grep -E '^## ' Makefile | sed 's/^## //'
