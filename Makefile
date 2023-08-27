EXAMPLES = $(shell find examples/ -type f)

all:
	python -m black .
	python -m isort .

$(EXAMPLES): all
	PYTHONPATH=. python $@

examples: $(EXAMPLES)

test: all
	python -m unittest tests/test_*.py