"""Defines fixtures for use in our tests."""

import pytest
<<<<<<< 58ddae63f22bf2f54edd5143cbf322eef552066b
from bounce.server import Server
from bounce.server.config import ServerConfig
from bounce.server.api.users import UserEndpoint, UsersEndpoint
=======

from bounce.server import Server
from bounce.server.api.users import UserEndpoint, UsersEndpoint
from bounce.server.config import ServerConfig
>>>>>>> first commit


@pytest.fixture
def config():
    """Returns test config for the server."""
    return ServerConfig(3131, 'postgres', 5432, 'bounce-test', 'bounce-test',
                        'bounce-test')


@pytest.fixture
def server(config):
    """Returns a test server."""
    serv = Server(config, [UserEndpoint, UsersEndpoint])
    serv.start(test=True)
    return serv
