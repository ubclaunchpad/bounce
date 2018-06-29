# The docker-compose files to use for our different environments
DEV := container/dev/docker-compose.yml
TEST := container/test/docker-compose.yml

# Container names
TEST_CONTAINER := ubclaunchpad/bounce:test

# The default SQL file to execute when migrating
MIGRATION ?= schema

all: dev

# Start Postgres container and run a shell in the web container
.PHONY: dev
dev:
	docker-compose -f ${DEV} up -d postgres
	docker-compose -f ${DEV} run --no-deps --rm -p 8080:8080 web bash

# Update requirements.txt
.PHONY: requirements
requirements:
	pip-compile --output-file requirements.txt requirements.in

# Install all packages in requirements.txt
.PHONY: install-requirements
install-requirements:
	pip install -r requirements.txt

# Update test-requirements.txt
.PHONY: test-requirements
test-requirements:
	pip-compile --output-file test-requirements.txt test-requirements.in

# Install all packages in test-requirements.txt
.PHONY: install-test-requirements
install-test-requirements:
	pip install -r test-requirements.txt

# Auto-format all Python files
.PHONY: format
format:
	@isort -rc bounce
	@yapf -i -r -vv bounce

# Run linters to make sure there are no formatting issues
.PHONY: lint
lint:
	@isort -rc -c bounce
	@yapf --diff -r bounce
	@pylint --rcfile setup.cfg bounce
	@flake8

# Runs the migration given by MIGRATION, or applies schema.sql if no MIGRATION
# is specified
.PHONY: migrate
migrate:
	@docker-compose -f ${DEV} exec postgres bash -c \
		"psql -U \$$POSTGRES_USER -d \$$POSTGRES_DB -f /var/bounce/${MIGRATION}.sql"

# Run tests in a Bounce test container
.PHONY: docker-test
docker-test:
	@docker-compose -f ${TEST} up -d postgres
	@docker-compose -f ${TEST} run --rm web

# Run tests in Travis
.PHONY: travis-test
travis-test:
	@docker-compose -f ${TEST} up -d postgres
	@docker-compose -f ${TEST} run --rm -e TRAVIS_JOB_ID="${TRAVIS_JOB_ID}" \
		-e TRAVIS_BRANCH="${TRAVIS_BRANCH}" -e COVERALLS_REPO_TOKEN="${COVERALLS_REPO_TOKEN}" \
		--entrypoint bash web -c "coverage run --source=bounce -m pytest -v && coveralls"

# Clean up test containers
.PHONY: clean
clean:
	@docker-compose -f ${TEST} stop
	@docker-compose -f ${TEST} rm -f
