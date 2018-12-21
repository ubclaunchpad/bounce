"""Tests the Bounce API."""

import json

from aiohttp import FormData

from bounce.server.api import util


def test_post_users__success(server):
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'test',
            'full_name': 'Test Guy',
            'email': 'test@test.com',
            'password': 'Val1dPassword!'
        }))
    assert response.status == 201


def test_post_users__failure(server):
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'full_name': 'Test Guy',
            'email': 'test@test.com',
            'password': 'Val1dPassword!'
        }))
    assert response.status == 400
    assert 'error' in response.json


def test_put_user__success(server):
    username = 'test'
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'full_name': 'New Name',
            'email': 'newemail@test.com',
        }),
        headers={'Authorization': token})

    assert response.status == 200
    assert response.json['username'] == username
    assert response.json['full_name'] == 'New Name'
    assert response.json['email'] == 'newemail@test.com'
    assert response.json['id'] == 1
    assert isinstance(response.json['created_at'], int)


def test_put_user__failure(server):
    username = 'test'
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'garbage': True
        }),
        headers={'Authorization': token})
    assert response.status == 400


def test_get_user__success(server):
    _, response = server.app.test_client.get('/users/test')
    assert response.status == 200
    assert response.json['username'] == 'test'
    assert response.json['full_name'] == 'New Name'
    assert response.json['email'] == 'newemail@test.com'
    assert response.json['id'] == 1
    assert isinstance(response.json['created_at'], int)


def test_get_user__failure(server):
    _, response = server.app.test_client.get('/users/doesnotexist')
    assert response.status == 404


def test_login__success(server):
    _, response = server.app.test_client.post(
        '/auth/login',
        data=json.dumps({
            'username': 'test',
            'password': 'Val1dPassword!'
        }))
    assert response.status == 200
    assert isinstance(response.json['token'], str)


def test_login__failure(server):
    _, response = server.app.test_client.post(
        '/auth/login',
        data=json.dumps({
            'username': 'test',
            'password': 'WrongPassword!'
        }))
    assert response.status == 401


def test_delete_user__success(server):
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.delete(
        '/users/test', headers={'Authorization': token})
    assert response.status == 204


def test_delete_user__failure(server):
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.delete(
        '/users/doesnotexist', headers={'Authorization': token})
    assert response.status == 404
