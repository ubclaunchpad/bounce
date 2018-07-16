"""Tests the Bounce API."""

import json


def test_root_handler(server):
    _, response = server.app.test_client.get('/')
    assert response.status == 200
    assert response.body == b'Bounce API accepting requests!'
<<<<<<< 58ddae63f22bf2f54edd5143cbf322eef552066b
=======
    print(_)
>>>>>>> first commit


def test_post_users__success(server):
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'test',
            'full_name': 'Test Guy',
            'email': 'test@test.com',
        }))
    assert response.status == 201


def test_post_users__failure(server):
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'full_name': 'Test Guy',
            'email': 'test@test.com',
        }))
    assert response.status == 400
    assert 'error' in response.json


def test_put_user__success(server):
    _, response = server.app.test_client.put(
        '/users/test',
        data=json.dumps({
            'full_name': 'New Name',
            'email': 'newemail@test.com',
        }))
    assert response.status == 200
    assert response.json['username'] == 'test'
    assert response.json['full_name'] == 'New Name'
    assert response.json['email'] == 'newemail@test.com'
    assert response.json['id'] == 1
    assert isinstance(response.json['created_at'], int)


def test_put_user__failure(server):
    _, response = server.app.test_client.put(
        '/users/test', data=json.dumps({
            'garbage': True
        }))
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


def test_delete_user__success(server):
    _, response = server.app.test_client.delete('/users/test')
    assert response.status == 204
<<<<<<< 58ddae63f22bf2f54edd5143cbf322eef552066b
=======

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
>>>>>>> first commit
