"""Tests the Bounce API."""

import json

from bounce.server.api import util


def test_root_handler(server):
    _, response = server.app.test_client.get('/')
    assert response.status == 200
    assert response.body == b'Bounce API accepting requests!'


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
        data=json.dumps({'garbage': True}),
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
        data=json.dumps({'username': 'test', 'password': 'Val1dPassword!'}))
    assert response.status == 200
    assert isinstance(response.json['token'], str)


def test_login__failure(server):
    _, response = server.app.test_client.post(
        '/auth/login',
        data=json.dumps({'username': 'test', 'password': 'WrongPassword!'}))
    assert response.status == 401


def test_delete_user__success(server):
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.delete(
        '/users/test',
        headers={'Authorization': token})
    assert response.status == 204


def test_delete_user__failure(server):
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.delete(
        '/users/doesnotexist',
        headers={'Authorization': token})
    assert response.status == 404


def test_post_clubs__success(server):
    _, response = server.app.test_client.post(
        '/clubs',
        data=json.dumps({
            'name': 'test',
            'description': 'club called test',
            'website_url': 'club.com',
            'facebook_url': 'facebook.com/test',
            'instagram_url': 'instagram.com/test',
            'twitter_url': 'twitter.com/test',
        }))
    assert response.status == 201


def test_post_clubs__failure(server):
    _, response = server.app.test_client.post(
        '/clubs',
        data=json.dumps({
            'name': 'test',
            'description': 'club called test',
            'website_url': 'club.com',
            'facebook_url': 'facebook.com/test',
            'instagram_url': 'instagram.com/test',
            'twitter_url': 'twitter.com/test',
        }))
    assert response.status == 409
    assert 'error' in response.json


def test_search_clubs(server):
# the server's test client doesn't expose a search method.
# It does expose a GET method but that can't provide a list
# of clubs like how the search method can.  Is there a way
# to use the search_clubs method created in the clubs endpoint?
# Reference:
# https://github.com/channelcat/sanic/blob/master/docs/sanic/testing.md

def test_put_club__success(server):
    _, response = server.app.test_client.put(
        '/clubs/test',
        data=json.dumps({
            'name': 'newtest',
            'description': 'club called new test',
        }))
    assert response.status == 200
    assert response.json['name'] == 'newtest'
    assert response.json['description'] == 'club called new test'
    assert response.json['id'] == 1
    assert isinstance(response.json['created_at'], int)


def test_put_club__failure(server):
    _, response = server.app.test_client.put(
        '/clubs/newtest', data=json.dumps({
            'garbage': True
        }))
    assert response.status == 400


def test_get_club__success(server):
    _, response = server.app.test_client.get('/clubs/newtest')
    assert response.status == 200
    assert response.json['name'] == 'newtest'
    assert response.json['description'] == 'club called new test'
    assert response.json['id'] == 1
    assert isinstance(response.json['created_at'], int)


def test_get_club__failure(server):
    _, response = server.app.test_client.get('/clubs/doesnotexist')
    assert response.status == 404


def test_delete_club__success(server):
    _, response = server.app.test_client.delete('/clubs/test')
    assert response.status == 204
