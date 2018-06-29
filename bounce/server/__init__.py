"""
Sets up Bounce's HTTP server.
"""

# Disable pylint's unused argument warnings in this module because we might
# not use our `request` arguments on some of our HTTP request handlers.s

from sanic import Sanic, response
from sanic.log import logger

from .. import db

DB_DRIVER = 'postgresql'
ALL_METHODS = [
    'GET', 'PUT', 'POST', 'DELETE', 'HEAD', 'CONNECT', 'OPTIONS', 'TRACE'
]


class Server:
    """Represents the Bounce webserver."""

    def __init__(self, config, endpoints):
        """Creates the server from the given config.

        Args:
            config (ServerConfig): configuration for the server
            endpoints (list[Endpoint]): list of Endpoints this server serves
                requests at
        """
        self._config = config
        self._app = Sanic()
        self._engine = None
        self._sessionmaker = None

        # Register routes for all endpoints
        self._app.add_route(self.root_handler, '/', methods=['GET'])
        for endpoint in endpoints:
            handler = endpoint(self)
            self._app.add_route(
                handler.handle_request, handler.uri, methods=ALL_METHODS)
            logger.info('Registered request handler for %s', handler.uri)

    def start(self):
        """Connects to the DB and starts the HTTP server."""
        # First make sure this server is not already running
        assert self._engine is None and self._sessionmaker is None, (
            'server is already running')
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
        # First make sure this server is actually running
        assert self._engine and self._sessionmaker, 'server was not running'
        self._app.stop()

    @property
    def app(self):
        """Returns the Sanic app associated with this server."""
        return self._app

    @property
    def config(self):
        """Returns the config for this server."""
        return self._config

    @property
    def db_session(self):
        """Create a new DB session."""
        return self._sessionmaker(autoflush=True)

    async def root_handler(self, _):
        """Returns an HTTP 200 reponse containing a simple message."""
        return response.text('Bounce API accepting requests!')
