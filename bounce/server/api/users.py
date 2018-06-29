"""Request handlers for the /users endpoint."""

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint
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
        user_data = user.select(self.server.db_session, username)
        if not user_data:
            # Failed to find a user with that username
            raise APIError('No such user', status=404)
        return response.json(user_data, status=200)

    @validate(PutUserRequest, GetUserResponse)
    async def put(self, request, username):
        """Handles a PUT /users/<username> request by updating the user with
        the given username and returning the updated user info."""
        body = request.json
        updated_user = user.update(
            self.server.db_session,
            username,
            full_name=body.get('full_name', None),
            email=body.get('email', None))
        return response.json(updated_user, status=200)

    async def delete(self, _, username):
        """Handles a DELETE /users/<username> request by deleting the user with
        the given username. """
        user.delete(self.server.db_session, username)
        return response.text('', status=204)


class UsersEndpoint(Endpoint):
    """Handles requests to /users."""

    __uri__ = '/users'

    @validate(PostUsersRequest, None)
    async def post(self, request):
        """Handles a POST /users request by creating a new user."""
        # Put the user in the DB
        body = request.json
        try:
            user.insert(self.server.db_session, body['full_name'],
                        body['username'], body['email'])
        except IntegrityError:
            raise APIError('User already exists', status=400)
        return response.text('', status=201)
