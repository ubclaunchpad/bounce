"""Tests the Bounce API."""

from aiohttp import FormData

from bounce.server.api import util


def test_put_user_image__success(server):
    # Upload image for user whose name is founder
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)
    data = FormData()
    data.add_field('image', open('tests/testdata/large-logo.png', 'rb'))
    _, response = server.app.test_client.put(
        '/users/' + str(user_id) + '/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_put_user_image__failure(server):
    token = util.create_jwt(99, server.config.secret)
    data = FormData()

    # No such user
    _, response = server.app.test_client.put(
        '/users/99/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 404

    # Forbidden (the user is trying to update another user's image)
    _, response = server.app.test_client.put(
        '/users/3/images/profile',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 403

    # Invalid image name
    token = util.create_jwt(3, server.config.secret)
    _, response = server.app.test_client.put(
        '/users/3/images/$%^&*(',
        data=data,
        headers={
            'Authorization': token,
        })
    assert response.status == 400


def test_get_user_image__success(server):
    # get image for user whose name is founder
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    _, response = server.app.test_client.get('/users/' + str(user_id) +
                                             '/images/profile')
    assert response.status == 200


def test_get_user_image__failure(server):
    _, response = server.app.test_client.get('/users/99/images/profile')
    assert response.status == 404


def test_delete_user_image__success(server):
    # get image for user whose name is founder
    _, response = server.app.test_client.get('/users/founder')
    user_id = response.json['id']
    token = util.create_jwt(user_id, server.config.secret)
    _, response = server.app.test_client.delete(
        '/users/' + str(user_id) + '/images/profile',
        headers={
            'Authorization': token,
        })
    assert response.status == 200


def test_delete_user_image__failure(server):
    token = util.create_jwt(99, server.config.secret)
    # No such image
    _, response = server.app.test_client.delete(
        '/users/99/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 404
    # Forbidden (user is trying to delete another user's image)
    _, response = server.app.test_client.delete(
        '/users/3/images/profile', headers={
            'Authorization': token,
        })
    assert response.status == 403
