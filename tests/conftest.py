"""Defines fixtures for use in our tests."""

import pytest
from bounce.server import Server
from bounce.server.config import ServerConfig


@pytest.fixture
def config():
    """Returns test config for the server."""
    return ServerConfig(3131, 'postgres', 5432, 'bounce-test', 'bounce-test',
                        'bounce-test')


@pytest.fixture
def server(config):
    """Returns a test server."""
    return Server(config)
