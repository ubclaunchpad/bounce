"""Request handlers for the /users endpoint."""

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, util, verify_token
from ...db import user
from ..resource import validate
from ..resource.user import GetUserResponse, PostUsersRequest, PutUserRequest


class UserEndpoint(Endpoint):
    """Handles requests to /users/<username>."""

    __uri__ = "/users/<username:string>"

    @validate(None, GetUserResponse)
    async def get(self, _, username):
        """Handles a GET /users/<username> request by returning the user with
        the given username."""
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
        body = request.json
        # Make sure the ID from the token is for the user we're updating
        user_row = user.select(self.server.db_session, username)
        if not user_row:
<<<<<<< HEAD
            raise APIError('No such user', status=404)
=======
            raise APIError('No such user', status=400)
>>>>>>> Add user authentication
        if user_row.identifier != id_from_token:
            raise APIError('Forbidden', status=403)
        # Update the user
        updated_user = user.update(
            self.server.db_session,
            username,
            full_name=body.get('full_name', None),
            email=body.get('email', None))
        # Returns the updated user info
        return response.json(updated_user.to_dict(), status=200)

    @verify_token()
    async def delete(self, _, username, id_from_token=None):
        """Handles a DELETE /users/<username> request by deleting the user with
        the given username. """
        # Make sure the ID from the token is for the user we're deleting
        user_row = user.select(self.server.db_session, username)
        if not user_row:
<<<<<<< HEAD
            raise APIError('No such user', status=404)
=======
            raise APIError('No such user', status=400)
>>>>>>> Add user authentication
        elif user_row.identifier != id_from_token:
            raise APIError('Forbidden', status=403)
        # Delete the user
        user.delete(self.server.db_session, username)
        return response.text('', status=204)


class UsersEndpoint(Endpoint):
    """Handles requests to /users."""

    __uri__ = '/users'

    @validate(PostUsersRequest, None)
    async def post(self, request):
        """Handles a POST /users request by creating a new user."""
        body = request.json
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
