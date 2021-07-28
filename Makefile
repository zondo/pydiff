# Makefile for pyxldiff.

include conf/Makefile.conf

SETUP = $(PYTHON) setup.py

PYPI = pypi
CHECK = twine check $(FILES)
UPLOAD = twine upload -r $(PYPI) --skip-existing $(FILES)
FILES = dist/*

CLEANFILES = build dist *.egg* *.zip *.el __pycache__ .tox

MAKEFLAGS = --no-print-directory

.DEFAULT:;	@ $(SETUP) $@ $(OPTS)

all:		develop

develop:;	$(PYTHON) -m pip install -e .

check:;		$(CHECK)

upload:		wheel sdist
		$(UPLOAD)

upload-test:	wheel sdist
		@ $(MAKE) upload PYPI=pypitest

verify:		test flake mypy

test:;		$(PYTHON) -m pytest -v

flake:;		flake8 xldiff tests

mypy:;		mypy xldiff

clean:;		$(SETUP) $@
		find . -name '*.py[co]' | xargs rm
		rm -rf $(CLEANFILES)
