"""Tests the Bounce API."""

import json

from aiohttp import FormData

from bounce.server.api import util


def test_put_memberships__success(server):
    # to put a new membership, we will first need to create a club 
    # to add a membership to.  A founder user will be needed to create
    # the club

    # get user whose name is test2 and get his id to pass in with his token
    _, response = server.app.test_client.get('/users/test2')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)
    
    _, response = server.app.test_client.post(
        '/clubs',
        data=json.dumps({
            'name': 'testclub',
            'description': 'club called test',
            'website_url': 'club.com',
            'facebook_url': 'facebook.com/test',
            'instagram_url': 'instagram.com/test',
            'twitter_url': 'twitter.com/test',
        }), headers={
            'Authorization': token})

    # add a President membership to another user who is not the founder
    import pdb
    pdb.set_trace()
    _, response = server.app.test_client.get('/users/mattgin')
    user_id = response.json['id']

    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=' + str(user_id),
        data=json.dumps({
            'members_role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': token})
    assert response.status == 201


def test_put_memberships__failure(server):
    # Club does not exist
    token = util.create_jwt(3, server.config.secret)
    _, response = server.app.test_client.put(
        '/memberships/doesnotexist?user_id=3&access=President',
        data=json.dumps({
            'role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': token})
    assert response.status == 400

    # Permission denied
    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=3&access=Member',
        data=json.dumps({
            'role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': token})
    assert response.status == 403


def test_get_memberships__success(server):
    _, response = server.app.test_client.get(
        '/memberships/testclub?user_id=3&access=President')
    assert response.status == 200
    assert len(response.json) == 1
    membership = response.json[0]
    assert membership['user_id'] == 3
    assert membership['full_name'] == 'Test Guy'
    assert membership['username'] == 'test'
    assert isinstance(membership['created_at'], int)


def test_get_membership__failure(server):
    # Permission denied
    _, response = server.app.test_client.get('/memberships/testclub?user_id=3')
    assert response.status == 403


def test_delete_membership__failure(server):
    # Members can't delete other memberships
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.delete(
        '/memberships/testclub?user_id=3&editor_id=1&editor_role=Member&member_role=President',
        headers={'Authorization': token})
    assert response.status == 403


def test_delete_membership__success(server):
    token = util.create_jwt(3, server.config.secret)
    _, response = server.app.test_client.delete(
        '/memberships/testclub?user_id=3&editor_id=3&editor_role=President&member_role=President',
        headers={'Authorization': token})
    assert response.status == 204
