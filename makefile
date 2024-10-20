.PHONY: test lint coverage

test:
	python -m unittest discover tests

lint:
	black .

coverage:
	coverage run -m unittest discover tests
	coverage report
	coverage html

all: test lint coverage
