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
            'full_name': 'NewName'
        }),
        headers={'Authorization': token})
    assert response.status == 200
    assert response.json['username'] == username
    assert response.json['full_name'] == 'NewName'
    assert response.json['id'] == 1
    assert response.json['email'] == 'test@test.com'
    assert response.json['bio'] == 'my name is test. I am a cs major'
    assert isinstance(response.json['created_at'], int)


def test_put_user_update_email__success(server):
    username = 'test'
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'full_name': 'New Name',
            'password': 'Val1dPassword!',
            'email': 'newemail@test.com',
        }),
        headers={'Authorization': token})
    assert response.status == 200
    assert response.json['username'] == username
    assert response.json['full_name'] == 'New Name'
    assert response.json['email'] == 'newemail@test.com'
    assert response.json['id'] == 1
    assert isinstance(response.json['created_at'], int)


def test_put_user_update_email__failure(server):
    username = 'test'
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'garbage': True
        }),
        headers={'Authorization': token})
    assert response.status == 400

    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'email': 'newemailfail@test.com'
        }),
        headers={'Authorization': token})
    assert response.status == 400

    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'email': 'newemailfail@test.com',
            'password': 'WrongPassword!'
        }),
        headers={'Authorization': token})
    assert response.status == 401

    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'email': 'newemailfail@test.com',
            'password': 'Val1dPassword!',
            'new_password': 'NewVal1dPassword!'
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


def test_put_users_update_password__success(server):
    username = 'test'
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'password': 'Val1dPassword!',
            'new_password': 'Val1dPassword!s',
        }),
        headers={'Authorization': token})
    assert response.status == 200


def test_put_users_update_password__failure(server):
    username = 'test'
    token = util.create_jwt(1, server.config.secret)
    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'new_password': 'Val1dPassword!123',
        }),
        headers={'Authorization': token})
    assert response.status == 400

    _, response = server.app.test_client.put(
        f'/users/{username}',
        data=json.dumps({
            'password': 'WrongPassword!',
            'new_password': 'Val1dPassword!123',
        }),
        headers={'Authorization': token})
    assert response.status == 401


def test_login__success(server):
    _, response = server.app.test_client.post(
        '/auth/login',
        data=json.dumps({
            'username': 'test',
            'password': 'Val1dPassword!s'
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


def test_put_club_image__success(server):
    # POST a dummy user to add a profile image to
    token = util.create_jwt(2, server.config.secret)
    data = FormData()
    data.add_field('image', open('tests/testdata/large-logo.png', 'rb'))
    _, response = server.app.test_client.put(
        '/clubs/test/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_put_club_image__failure(server):
    # No such club
    token = util.create_jwt(2, server.config.secret)
    data = FormData()
    _, response = server.app.test_client.put(
        '/clubs/newtest/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 404
    # Invalid image name
    _, response = server.app.test_client.put(
        '/clubs/test/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 400

    data.add_field('image', open('tests/testdata/gif-file.gif', 'rb'))

    _, response = server.app.test_client.put(
        '/clubs/test/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 400

    data = FormData()
    data.add_field('image', open('tests/testdata/large-png-file.png', 'rb'))
    _, response = server.app.test_client.put(
        '/clubs/test/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 400

    data = FormData()
    data.add_field('image', open('tests/testdata/large-logo.png', 'rb'))
    _, response = server.app.test_client.put(
        '/clubs/test/images/@$@3(',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 400


def test_get_club_image__success(server):
    _, response = server.app.test_client.get('/clubs/test/images/profile')
    assert response.status == 200


def test_get_club_image__failure(server):
    # No such club
    _, response = server.app.test_client.get('/clubs/newTest/images/profile')
    assert response.status == 404

    _, response = server.app.test_client.get('/clubs/test/images/adw0@?dow')
    assert response.status == 400


def test_delete_club_image__success(server):
    token = util.create_jwt(2, server.config.secret)
    _, response = server.app.test_client.delete(
        '/clubs/test/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_delete_club_image__failure(server):
    token = util.create_jwt(2, server.config.secret)
    # No such image
    _, response = server.app.test_client.delete(
        '/clubs/test/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 404

    _, response = server.app.test_client.delete(
        '/clubs/test/images/adw0@?dow', headers={
            'Authorization': token,
        })
    assert response.status == 400
    # TODO : Uncomment this portion of code once memberships code is merged in
    # # Forbidden (user is trying to delete image of an unrelated club)
    # _, response = server.app.test_client.delete(
    #     '/clubs/newtest/images/profile', headers={
    #         'Authorization': token,
    #     })
    # assert response.status == 403


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
    club_info = [('UBC Launch Pad', 'software engineering team'),
                 ('envision', 'something'), ('UBC biomed', 'something else')]
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
    _, response = server.app.test_client.get('/clubs/search?size=2')
    assert response.status == 200
    body = response.json
    assert body.get('result_count') == 4
    assert body.get('page') == 0
    assert body.get('total_pages') == 2


def test_paginate_clubs__failure(server):
    _, response = server.app.test_client.get('/clubs/search?size=0')
    assert response.status == 400
    _, response = server.app.test_client.get('/clubs/search?size=25')
    assert response.status == 400


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
            'password': 'Val1dPassword!',
            'bio': 'my name is test. I am a cs major'
        }))
    token = util.create_jwt(5, server.config.secret)
    data = FormData()
    data.add_field('image', open('tests/testdata/large-logo.png', 'rb'))
    _, response = server.app.test_client.put(
        '/users/5/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_put_user_image__failure(server):
    token = util.create_jwt(6, server.config.secret)
    data = FormData()
    # No such user
    _, response = server.app.test_client.put(
        '/users/6/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 404
    # Forbidden (the user is trying to update another user's image)
    _, response = server.app.test_client.put(
        '/users/5/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 403
    # Invalid image name
    token = util.create_jwt(2, server.config.secret)
    _, response = server.app.test_client.put(
        '/users/5/images/$%^&*(',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 400


def test_get_user_image__success(server):
    _, response = server.app.test_client.get('/users/5/images/profile')
    assert response.status == 200


def test_get_user_image__failure(server):
    _, response = server.app.test_client.get('/users/6/images/profile')
    assert response.status == 404


def test_delete_user_image__success(server):
    token = util.create_jwt(5, server.config.secret)
    _, response = server.app.test_client.delete(
        '/users/5/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_delete_user_image__failure(server):
    token = util.create_jwt(6, server.config.secret)
    # No such image
    _, response = server.app.test_client.delete(
        '/users/6/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 404
    # Forbidden (user is trying to delete another user's image)
    _, response = server.app.test_client.delete(
        '/users/5/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 403


def test_put_memberships__success(server):
    _, response = server.app.test_client.post(
        '/users',
        data=json.dumps({
            'username': 'mrguy',
            'full_name': 'Hello WOrld',
            'email': 'something@anotherthing.com',
            'password': 'Val1dPassword!',
            'bio': 'I am an eng student, rip'
        }))
    assert response.status == 201
    token = util.create_jwt(2, server.config.secret)
    _, response = server.app.test_client.put(
        '/memberships/newtest?user_id=2', headers={'Authorization': token})
    assert response.status == 201


def test_put_memberships__failure(server):
    token = util.create_jwt(2, server.config.secret)
    _, response = server.app.test_client.put(
        '/memberships/doesnotexist?user_id=2',
        headers={'Authorization': token})
    assert response.status == 400


def test_get_memberships__success(server):
    _, response = server.app.test_client.get('/memberships/newtest?user_id=2')
    assert response.status == 200
    assert len(response.json) == 1
    membership = response.json['results'][0]
    assert membership['user_id'] == 2
    assert membership['full_name'] == 'matt gin'
    assert membership['username'] == 'ginsstaahh'
    assert isinstance(membership['created_at'], int)


def test_delete_membership__failure(server):
    token = util.create_jwt(3, server.config.secret)
    _, response = server.app.test_client.delete(
        '/memberships/newtest?user_id=2', headers={'Authorization': token})
    assert response.status == 403


def test_delete_membership__success(server):
    token = util.create_jwt(2, server.config.secret)
    _, response = server.app.test_client.delete(
        '/memberships/newtest?user_id=2', headers={'Authorization': token})
    assert response.status == 204
