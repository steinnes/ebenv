.DEFAULT: setup
.PHONY: setup

setup: venv
	venv/bin/python setup.py develop

venv:
	virtualenv venv

clean:
	rm -rf venv
	rm -rf *.egg-info
