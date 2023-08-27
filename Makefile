EXAMPLES = $(shell find examples/ -type f)

all:
	black .
	isort .

$(EXAMPLES): all
	PYTHONPATH=. python $@

examples: $(EXAMPLES)

test: all
	python -m unittest tests/test_*.py