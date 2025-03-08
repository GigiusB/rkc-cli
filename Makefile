.PHONY: clean clean-test clean-pyc clean-build docs help static
.DEFAULT_GOAL := help
PARALLEL_TEST?=-n auto

BROWSERCMD?=google-chrome

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

guard-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
        exit 1; \
    fi

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 src tests

test: ## run tests once
	@pytest ${PARALLEL_TEST}

test-save: ## run tests twice to check tests isolation
	@pytest tests ${PARALLEL_TEST} && pytest tests ${PARALLEL_TEST}

test-cov: ## run tests with coverage
	@pytest --junitxml=/tmp/test_report/pytest.xml -vv \
        --cov-report=xml:/tmp/test_report/coverage.xml --cov-report=html --cov-report=term \
        --cov-config=tests/.coveragerc \
        --cov=kt_odoo_ui_test
	@if [ "${BROWSERCMD}" != "" ]; then \
    	${BROWSERCMD} `pwd`/~build/coverage/index.html ; \
    fi

test-all: ## run tests on every Python version with tox
	tox

dev-email-ui:  ## Starts the console email smtp with UI
	docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog

bump:   ## Bumps version
	@while :; do \
		read -r -p "bumpversion [major/minor/patch]: " PART; \
		case "$$PART" in \
			major|minor|patch) break ;; \
  		esac \
	done ; \
	bumpversion --no-commit --allow-dirty $$PART
	echo "" >> .bumpversion.cfg
	@grep "^version = " pyproject.toml
