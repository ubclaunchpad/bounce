"""Tests the Bounce API."""

import json

from aiohttp import FormData

from bounce.server.api import util


def test_put_user_image__success(server):
    # POST a dummy user to add a profile image to
    server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'test',
            'full_name': 'Test Guy',
            'email': 'test@test.com',
            'password': 'Val1dPassword!'
        }))
    token = util.create_jwt(3, server.config.secret)
    data = FormData()
    data.add_field('image', open('tests/testdata/large-logo.png', 'rb'))
    _, response = server.app.test_client.put(
        '/users/3/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_put_user_image__failure(server):
    token = util.create_jwt(4, server.config.secret)
    data = FormData()
    # No such user
    _, response = server.app.test_client.put(
        '/users/4/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 404
    # Forbidden (the user is trying to update another user's image)
    _, response = server.app.test_client.put(
        '/users/3/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 403
    # Invalid image name
    token = util.create_jwt(3, server.config.secret)
    _, response = server.app.test_client.put(
        '/users/3/images/$%^&*(',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 400


def test_get_user_image__success(server):
    _, response = server.app.test_client.get('/users/3/images/profile')
    assert response.status == 200


def test_get_user_image__failure(server):
    _, response = server.app.test_client.get('/users/4/images/profile')
    assert response.status == 404


def test_delete_user_image__success(server):
    token = util.create_jwt(3, server.config.secret)
    _, response = server.app.test_client.delete(
        '/users/3/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_delete_user_image__failure(server):
    token = util.create_jwt(4, server.config.secret)
    # No such image
    _, response = server.app.test_client.delete(
        '/users/4/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 404
    # Forbidden (user is trying to delete another user's image)
    _, response = server.app.test_client.delete(
        '/users/3/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 403
