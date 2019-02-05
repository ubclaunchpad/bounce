"""Tests the Bounce API."""

import json

from aiohttp import FormData

from bounce.server.api import util


def test_put_memberships__success(server):
    # to put a new membership, we will first need to create a club
    # to add a membership to.  A founder user will be needed to create
    # the club

    # get user whose name is founder and get his id to pass in with his token
    _, response = server.app.test_client.get('/users/founder')
    founder_id = response.json['id']
    founder_token = util.create_jwt(founder_id, server.config.secret)

    _, response = server.app.test_client.post(
        '/clubs',
        data=json.dumps({
            'name': 'testclub',
            'description': 'club called test',
            'website_url': 'club.com',
            'facebook_url': 'facebook.com/test',
            'instagram_url': 'instagram.com/test',
            'twitter_url': 'twitter.com/test',
        }),
        headers={'Authorization': founder_token})

    # add an Admin membership to another user
    # first create user whom we will give an Admin membership to
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'admin',
            'full_name': 'admin guy',
            'email': 'my@name.com',
            'password': 'Val1dPassword!'
        }))
    # get his id
    _, response = server.app.test_client.get('/users/admin')
    admin_id = response.json['id']
    # add Admin membership
    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=' + str(admin_id),
        data=json.dumps({
            'members_role': 'Admin',
            'position': 'tech lead'
        }),
        headers={'Authorization': founder_token})
    assert response.status == 201

    # edit same Admin membership
    # _, response = server.app.test_client.put(
    #     '/memberships/testclub?user_id=' + str(admin_id),
    #     data=json.dumps({
    #         'members_role': 'Admin',
    #         'position': 'former tech lead'
    #     }),
    #     headers={'Authorization': founder_token})
    # assert response.status == 201

    # add a Member membership to another user.
    # use the Admin membership to put entry into the memberships table
    admin_token = util.create_jwt(admin_id, server.config.secret)
    _, response = server.app.test_client.get('/users/member')
    member_id = response.json['id']

    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=' + str(member_id),
        data=json.dumps({
            'members_role': 'Member',
            'position': 'club member'
        }),
        headers={'Authorization': admin_token})
    assert response.status == 201

    # edit the same Member membership
    # _, response = server.app.test_client.put(
    #     '/memberships/testclub?user_id=' + str(member_id),
    #     data=json.dumps({
    #         'members_role': 'Member',
    #         'position': 'former club member'
    #     }),
    #     headers={'Authorization': admin_token})
    # assert response.status == 201


def test_put_memberships__failure(server):
    # Club does not exist
    _, response = server.app.test_client.get('/users/founder')
    founder_id = response.json['id']
    token = util.create_jwt(founder_id, server.config.secret)
    _, response = server.app.test_client.put(
        '/memberships/doesnotexist?user_id=3',
        data=json.dumps({
            'members_role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': token})
    assert response.status == 400

    # User does not exist
    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=99',
        data=json.dumps({
            'members_role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': token})
    assert response.status == 400

    # Permission denied.  A user with an Admin membership cannot
    # edit a President membership
    _, response = server.app.test_client.get('/users/admin')
    admin_id = response.json['id']
    admin_token = util.create_jwt(admin_id, server.config.secret)
    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=' + str(founder_id),
        data=json.dumps({
            'members_role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': admin_token})
    assert response.status == 403

    # Permission denied.  A user with an Admin membership cannot
    # add a President membership

    # Create new user to attempt adding into database
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'president2',
            'full_name': 'president guy',
            'email': 'new@email.com',
            'password': 'Val1dPassword!'
        }))

    # get his id
    _, response = server.app.test_client.get('/users/president2')
    president_id = response.json['id']
    # add President membership
    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=' + str(president_id),
        data=json.dumps({
            'members_role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': admin_token})
    assert response.status == 403

    # Permission denied.  A user with a Membership membership cannot
    # edit an Admin membership
    _, response = server.app.test_client.get('/users/member')
    member_id = response.json['id']
    token = util.create_jwt(member_id, server.config.secret)
    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=' + str(admin_id),
        data=json.dumps({
            'members_role': 'President',
            'position': 'VP'
        }),
        headers={'Authorization': token})
    assert response.status == 403

    # Permission denied.  A user with a Membership membership cannot
    # add an Admin membership
    _, response = server.app.test_client.get('/users/member')
    member_id = response.json['id']
    member_token = util.create_jwt(member_id, server.config.secret)

    # Create new user to attempt adding into database
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'admin2',
            'full_name': 'admin guy',
            'email': 'mynew@email.com',
            'password': 'Val1dPassword!'
        }))
    # get his id
    _, response = server.app.test_client.get('/users/admin2')
    admin_id = response.json['id']
    # add Admin membership
    _, response = server.app.test_client.put(
        '/memberships/testclub?user_id=' + str(admin_id),
        data=json.dumps({
            'members_role': 'Admin',
            'position': 'tech lead 2'
        }),
        headers={'Authorization': member_token})
    assert response.status == 403


def test_get_memberships__success(server):
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)
    # get all memberships
    _, response = server.app.test_client.get(
        '/memberships/testclub', headers={'Authorization': token})
    assert response.status == 200
    # check that the two membership were obtained
    assert len(response.json) == 3

    # get founder's membership
    _, response = server.app.test_client.get(
        '/memberships/testclub?user_id=' + str(user_id),
        headers={'Authorization': token})
    membership = response.json[0]
    assert membership['user_id'] == 2
    assert membership['full_name'] == 'Test Guy'
    assert membership['username'] == 'founder'
    assert isinstance(membership['created_at'], int)

    # get member's membership
    _, response = server.app.test_client.get(
        '/memberships/testclub?user_id=' + str(user_id + 1),
        headers={'Authorization': token})


def test_get_membership__failure(server):
    # club does not exist
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)
    _, response = server.app.test_client.get(
        '/memberships/doesnotexist?user_id=3',
        headers={'Authorization': token})
    assert response.status == 404

    # Permission denied
    _, response = server.app.test_client.get('/users/member')
    editor_id = response.json['id']
    token = util.create_jwt(99, server.config.secret)
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    _, response = server.app.test_client.get(
        '/memberships/testclub?user_id=' + str(user_id),
        headers={'Authorization': token})
    assert response.status == 403


def test_delete_membership__failure(server):
    # Members can't delete other memberships other than their own
    _, response = server.app.test_client.get('/users/member')
    editor_id = response.json['id']
    token = util.create_jwt(editor_id, server.config.secret)
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    _, response = server.app.test_client.delete(
        '/memberships/testclub?user_id=' + str(user_id),
        headers={'Authorization': token})
    assert response.status == 403

    # Invalid ID
    _, response = server.app.test_client.delete(
        '/memberships/testclub?user_id=99', headers={'Authorization': token})
    assert response.status == 400

    # Invalid club
    _, response = server.app.test_client.delete(
        '/memberships/doesnotexist?user_id=' + str(user_id),
        headers={'Authorization': token})
    assert response.status == 404


def test_delete_membership__success(server):
    # Presidents can delete members
    _, response = server.app.test_client.get('/users/founder')
    editor_id = response.json['id']
    _, response = server.app.test_client.get('/users/member')
    token = util.create_jwt(editor_id, server.config.secret)
    user_id = response.json['id']
    _, response = server.app.test_client.delete(
        '/memberships/testclub?user_id=' + str(user_id),
        headers={'Authorization': token})
    assert response.status == 201
