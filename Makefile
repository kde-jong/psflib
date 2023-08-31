EXAMPLES = $(shell find examples/ -type f -a -name "*.py")
SOURCES = $(shell find psflib/ -type f -a -name "*.py")


build: fmt $(SOURCES)
	python -m build

clean:
	rm -rf dist/ output/ */__pycache__ poetry.lock

re: clean build

test: fmt
	python -m unittest tests/test_*.py


fmt: $(SOURCES)
	python -m black -q .
	python -m isort -q .


prep:
	mkdir -p output/

$(EXAMPLES): fmt prep
	PYTHONPATH=. python $@

examples: $(EXAMPLES)


.PHONY: fmt prep examples test
