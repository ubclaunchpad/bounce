"""Tests the Bounce API."""

import json

from aiohttp import FormData

from bounce.server.api import util


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
    # updating clubs requires Admin or President privileges
    # therefore we must set a user to have an Admin/President membership

    # add a test user
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'user2',
            'full_name': 'Hello WOrld',
            'email': 'something@anotherthing.com',
            'password': 'Val1dPassword!'
        }))

    # add a President membership for this user to this club
    token = util.create_jwt(2, server.config.secret)
    _, response = server.app.test_client.put(
        '/memberships/test?user_id=2&access=President',
        data=json.dumps({
            'role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': token})
    assert response.status == 201

    # check the user's role given the id from his/her token
    id = util.check_jwt(token, server.config.secret)
    _, response = server.app.test_client.get('/memberships/test?user_id=' +
                                             str(id) + '&access=President')
    role = response.json[0].get('role')

    # test if the club is successfully edited by President
    _, response = server.app.test_client.put(
        '/clubs/test?access=' + role,
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
    # deleting clubs requires Admin or President privileges
    # therefore use the user's id retrieved from his/her token and
    # use it to check he or she is an Admin or President of the club

    token = util.create_jwt(2, server.config.secret)
    # check the user's role given the id from his/her token
    id = util.check_jwt(token, server.config.secret)
    _, response = server.app.test_client.get('/memberships/newtest?user_id=' +
                                             str(id) + '&access=President')
    role = response.json[0].get('role')

    _, response = server.app.test_client.delete('/clubs/newtest?access=' +
                                                role)
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
    assert body.get('result_count') == 3
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
