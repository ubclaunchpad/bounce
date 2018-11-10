"""Request handlers for the /users endpoint."""

import os

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, util, verify_token
from ...db import image, user
from ...db.image import EntityType
from ..resource import validate
from ..resource.user import GetUserResponse, PostUsersRequest, PutUserRequest

# Maximum number of bytes in an image upload
IMAGE_SIZE_LIMIT = 1000000


class UserEndpoint(Endpoint):
    """Handles requests to /users/<username>."""

    __uri__ = "/users/<username:string>"

    @validate(None, GetUserResponse)
    async def get(self, _, username):
        """Handles a GET /users/<username> request by returning the user with
        the given membership."""
        # Fetch user data from DB
        user_row = user.select(self.server.db_session, username)
        if not user_row:
            # Failed to find a user with that username
            raise APIError('No such user', status=404)
        return response.json(user_row.to_dict(), status=200)

    @verify_token()
    @validate(PutUserRequest, GetUserResponse)
    async def put(self, request, username, id_from_token=None):
        """Handles a PUT /users/<username> request by updating the user with
        the given username and returning the updated user info. """
        body = util.strip_whitespace(request.json)
        secret = None
        email = None
        # Make sure the ID from the token is for the user we're updating
        user_row = user.select(self.server.db_session, username)
        if not user_row:
            raise APIError('No such user', status=404)
        if user_row.identifier != id_from_token:
            raise APIError('Forbidden', status=403)
        if body.get('email'):
            # Check that user password is provided
            if not body.get('password'):
                raise APIError('Password not provided', status=400)
            # Check that user's password is correct
            if not util.check_password(body['password'], user_row.secret):
                raise APIError('Unauthorized', status=401)
            if body.get('new_password'):
                raise APIError(
                    'New password should not be provided for email change',
                    status=400)
            email = body['email']
        elif body.get('new_password'):
            # Check that user current password is provided
            if not body.get('password'):
                raise APIError('Current Password not provided', status=400)
            # Check that the user's password is correct
            if not util.check_password(body['password'], user_row.secret):
                raise APIError('Unauthorized', status=401)
            # Make sure the password is valid (no need
            # to check email, this is done
            # by a jsonschema formatter)
            if not util.validate_password(body['new_password']):
                raise APIError('Invalid new password', status=400)
            # Create a secret from the user's password
            #  that we can use to securely
            # verify their password when they log in
            secret = util.hash_password(body['new_password'])
        # Update the user
        updated_user = user.update(
            self.server.db_session,
            username,
            secret=secret,
            full_name=body.get('full_name', None),
            email=email)
        # Returns the updated user info
        return response.json(updated_user.to_dict(), status=200)

    @verify_token()
    async def delete(self, _, username, id_from_token=None):
        """Handles a DELETE /users/<username> request by deleting the user with
        the given username. """
        # Make sure the ID from the token is for the user we're deleting
        user_row = user.select(self.server.db_session, username)
        if not user_row:
            raise APIError('No such user', status=404)
        elif user_row.identifier != id_from_token:
            raise APIError('Forbidden', status=403)
        # Delete the user
        user.delete(self.server.db_session, username)
        # Delete the user's images
        image.delete_dir(self.server.config.image_dir, EntityType.USER,
                         user_row.identifier)
        return response.text('', status=204)


class UsersEndpoint(Endpoint):
    """Handles requests to /users."""

    __uri__ = '/users'

    @validate(PostUsersRequest, None)
    async def post(self, request):
        """Handles a POST /users request by creating a new user."""
        body = util.strip_whitespace(request.json)
        # Make sure the username is valid
        if not util.validate_username(body['username']):
            raise APIError('Invalid username', status=400)
        # Make sure the password is valid (no need to check email, this is done
        # by a jsonschema formatter)
        if not util.validate_password(body['password']):
            raise APIError('Invalid password', status=400)
        # Create a secret from the user's password that we can use to securely
        # verify their password when they log in
        secret = util.hash_password(body['password'])
        # Put the user in the DB
        try:
            user.insert(self.server.db_session, body['full_name'],
                        body['username'], secret, body['email'])
        except IntegrityError:
            raise APIError('User already exists', status=409)
        return response.text('', status=201)


class UserImagesEndpoint(Endpoint):
    """Handles requests to /users/<user_id>/images/<image_name>."""

    __uri__ = '/users/<user_id>/images/<image_name>'

    async def get(self, _, user_id, image_name):
        """
        Handles a GET /users/<user_id>/images/<image_name> request
        by returning the user's image with the given name.
        """
        if not util.check_image_name(image_name):
            raise APIError('Invalid image name', status=400)
        try:
            return await response.file(
                os.path.join(self.server.config.image_dir,
                             EntityType.USER.value, user_id, image_name))
        except FileNotFoundError:
            raise APIError('No such image', status=404)

    @verify_token()
    async def put(self, request, user_id, image_name, id_from_token=None):
        """
        Handles a PUT /users/<user_id>/images/<image_name> request
        by updating the image at the given path.
        """
        # For now, only allow users to upload profile pictures
        if image_name != 'profile' or not util.check_image_name(image_name):
            raise APIError('Invalid image name', status=400)

        # Make sure the user is updating an image they own
        user_info = user.select_by_id(self.server.db_session, user_id)
        if not user_info:
            raise APIError('No such image', status=404)
        if not user_info.identifier == id_from_token:
            raise APIError('Forbidden', status=403)

        # Save the image
        image_upload = request.files.get('image')
        if not image_upload:
            raise APIError('No image provided', status=400)
        if (image_upload.type != 'image/png'
                and image_upload.type != 'image/jpeg'):
            raise APIError(
                'Only png and jpeg images are supported', status=400)
        if len(image_upload.body) > IMAGE_SIZE_LIMIT:
            raise APIError('Image too large', status=400)
        try:
            image.save(self.server.config.image_dir, EntityType.USER, user_id,
                       image_name, image_upload.body)
        except FileExistsError:
            raise APIError('No such image', status=404)

        return response.text('', status=200)

    @verify_token()
    async def delete(self, _, user_id, image_name, id_from_token=None):
        """Handles a DETELE by deleting the user's image by the given name."""
        if not util.check_image_name(image_name):
            raise APIError('Invalid image name', status=400)
        # Make sure the user is deleting their own image
        user_info = user.select_by_id(self.server.db_session, user_id)
        if not user_info:
            raise APIError('No such image', status=404)
        if not user_info.identifier == id_from_token:
            raise APIError('Forbidden', status=403)
        try:
            image.delete(
                self.server.config.image_dir,
                EntityType.USER,
                user_id,
                image_name,
                must_exist=True)
        except FileExistsError:
            raise APIError('No such image', status=404)
        return response.text('', status=200)
