"""Tests the Bounce API."""

import json

from aiohttp import FormData

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


def test_paginate_clubs__success(server):
    import pdb
    # add dummy data to search for in database
    club_info = [['UBC Launch Pad', 'software engineering team'],
                 ['envision', 'something'], ['UBC biomed', 'something else']]
    for name, desc in club_info:
        server.app.test_client.post(
            '/clubs',
            data=json.dumps({
                'name': name,
                'description': desc,
                'website_url': '',
                'twitter_url': '',
                'facebook_url': '',
                'instagram_url': '',
            }))
    _, response = server.app.test_client.get('/clubs/search?page=0&size=2')
    pdb.set_trace()
    assert response.status == 200
    body = response.json
    assert body.get('result_count') == 3
    assert body.get('page') == 0
    assert body.get('total_pages') == 2

    _, response = server.app.test_client.get('/clubs/search?query=UBC')
    assert response.status == 200
    body = response.json
    assert len(body) == 2
    assert body[0]['name'] == 'UBC Launch Pad'
    assert body[0]['description'] == 'software engineering team'
    assert body[1]['name'] == 'UBC biomed'
    assert body[1]['description'] == 'something else'


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


def test_paginate_clubs__success(server):
    # add dummy data to search for in database
    club_info = [['UBC Launch Pad', 'software engineering team'],
                 ['envision', 'something'], ['UBC biomed', 'something else']]
    for name, desc in club_info:
        server.app.test_client.post(
            '/clubs',
            data=json.dumps({
                'name': name,
                'description': desc,
                'website_url': '',
                'twitter_url': '',
                'facebook_url': '',
                'instagram_url': '',
            }))
    _, response = server.app.test_client.get('/clubs/search?page=0&size=2')
    assert response.status == 200
    body = response.json
    assert body.get('result_count') == 4
    assert body.get('page') == 0
    assert body.get('total_pages') == 2


def test_search_clubs__success(server):
    _, response = server.app.test_client.get('/clubs/search?query=UBC')
    assert response.status == 200
    body = response.json
    assert len(body.get('results')) == 2
    assert body.get('results')[0]['name'] == 'UBC Launch Pad'
    assert body.get('results')[0]['description'] == 'software engineering team'
    assert body.get('results')[1]['name'] == 'UBC biomed'
    assert body.get('results')[1]['description'] == 'something else'


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
    token = util.create_jwt(2, server.config.secret)
    data = FormData()
    data.add_field('image', open('tests/testdata/large-logo.png', 'rb'))
    _, response = server.app.test_client.put(
        '/users/2/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_put_user_image__failure(server):
    token = util.create_jwt(3, server.config.secret)
    data = FormData()
    # No such user
    _, response = server.app.test_client.put(
        '/users/3/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 404
    # Forbidden (the user is trying to update another user's image)
    _, response = server.app.test_client.put(
        '/users/2/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 403
    # Invalid image name
    token = util.create_jwt(2, server.config.secret)
    _, response = server.app.test_client.put(
        '/users/2/images/$%^&*(',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 400


def test_get_user_image__success(server):
    _, response = server.app.test_client.get('/users/2/images/profile')
    assert response.status == 200


def test_get_user_image__failure(server):
    _, response = server.app.test_client.get('/users/3/images/profile')
    assert response.status == 404


def test_delete_user_image__success(server):
    token = util.create_jwt(2, server.config.secret)
    _, response = server.app.test_client.delete(
        '/users/2/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_delete_user_image__failure(server):
    token = util.create_jwt(3, server.config.secret)
    # No such image
    _, response = server.app.test_client.delete(
        '/users/3/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 404
    # Forbidden (user is trying to delete another user's image)
    _, response = server.app.test_client.delete(
        '/users/2/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 403
