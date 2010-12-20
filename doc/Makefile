# Makefile for googlemaps Sphinx documentation

SPHINXBUILD   = ~/software/bin/sphinx-build
BROWSER		  = firefox

.PHONY: clean html show

html:
	$(SPHINXBUILD) . html/

show: html
	$(BROWSER) html/index.html &

clean:
	-rm -rf html/
