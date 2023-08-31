EXAMPLES = $(shell find examples/ -type f -a -name "*.py")
SOURCES = $(shell find psflib/ -type f -a -name "*.py")

fmt: $(SOURCES)
	python -m black -q .
	python -m isort -q .

prep:
	mkdir -p output/

$(EXAMPLES): fmt prep
	PYTHONPATH=. python $@

examples: $(EXAMPLES)

test: fmt
	python -m unittest tests/test_*.py

.PHONY: fmt prep examples test
