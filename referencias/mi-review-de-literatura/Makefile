# Compila cada .md de esta carpeta a PDF (pandoc + tectonic).
# Requisitos: brew install pandoc tectonic
#   make          -> compila todos los .md que cambiaron
#   make clean    -> borra los PDFs generados

PANDOC_FLAGS = --pdf-engine=tectonic \
  -V lang=es \
  -V geometry:margin=2.5cm \
  -V colorlinks=true \
  -V mainfont="STIX Two Text" \
  -V mathfont="STIX Two Math" \
  -H header.tex

MDS  := $(wildcard *.md)
PDFS := $(MDS:.md=.pdf)

all: $(PDFS)

%.pdf: %.md header.tex $(wildcard img/*/*)
	pandoc $< -o $@ $(PANDOC_FLAGS)

clean:
	rm -f $(PDFS)

.PHONY: all clean
