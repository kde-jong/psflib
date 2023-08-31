EXAMPLES = $(shell find examples/ -type f -a -name "*.py")
SOURCES = $(shell find pypsf/ -type f -a -name "*.py")

fmt: $(SOURCES)
	python -m black -q .
	python -m isort -q .

prep:
	mkdir -p output/

$(EXAMPLES): all prep
	PYTHONPATH=. python $@

examples: $(EXAMPLES)

test: all
	python -m unittest tests/test_*.py

.PHONY: fmt prep examples test
