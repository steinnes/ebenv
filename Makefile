.DEFAULT: setup
.PHONY: setup clean release release_test

setup: venv
	venv/bin/python setup.py develop

venv:
	virtualenv venv

clean:
	rm -rf *.egg-info
	rm -rf dist/*

release:
	venv/bin/python setup.py sdist bdist_wheel
	twine upload dist/*.tar.gz
	twine upload dist/*.whl

release_test:
	python setup.py sdist upload -r pypitest
