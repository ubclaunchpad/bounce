"""Request handlers for the /users endpoint."""

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint
from ...db import user
from ..resource import validate
from ..resource.user import (GetUserRequest, GetUserResponse, PutUserRequest,
                             PutUserResponse)


class UsersEndpoint(Endpoint):
    """Handles requests to /users."""

    __uri__ = '/users'

    @validate(PutUserRequest, PutUserResponse)
    async def post(self, request):
        """Handles a POST /users request."""
        # Put the user in the DB
        body = request.json
        try:
            user.insert(self.server.db_session, body['full_name'],
                        body['username'], body['email'])
        except IntegrityError:
            raise APIError('User already exists', status=400)
        user_data = user.select_by_username(self.server.db_session,
                                            body['username'])
        return response.json(user_data, status=200)

    @validate(GetUserRequest, GetUserResponse)
    async def get(self, request):
        """Handles a GET /users request."""
        # Fetch user data from DB
        user_data = user.select_by_username(self.server.db_session,
                                            request.args.get('username'))
        if not user_data:
            # Failed to find a user with that username
            raise APIError('No such user', status=404)
        return response.json(user_data, status=200)
