# REPO_OWNER name and PROJECT_NAME must be lowercase
REPO_OWNER=workiva
PROJECT_NAME=pies

IMAGE_TAG=$(REPO_OWNER)/$(PROJECT_NAME)_dev

# Find all of the python files in the project
SOURCE_CODE=$(shell find pies tests setup.py -name \*.py -type f)

# Get the private index-url from pip.conf
PIP_INDEX_URL="$$(grep "@pypi" ~/.pip/pip.conf | awk '{print $$3}')"

# Build up to the build stage
DOCKER_BUILD=docker build . $(BUILD_ARGS) -t $(IMAGE_TAG) \
	     --build-arg PIP_INDEX_URL=$(PIP_INDEX_URL)

# Ensure the container is built and execute a command in it
DOCKER_RUN=docker run --rm -p 5000:5000 -dt $(RUN_ARGS) -v $(CURDIR):/$(PROJECT_NAME) $(IMAGE_TAG)  sh -c

# Run before every command executed in the container
DOCKER_PRETASK=cd /$(PROJECT_NAME) && make local-format

# Run run local make target in a docker container ex: check-cfn -> local-checkcfn
RUN_LOCAL_COMMAND_IN_DOCKER=$(DOCKER_BUILD) --target build && $(DOCKER_RUN) "$(DOCKER_PRETASK) && make local-$@"

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | \
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' | \
	sed "s/local-//" | \
	sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc ## Remove build artifacts and python artifacts

clean-build: ## Remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## Remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

update-template: ## Update the cookiecutter template (Overrides upstaged changes)
	cookiecutter gh:workiva/cookiecutter-python-dockerdev --output-dir .. --config-file .cookiecutter.yaml --no-input --overwrite-if-exists
# Template update command taken from https://github.com/audreyr/cookiecutter/issues/784

# All of the rules with the "local-" prefix are not run in a docker container
# To execute 'local-{name}' rules in the docker container add '{name}' to DOCKER_RULES.
DOCKER_RULES := $(DOCKER_RULES) ready
local-ready: local-test local-update-docs ## Format and test all code
	@echo "All checks pass. You're ready to commit!"

DOCKER_RULES := $(DOCKER_RULES) coverage-view
local-coverage-view: local-test # Open a test coverage map in your browser
	coverage html
	open htmlcov/index.html

DOCKER_RULES := $(DOCKER_RULES) check
local-check: local-check-format

DOCKER_RULES := $(DOCKER_RULES) check-format
local-check-format: ## Throw an error if project files need formatting changes
	 @{ [ ! "$(shell yapf --recursive --diff $(SOURCE_CODE))" ]  && \
	 [ ! "$(shell isort --check-only --recursive | grep "ERROR")" ] && [ ! $(shell unify --check $(SOURCE_CODE)) ]; } || \
	 { echo "Please run 'make format' to fix incorrect formatting" && exit 1; }
	@echo "All python files are properly formatted"

DOCKER_RULES := $(DOCKER_RULES) codecov
local-codecov: ## Report coverage results to the Codecov server.
	./codecov.sh

DOCKER_RULES := $(DOCKER_RULES) package
local-package: ## Generate a *.whl file for the project
	python setup.py bdist_wheel

DOCKER_RULES := $(DOCKER_RULES) format
local-format: ## Automatically format code using yapf, isort, and unify
	@echo "Formatting to fit style guide"
	@yapf --recursive --in-place $(SOURCE_CODE)
	@isort --apply --atomic --recursive
	@unify  --in-place $(SOURCE_CODE)

DOCKER_RULES := $(DOCKER_RULES) test
local-test: ## Run linter, coverage, and unit tests
	py.test -x --junitxml test_results.xml tests

DOCKER_RULES := $(DOCKER_RULES) debug
local-debug: ## Run linter, coverage, and debug unit tests
	py.test -x --pdb tests

DOCKER_RULES := $(DOCKER_RULES) test-watch
local-test-watch: ## Run the unit tests on filechanges if the tests fail
	py.test --looponfail tests

DOCKER_RULES := $(DOCKER_RULES) update-docs
local-update-docs: ## Update the documentation
	md-magic --config ./markdown.config.js

DOCKER_RULES := $(DOCKER_RULES) shell
local-shell: ## Open a shell in build stage of the project's Dockerfile
	bash

build: ## Build the entire Dockerfile
	$(DOCKER_BUILD)

# List all of the targets in the Makefile for testing
# Manually exclude targets by adding them to the grep or statement
# Based on : https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | \
        awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | \
        sort | \
	grep -v "local-\|shell\|watch\|coverage-view\|debug\|update-template" | \
	egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | \
        xargs

# Ignore files/directories with the same name as the target ex: "test"
.PHONY: $(DOCKER_RULES)

# When 'make test' is run, the Makefile will run 'make local-test' in the docker container
$(DOCKER_RULES):
	$(RUN_LOCAL_COMMAND_IN_DOCKER)
