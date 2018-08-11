# :basketball: Bounce

[![Build Status](https://travis-ci.org/ubclaunchpad/bounce.svg?branch=master)](https://travis-ci.org/ubclaunchpad/bounce)
[![Coverage Status](https://coveralls.io/repos/github/ubclaunchpad/bounce/badge.svg)](https://coveralls.io/github/ubclaunchpad/bounce)

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
* `BOUNCE_SECRET`: The secret the server uses to issue and validate JSON Web Tokens.
* `POSTGRES_HOST`: The hostname of the container running our Postgres DB. This should almost always be `postgres`.
* `POSTGRES_PORT`: The port the Postgres daemon should listen on. The default should be `5432`.
* `POSTGRES_USER`: Should match the setting by the same name in `postgres.env`.
* `POSTGRES_PASSWORD`: Should match the setting by the same name in `postgres.env`.
* `POSTGRES_DB`: Should match the setting by the same name in `postgres.env`.
* `ALLOWED_ORIGIN`: The domain that is allowed to access the API. For local development you can set this to your front-end URL (`http://localhost:3000`).

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

### Ubuntu 16.04

Some packages such as aiohttp > 3.0.0 won't be found in python 3.5's virtualenv. So you can do the following:
```bash
virtualenv -p /usr/bin/python3.6 py36env
source py36env/bin/activate # to start the virtualenv
pip3 install package-name
deactivate # to exit the virtualenv
```

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

### Testing

All tests should go in the `tests` folder. Put any fixtures your tests rely on in [conftest.py](tests/conftest.py). To run tests use:

```bash
# Run all tests
$ make docker-test
# Clean up test containers
$ make clean
```

### HTTP Server

We're relying on [Sanic](https://sanic.readthedocs.io/en/latest/) as our HTTP server framework. Our routes and HTTP request handlers can be found in [server/__init__.py](server/__init__.py).

#### Adding routes and resources

Adding a route that serves RESTful requests is best illustrated by example. In this example we'll add a new endpoint for managing Users.

**Step 1: Create request and response schemas**

First we need to figure out what we want our requests and responses to look like on this endpoint. For simplicity our endpoint will only accept GET requests. To make sure that requests and responses on this endpoint fit the required format we'll specify a schema for each, and we'll use these schemas to validate incoming requests and outgoing responses.

We want our GET requests to specify a `username` as we'll use it to retreive information about a user. We create a file in `bounce/server/resource` called `users.py` and put our schema for the `GetUserRequest` in it:

```python
class GetUserRequest(metaclass=ResourceMeta):
    """Defines the schema for a GET /users request."""
    __params__ = {
        'type': 'object',
        'required': ['username'],
        'properties': {
            'username': {
                'type': 'string',
            }
        }
    }
```

The `__params__` field is used to specify the schema that the request parameters must match. Specifically, `GET /users` requests require a `username` field with a `string` value. See [JSONSchema](https://python-jsonschema.readthedocs.io/en/latest/) for more information on schema creation.

We also want our responses to contain the user's full name, email, username, ID, and the time at which they were created, so we specify our `GetUserResponse` in the same file as follows:

```python
class GetUserResponse(metaclass=ResourceMeta):
    """Defines the schema for a GET /users response."""
    __body__ = {
        'type': 'object',
        'required': ['full_name', 'username', 'email', 'id', 'createdAt'],
        'additionalProperties': False,
        'properties': {
            'full_name': {
                'type': 'string'
            },
            'username': {
                'type': 'string',
            },
            'email': {
                'type': 'string',
                'format': 'email',
            },
            'id': {
                'type': 'integer',
                'minimum': 0,
            },
            'createdAt': {
                'type': 'integer',
            },
        }
    }
```

The `__body__` field is used to specify the schema that the response body must match. Specifically, the response to a `GET /users` request must contain the user's full name, username, email, ID and the time at which the user was created.

Note that in this example our request resource contained only a schema for params, and our response resource contained only a schema for the body. If you like you can specify neither or both schemas for `__params__` and `__body__` on your resource class.

**Step 2: Create a new Endpoint**

Now we create a new file in `bounce/server/api` called `users.py` and create a `UsersEndpoint` class in `users.py` that will contain all of our HTTP request handlers for the endpoint.

```python
"""Request handlers for the /users endpoint."""

from sanic import response

from ..resource import validate
from ..resource.user import GetUserRequest, GetUserResponse


class UsersEndpoint(Endpoint):
    """Handles requests to /users."""

    __uri__ = '/users'

    @validate(GetUserRequest, GetUserResponse)
    async def get(self, request):
        """Handles a GET /users request."""
        return response.json({
            'full_name': 'Test Boy',
            'username': 'tester',
            'email': 'test@test.com',
            'id': 1234,
            'created_at': 1529785677,
        }, status=200)
```

Notice that we're using the `@validate` decorator to validate the request parameters against our `GetUserRequest` schema when the request is passed to the function and to validate the response we return against the `GetUserResponse` schema. In this case we named our method `get` because it serves GET requests. Your method's name should match the HTTP method it handles, otherwise the server will not register it as a request handler. Since our `UsersEndpoint` does not have handlers for methods other than GET, it will automatically return an HTTP 405 "Method not allowed" when it sees requests to `/users` that are not GET requests.

**Step 3: Add the endpoint to the server**

Now we can add the endpoint to the server by updating `endpoints` in the `start` function in `cli.py`:

```python
def start(port, pg_host, pg_port, pg_user, pg_password, pg_database):
    """Starts the Bounce webserver with the given configuration."""
    conf = ServerConfig(port, pg_host, pg_port, pg_user, pg_password,
                        pg_database)
    # Register your new endpoints here
    endpoints = [UsersEndpoint]
    serv = Server(conf, endpoints)
    serv.start()
```

### Interacting with the DB

We're using [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html) for interacting with our Postgres DB. Anything related to the DB, like defining schemas/mappings from Python classes to tables, creating queries, and initialization should be placed in the `db` module.

### User Authentication

When a new Bounce user is created, the front-end passes the user's username and password to the Bounce server in an HTTP `POST` request to the `/users` endpoint. If the given username and password match our [security requirements](bounce/server/api/util.py) and the username is not already taken, the user will be added to the database.

Following this the user can log in with their username and password to acquire an access token for making authenticated requests to the API. To do this, the client makes an HTTP `POST` request to `/auth/login` with the user's credentials and the Bounce server validates the credentials and returns a [JSON Web Token](https://jwt.io/). The Bounce client can then use this access token on subsequent calls to the server, and the token will be validated by the server where necessary before serving requests. Access tokens issued be the server will expire after 30 days, at which point the user will have to log in again to acquire a new access token.

Any request handlers that require authentication should use the `@verify_token`. If you're using other decorators on your handler, `@verify_token` should come first (see the [UserEndpoint](bounce/server/api/users.py) for an example). This decorator will pass a `id_from_token` keyword argument to the request handler it's used on. This argument will contain the ID of the user to whom the token was issued, and should be used to verify that the user has access to the resource they're trying to access before the request is served. For example, in [UserEndpoint::put()](bounce/server/api/users.py) we use the `id_from_token` to make sure that the user is only trying to edit his/her _own_ information.

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
