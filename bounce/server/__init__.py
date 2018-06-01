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
        self.config = config
        self.app = Sanic()
        self._engine = None

        # Register routes
        self.app.add_route(self.root, '/')

    def start(self):
        """Connects to the DB and starts the HTTP server."""
        # Set up engine for interacting with the DB
        self._engine = db.create_engine(
            DB_DRIVER, self.config.postgres_user,
            self.config.postgres_password, self.config.postgres_host,
            self.config.postgres_port, self.config.postgres_db)

        # Create missing tables based on schema in `db` module
        db.create_missing_tables(self._engine)

        # Start listening on the configured port
        self.app.run(host='0.0.0.0', port=self.config.server_port)

    def get_db_session(self):
        """Create a new DB session."""
        return db.get_session(self._engine)

    async def root(self, request):
        """Returns an HTTP 200 reponse containing a simple 'Hello World'
        message."""
        return response.text('Bounce API accepting requests!')
