
all: install

# Install required Node modules
.PHONY: install
install:
	@yarn

# Run all tests
.PHONY: test
test: styles
	@yarn run test

# Check for formatting errors
.PHONY: lint
lint:
	@./node_modules/.bin/eslint src

# Reformat code
.PHONY: format
format:
	@./node_modules/.bin/eslint --fix src

# Preprocess CSS
.PHONY: styles
styles:
	@./node_modules/.bin/sass src/sass/:src/css/
