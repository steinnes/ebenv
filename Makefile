.DEFAULT: setup
.PHONY: setup clean release release_test

setup: venv
	venv/bin/pip install -r dev-requirements.txt
	venv/bin/python setup.py develop

venv:
	virtualenv venv

clean:
	rm -rf *.egg-info
	rm -rf dist/*

lint:
	venv/bin/flake8 ebenv

release:
	venv/bin/python setup.py sdist bdist_wheel
	twine upload dist/*.tar.gz
	twine upload dist/*.whl

release_test:
	python setup.py sdist upload -r pypitest
