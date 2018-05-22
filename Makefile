.PHONY: dev requirements install-requirements lint

# The docker-compose file to use for our dev environment
DEV := container/dev/docker-compose.yml

all: dev

# Start Postgres container and run a shell in the web container
dev:
	docker-compose -f ${DEV} up -d postgres
	docker-compose -f ${DEV} run --no-deps --rm -p 8080:8080 web bash

# Update requirements.txt
requirements:
	pip-compile --output-file requirements.txt requirements.in

# Install all packages in requirements.txt
install-requirements:
	pip install -r requirements.txt

# Update test-requirements.txt
test-requirements:
	pip-compile --output-file test-requirements.txt test-requirements.in

# Install all packages in test-requirements.txt
install-test-requirements:
	pip install -r test-requirements.txt

# Run linters to make sure there are no formatting issues
lint:
	@pylint --rcfile tox.ini server cli
	@flake8