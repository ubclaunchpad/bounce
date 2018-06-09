# :basketball: Bounce

[![Build Status](https://travis-ci.org/ubclaunchpad/bounce.svg?branch=master)](https://travis-ci.org/ubclaunchpad/bounce)

The backend for our application that brings people together based on common interests.

## Installation

### Requirements

Before you can install and run Bounce you'll need the following:

* Docker (see [Install Docker](https://docs.docker.com/install/))
* Docker Compose (see [Install Docker Compose](https://docs.docker.com/compose/install/))

### Configuration

Both the Python backend and Postgres need to be configured before they can run. Copy the [web](container/web.env.example) and [Postgres](container/postgres.env.example) example configuration files to `container/web.env` and `container/postgres.env` respectively. These files will contain the environment variables that our web server and Postgres rely on.

**Important:** Don't expose your config files to the web or commit them to source control.

#### Postgres

* `POSTGRES_USER`: The username to use with our database. This can be anything you like, but `bounce` is probably the most sensical choice.
* `POSTGRES_PASSWORD`: The DB password. Make this something relatively secure.
* `POSTGRES_DB`: The name of the DB we'll use in Postgres.

#### Web Server

* `PORT`: The port our web server will listen on. For development use `8080`, for production use `80`.
* `POSTGRES_HOST`: The hostname of the container running our Postgres DB. This should almost always be `postgres`.
* `POSTGRES_PORT`: The port the Postgres daemon should listen on. The default should be `5432`.
* `POSTGRES_USER`: Should match the setting by the same name in `postgres.env`.
* `POSTGRES_PASSWORD`: Should match the setting by the same name in `postgres.env`.
* `POSTGRES_DB`: Should match the setting by the same name in `postgres.env`.

### Running the Server

Once you have the requirements installed and you've created your config files you can run the Postgres and web containers.

```bash
$ make dev
```

This will start a Postgres container (if one is not already running) with the environment variables from `container/postgres.env` and a web container with the environment variables from `container/web.env`.

You should be dropped into a shell in your web container once both containers are running. From there you can install the Bounce Python package for development.

```bash
$ pip install -e .
```

Now you're ready to run the server.

```bash
bounce start
```

To check if your server is running navigate to [localhost:8080](http://localhost:8080/) in your browser. You should see see `Bounce API accepting requests!`. Note that this project directory is mounted to `/opt/bounce` in the `web` development container, so any edits you make to it should be immediately available in the container - no need to rebuild or restart it while developing!

## Development

### Packaging

Bounce is packaged as a Python package. [setup.py](setup.py) is used by tools like `pip` (which is what we're using) to specify details about our package like it's requirements, the packages it provides, and it's entry point (so we can run it as a command-line utility.

### Python Package Requirements

We use [requirements.in](requirements.in) to specify our dependencies and their versions. When you add a new dependency to the project make sure you specify it in this file, along with a specific version.

We use `pip-compile` to parse our depenencies and make sure they are all compatible. When you update [requirements.in](requirements.in) make sure you run

```bash
$ make requirements
```

to update [requirements.txt](requirements.txt) accordingly.

### Code Format

To ensure our code is nicely formatted and documented we use `isort`, `flake8`, and `pylint` through the `lint` Make target.

Before your commit your code, have `isort` and `yapf` auto-format your code by running `make format` from inside your dev container.

To check for code formatting issues, run `make lint` from inside your dev container.

Linter configuration can be found in [setup.cfg](setup.cfg). If you feel that specific lint rules are too restricitve, you can disable them in that file.

### HTTP Server

We're relying on [Sanic](https://sanic.readthedocs.io/en/latest/) as our HTTP server framework. Our routes and HTTP request handlers can be found in [server/__init__.py](server/__init__.py).

### Interacting with the DB

We're using [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html) for interacting with our Postgres DB. Anything related to the DB, like defining schemas/mappings from Python classes to tables, creating queries, and initialization should be placed in the `db` module.

#### Migrations

Every so often we'll have to update the DB schema. When you need to make an update, create a new `.sql` migration file under the `schema` folder. Your migration file's name should follow the format `N_verb_qualifiers_subject_qualifiers.sql`. So if you were creating the first migration (`N`=1) that updates the `Clubs` table by adding a `owner_id` column you would call your migration `1_add_owner_id_to_club.sql`.

To run your migration make sure your Postgres container is running (`make dev`), then run:

```bash
# Run <your migration file> against the DB in the POSTGRES container
$ make migrate MIGRATION=<your migration name>
```

For exmaple, if you wanted to apply the `1_add_owner_id_to_club` migration you would run

```bash
# Run 1_add_owner_id_to_club.sql against the DB in the POSTGRES container
$ make migrate MIGRATION=1_add_owner_id_to_club
```

### Command-line Interface

Bounce's command-line interface is built using [Click](http://click.pocoo.org/6/). Commands can be found in [cli/__init__.py](cli/__init__.py). Note that we generally won't have to specify options when running Bounce commands because `Click` will pull options from environment variables in our Docker conatiner (assuming `envvar`s are declared for the options).
