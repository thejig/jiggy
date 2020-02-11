PWD := $(shell pwd)

.PHONY: black
black:
	tox -e black

.PHONY: tests
tests:
	tox

.PHONY: lint
lint:
	tox -e pylint

.PHONY: flake
flake:
	tox -e flake8


.PHONY: pre-commit
pre-commit:
	tox -e pylint
	tox -e flake8
	tox -vv

.PHONY: clean
clean:
	rm -rf build
	rm -rf doc/build
