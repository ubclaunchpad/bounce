"""Defines fixtures for use in our tests."""

import pytest

from bounce.server import Server
from bounce.server.api.auth import LoginEndpoint
from bounce.server.api.clubs import (ClubEndpoint, ClubsEndpoint,
                                     SearchClubsEndpoint, ClubImagesEndpoint)
from bounce.server.api.membership import MembershipEndpoint
from bounce.server.api.users import (SearchUsersEndpoint, UserEndpoint,
                                     UserImagesEndpoint, UsersEndpoint)
from bounce.server.config import ServerConfig


@pytest.fixture
def config():
    """Returns test config for the server."""
    return ServerConfig(3131, 'test_secret', 'postgres', 5432, 'bounce-test',
                        'bounce-test', 'bounce-test', '*', 'images')


@pytest.fixture
def server(config):
    """Returns a test server."""
    serv = Server(config, [
        UserEndpoint, UsersEndpoint, ClubEndpoint, ClubsEndpoint,
        LoginEndpoint, UserImagesEndpoint, SearchClubsEndpoint,
        SearchUsersEndpoint, ClubImagesEndpoint
    ])
    serv.start(test=True)
    return serv
