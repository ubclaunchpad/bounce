"""
Sets up Bounce's HTTP server.
"""

# Disable pylint's unused argument warnings in this module because we might
# not use our `request` arguments on some of our HTTP request handlers.
# pylint: disable=unused-argument

from sanic import Sanic, response


class Server:
    """Represents the Bounce webserver."""

    def __init__(self, config):
        """Creates the server from the given config."""
        self.config = config
        self.app = Sanic()

        # Register routes
        self.app.add_route(self.root, '/')

    def start(self):
        """Starts the HTTP server."""
        self.app.run(host='0.0.0.0', port=self.config.server_port)

    async def root(self, request):
        """Returns an HTTP 200 reponse containing a simple 'Hello World'
        message."""
        return response.text('Bounce API accepting requests!')
