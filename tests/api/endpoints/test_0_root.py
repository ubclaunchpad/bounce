"""Tests the Bounce API."""

import json

from aiohttp import FormData

from bounce.server.api import util


def test_root_handler(server):
    _, response = server.app.test_client.get('/')
    assert response.status == 200
    assert response.body == b'Bounce API accepting requests!'
