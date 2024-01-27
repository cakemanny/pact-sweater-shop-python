
VIRTUAL_ENV ?=
PY = $(VIRTUAL_ENV)/bin/python

ifeq "$(VIRTUAL_ENV)" ""
.PHONY: check_venv
check_venv:
	@echo "not in a virtual env ... could try this:"
	@echo "python3 -m venv .venv; . .venv/bin/activate"
	@exit 1
endif

.PHONY: all
all: install

.PHONY: install
install:
	$(PY) -m pip install wheel
	$(PY) -m pip install -e '.[test,dev]'

.PHONY: test
test:
	$(PY) -m pytest

.PHONY: lint
lint:
	$(PY) -m flake8

.venv:
	python3 -m venv .venv

ifeq "$(realpath $(VIRTUAL_ENV))" "$(realpath .venv)"
.PHONY: clean
clean:
	rm -rf .venv src/*.egg-info
	find . -type d -name __pycache__ -delete
endif
