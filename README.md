# :basketball: Bounce

[![Build Status](https://travis-ci.org/ubclaunchpad/bounce-front-end.svg?branch=master)](https://travis-ci.org/ubclaunchpad/bounce-front-end)

Frontend for our application that brings people together based on common interests.

## Installation

Clone the repository:

```bash
$ git clone https://github.com/ubclaunchpad/bounce-front-end.git
$ cd bounce-front-end
```

Install required packages

```bash
$ make
```

Start local server

```bash
$ yarn start
```

## Development

### Code Formatting

We're using [ESLint](https://eslint.org/) for JavaScript linting and formatting. Before you commit, make sure your code is appropriately formatted and linted

```bash
$ make format
```

ESLint config can be found in [.eslintrc.yml](.eslintrc.yml). You can disable errors/warnings globally by altering the config in that file, or you can do so on a per-file or per-line using comments (see the top of [App.js](src/App.js) for an example).

### Testing

To run tests and view code coverage use:

```bash
$ make test
```
