.DEFAULT: setup
.PHONY: setup clean release release_test

setup: venv
	venv/bin/python setup.py develop

venv:
	virtualenv venv

clean:
	rm -rf venv
	rm -rf *.egg-info

release:
	python setup.py sdist upload -r pypi

release_test:
	python setup.py sdist upload -r pypitest
