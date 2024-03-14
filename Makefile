SHELL := /bin/bash
.PHONY: help
primary := '\033[1;36m'
err := '\033[0;31m'
bold := '\033[1m'
clear := '\033[0m'

-include .env
export $(shell [ -f .env ] && sed 's/=.*//' .env)
-include .env.local
export $(shell [ -f .env.local ] && sed 's/=.*//' .env.local)

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

deps: ## install dependancies for development of this project
	pip install -U pip
	pip install -U -r requirements-dev.txt
	pip install -e .
	pre-commit autoupdate

setup: ## setup for development of this project
	pre-commit install --hook-type pre-push --hook-type pre-commit
	@ [ -f .secrets.baseline ] || ( detect-secrets scan > .secrets.baseline )
	detect-secrets audit .secrets.baseline

clean: ## Cleanup tmp files
	@find . -type f -name '*.pyc' -delete 2>/dev/null
	@find . -type d -name '__pycache__' -delete 2>/dev/null
	@find . -type f -name '*.DS_Store' -delete 2>/dev/null

test: ## Prettier test outputs
	pre-commit run --all-files
	semgrep -q --strict --timeout=0 --config=p/r2c-ci --lang=py
	coverage run -m pytest --nf
	coverage report -m

unit-test: ## run unit tests with coverage
	coverage run -m pytest --nf
	coverage report -m

