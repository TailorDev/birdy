# Birdy

all: install

install:
	python setup.py install

install-dev:
	pip install -r requirements-dev.txt
	python setup.py develop

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr

distclean: clean
	rm -fr *.egg *.egg-info/

test:
	venv/bin/py.test -vs tests/
