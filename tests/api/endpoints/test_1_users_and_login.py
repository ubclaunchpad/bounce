"""Tests the Bounce API."""

import json

from bounce.server.api import util


def test_post_users__success(server):
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'test',
            'full_name': 'Test Guy',
            'email': 'test@test.com',
            'bio': 'my name is test. I am a cs major',
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
            'password': 'Val1dPassword!'
        }),
        headers={'Authorization': token})

    assert response.status == 200
    assert response.json['username'] == username
    assert response.json['full_name'] == 'New Name'
    assert response.json['email'] == 'newemail@test.com'
    assert response.json['id'] == 1
    assert response.json['bio'] == 'my name is test. I am a cs major'
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


def test_paginate_users__success(server):
    # add 3 dummy data entries to search for in database.
    # In total there's 4 with one coming from previous tests.
    user_info = [('matt gin', 'ginsstaahh', 'matthewgin10@gmail.com',
                  'Val1dPassword!', 'ginsstaahs bio'),
                 ('gin', 'ginsstaahh221', 'matt.gin@hotmail.com',
                  'Val1dPassword!', 'my second bio'),
                 ('bruno', 'bfcbachman', 'bruno@gmail.com', 'Val1dPassword!',
                  'brunos bio')]
    for full_name, username, email, password, bio in user_info:
        server.app.test_client.post(
            '/users',
            data=json.dumps({
                'full_name': full_name,
                'username': username,
                'email': email,
                'bio': bio,
                'password': password,
            }))
    _, response = server.app.test_client.get('/users/search?size=2')
    assert response.status == 200
    body = response.json
    assert body.get('result_count') == 4
    assert body.get('page') == 0
    assert body.get('total_pages') == 2


def test_paginate_users__failure(server):
    _, response = server.app.test_client.get('/users/search?size=0')
    assert response.status == 400
    _, response = server.app.test_client.get('/users/search?size=25')
    assert response.status == 400


def test_search_users__success(server):
    _, response = server.app.test_client.get('/users/search?query=gin')
    assert response.status == 200
    body = response.json
    assert len(body.get('results')) == 2


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
