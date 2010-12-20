# pygeocoder Makefile

export PYTHONPATH := $(realpath pygeocoder):$(PYTHONPATH)
PYTHON=python
SFUSER=doctorj
SFPROJ=pygeocoder
SRCDIR=pygeocoder
# SourceForge's File Release System path needs the first 1 and 2 chars of the project name.
SFPROJ1:=$(shell $(PYTHON) -c "print '$(SFPROJ)'[0]")
SFPROJ2:=$(shell $(PYTHON) -c "print '$(SFPROJ)'[0:2]")

.PHONY: doc release pypi clean test

release: clean doc $(SRCDIR)/*.py test/*.py
	rm -f dist/*
	$(PYTHON) setup.py sdist bdist_wininst
	# This is a workaround for a Python 2.6 bug
	export VER=`python setup.py --version`;	mv dist/$(SRCDIR)-$${VER}.linux-x86_64.exe dist/$(SRCDIR)-$${VER}.win32.exe
	
	rsync -rv --chmod=u+rwX,go+rX dist/* $(SFUSER),$(SFPROJ)@frs.sourceforge.net:/home/pfs/project/$(SFPROJ1)/$(SFPROJ2)/$(SFPROJ)/
	rsync -rv --chmod=u+rwX,go+rX doc/html/* $(SFUSER),$(SFPROJ)@web.sourceforge.net:htdocs/
	@#scp -r dist/* $(SFUSER),$(SFPROJ)@frs.sourceforge.net:/home/pfs/project/$(SFPROJ1)/$(SFPROJ2)/$(SFPROJ)/
	@#scp -r doc/html/* $(SFUSER),$(SFPROJ)@web.sourceforge.net:htdocs/
	@echo -e "\n\nDon't forget to do an svn commit if needed."

pypi: doc
	$(PYTHON) setup.py sdist upload
	@#$(PYTHON) setup.py bdist_wininst upload
	@echo "Upload win32.exe to PyPI."

doc:
	cd doc; $(MAKE) html
	
test:
	@# You'll need a Google Maps API key in the file test/gmaps-api-key.txt or test_googlemaps.py
	cd test; $(PYTHON) test_googlemaps.py
	
clean:
	cd doc; $(MAKE) clean
	rm -rf dist build 
	rm -f $(SRCDIR)/*.pyc test/*.pyc setup.pyc MANIFEST
