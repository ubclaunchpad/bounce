"""Tests the Bounce API."""

import json

from bounce.server.api import util


def test_post_clubs__success(server):
    # A user is required to create the club
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'founder',
            'full_name': 'Test Guy',
            'email': 'test@test.com',
            'password': 'Val1dPassword!'
        }))
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)

    # post club using the id of the user from token
    _, response = server.app.test_client.post(
        '/clubs',
        data=json.dumps({
            'name': 'test',
            'description': 'club called test',
            'website_url': 'club.com',
            'facebook_url': 'facebook.com/test',
            'instagram_url': 'instagram.com/test',
            'twitter_url': 'twitter.com/test',
        }),
        headers={'Authorization': token})
    assert response.status == 201


def test_post_clubs__failure(server):
    # Get token for founder
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)
    _, response = server.app.test_client.post(
        '/clubs',
        data=json.dumps({
            'name': 'test',
            'description': 'club called test',
            'website_url': 'club.com',
            'facebook_url': 'facebook.com/test',
            'instagram_url': 'instagram.com/test',
            'twitter_url': 'twitter.com/test',
        }),
        headers={'Authorization': token})
    assert response.status == 409
    assert 'error' in response.json


def test_put_club__success(server):
    # updating clubs requires Admin or President privileges
    # therefore we will get the owners id to get access
    _, response = server.app.test_client.get('/users/founder')
    founder_id = response.json['id']
    founder_token = util.create_jwt(founder_id, server.config.secret)

    # test if the club is successfully edited by President
    _, response = server.app.test_client.put(
        '/clubs/test',
        data=json.dumps({
            'name': 'newtest',
            'description': 'club with a new description',
        }),
        headers={'Authorization': founder_token})
    assert response.status == 200
    assert response.json['description'] == 'club with a new description'
    assert response.json['id'] == 1
    assert isinstance(response.json['created_at'], int)

    # test if the club is successfully edited by an Admin
    # First, create admin user
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'adminPerson',
            'full_name': 'admin Guy',
            'email': 'test@somethingelse.com',
            'password': 'Val1dPassword!'
        }))
    _, response = server.app.test_client.get('/users/adminPerson')
    admin_id = response.json['id']
    admin_token = util.create_jwt(admin_id, server.config.secret)

    # add Admin membership
    _, response = server.app.test_client.put(
        '/memberships/newtest?user_id=' + str(admin_id),
        data=json.dumps({
            'members_role': 'Admin',
            'position': 'tech lead'
        }),
        headers={'Authorization': founder_token})
    assert response.status == 201

    # test if the club is successfully edited by Admin
    _, response = server.app.test_client.put(
        '/clubs/newtest',
        data=json.dumps({
            'name': 'newtest',
            'description': 'club with a newer description',
        }),
        headers={'Authorization': admin_token})
    assert response.status == 200
    assert response.json['description'] == 'club with a newer description'
    assert response.json['id'] == 1
    assert isinstance(response.json['created_at'], int)


def test_put_club__failure(server):
    # bad json data test:
    # first get the founder's id to get access
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)

    # bad json data
    _, response = server.app.test_client.put(
        '/clubs/newtest',
        data=json.dumps({
            'garbage': True
        }),
        headers={'Authorization': token})
    assert response.status == 400

    # try editing the club with a Member membership
    # first create user whom we will give a member membership to
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'member',
            'full_name': 'Matthew Gin',
            'email': 'matt@gin.com',
            'password': 'Val1dPassword!'
        }))
    # get the founder's id and his membership to get access
    # to add the member to the club
    _, response = server.app.test_client.get('/users/founder')
    editor_id = response.json['id']
    token = util.create_jwt(editor_id, server.config.secret)

    # get user's id to add to the club
    _, response = server.app.test_client.get('/users/member')
    user_id = response.json['id']

    # give user a Member membership to the club
    _, response = server.app.test_client.put(
        '/memberships/newtest?user_id=' + str(user_id),
        data=json.dumps({
            'members_role': 'Member',
            'position': 'Student'
        }),
        headers={'Authorization': token})

    # now try editing the club with the Member membership
    token = util.create_jwt(user_id, server.config.secret)
    _, response = server.app.test_client.put(
        '/clubs/newtest',
        data=json.dumps({
            'name': 'newtest',
            'description': 'new description',
        }),
        headers={'Authorization': token})
    assert response.status == 403


def test_get_club__success(server):
    _, response = server.app.test_client.get('/clubs/newtest')
    assert response.status == 200
    assert response.json['name'] == 'newtest'
    assert response.json['description'] == 'club with a newer description'
    assert response.json['id'] == 1
    assert isinstance(response.json['created_at'], int)


def test_get_club__failure(server):
    _, response = server.app.test_client.get('/clubs/doesnotexist')
    assert response.status == 404


def test_delete_club__failure(server):
    # get user's id of a Member membership
    _, response = server.app.test_client.get('/users/member')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)

    # fail when a user with a Member membership tries to delete the club
    _, response = server.app.test_client.delete(
        '/clubs/newtest', headers={'Authorization': token})
    assert response.status == 403


def test_delete_club__success(server):
    # deleting clubs requires President privileges
    # therefore use the founder's ID to successfully delete the club
    _, response = server.app.test_client.get('/users/founder')
    editor_id = response.json['id']
    token = util.create_jwt(editor_id, server.config.secret)

    _, response = server.app.test_client.delete(
        '/clubs/newtest', headers={'Authorization': token})
    assert response.status == 204


def test_paginate_clubs__success(server):
    # get founder's id to post a club
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)

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
            }),
            headers={'Authorization': token})
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
