"""Defines fixtures for use in our tests."""

import pytest

from bounce.server import Server
from bounce.server.api.auth import LoginEndpoint
<<<<<<< 44c7da3db86f72b4de2f45d358508ba095e9f112
from bounce.server.api.clubs import (ClubEndpoint, ClubsEndpoint,
                                     SearchClubsEndpoint)
from bounce.server.api.users import (UserEndpoint, UserImagesEndpoint,
                                     UsersEndpoint)
=======
from bounce.server.api.users import UserEndpoint, UsersEndpoint
from bounce.server.api.clubs import ClubEndpoint, ClubsEndpoint, SearchClubsEndpoint
>>>>>>> create new SearchClubsEndpoint
from bounce.server.config import ServerConfig


@pytest.fixture
def config():
    """Returns test config for the server."""
    return ServerConfig(3131, 'test_secret', 'postgres', 5432, 'bounce-test',
                        'bounce-test', 'bounce-test', '*', 'images')


@pytest.fixture
def server(config):
    """Returns a test server."""
<<<<<<< 44c7da3db86f72b4de2f45d358508ba095e9f112
    serv = Server(config, [
        UserEndpoint, UsersEndpoint, ClubEndpoint, ClubsEndpoint,
        LoginEndpoint, UserImagesEndpoint, SearchClubsEndpoint
    ])
=======
    serv = Server(config, [UserEndpoint, UsersEndpoint, SearchClubsEndpoint,
                           ClubEndpoint, ClubsEndpoint, LoginEndpoint])
>>>>>>> create new SearchClubsEndpoint
    serv.start(test=True)
    return serv
