"""
Sets up Bounce's HTTP server.
"""

# Disable pylint's unused argument warnings in this module because we might
# not use our `request` arguments on some of our HTTP request handlers.
# pylint: disable=unused-argument

from sanic import Sanic, response

from .. import db

DB_DRIVER = 'postgresql'


class Server:
    """Represents the Bounce webserver."""

    def __init__(self, config):
        """Creates the server from the given config."""
        self._config = config
        self._app = Sanic()
        self._engine = None
        self._sessionmaker = None

        # Register routes
        self._app.add_route(self.root_handler, '/', methods=['GET'])

    def start(self):
        """Connects to the DB and starts the HTTP server."""
        # Set up engine for interacting with the DB
        self._engine = db.create_engine(
            DB_DRIVER, self._config.postgres_user,
            self._config.postgres_password, self._config.postgres_host,
            self._config.postgres_port, self._config.postgres_db)

        # Set up the sessionmaker we'll use to create DB sessions
        self._sessionmaker = db.get_sessionmaker(self._engine)

        # Start listening on the configured port
        self._app.run(host='0.0.0.0', port=self._config.server_port)

    def stop(self):
        """Stops the web server."""
        self._app.stop()

    @property
    def app(self):
        """Returns the Sanic app associated with this server."""
        return self._app

    @property
    def config(self):
        """Returns the config for this server."""
        return self._config

    def get_db_session(self):
        """Create a new DB session."""
        return self._sessionmaker()

    async def root_handler(self, request):
        """Returns an HTTP 200 reponse containing a simple message."""
        return response.text('Bounce API accepting requests!')
