"""Tests the Bounce API."""

import json

from aiohttp import FormData

from bounce.server.api import util


def test_put_memberships__success(server):
    # create a club to add a membership to
    _, response = server.app.test_client.post(
        '/clubs',
        data=json.dumps({
            'name': 'testclub',
            'description': 'club called test',
            'website_url': 'club.com',
            'facebook_url': 'facebook.com/test',
            'instagram_url': 'instagram.com/test',
            'twitter_url': 'twitter.com/test',
        }))

    # use the dummy user's id created from test_put_user_image__success
    token = util.create_jwt(3, server.config.secret)
    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=3&access=President',
        data=json.dumps({
            'role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': token})
    assert response.status == 201


def test_put_memberships__failure(server):
    # TODO: add permission error
    token = util.create_jwt(3, server.config.secret)
    _, response = server.app.test_client.put(
        '/memberships/doesnotexist?user_id=3&access=President',
        data=json.dumps({
            'role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': token})
    assert response.status == 400


def test_get_memberships__success(server):
    # TODO: add permission error
    _, response = server.app.test_client.get(
        '/memberships/testclub?user_id=3&access=President')
    assert response.status == 200
    assert len(response.json) == 1
    membership = response.json[0]
    assert membership['user_id'] == 3
    assert membership['full_name'] == 'Test Guy'
    assert membership['username'] == 'test'
    assert isinstance(membership['created_at'], int)


def test_delete_membership__failure(server):
    # TODO: Add permission error
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.delete(
        '/memberships/testclub?user_id=3&editor_id=3&editor_role=President&member_role=President',
        headers={'Authorization': token})
    assert response.status == 403


def test_delete_membership__success(server):
    token = util.create_jwt(3, server.config.secret)
    _, response = server.app.test_client.delete(
        '/memberships/testclub?user_id=3&editor_id=3&editor_role=President&member_role=President',
        headers={'Authorization': token})
    assert response.status == 204
