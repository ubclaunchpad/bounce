"""Endpoints for authenticating users."""

from sanic import response

from . import APIError, Endpoint, util
from ...db import user
from ..resource import validate
from ..resource.auth import AuthenticateUserRequest, AuthenticateUserResponse


class LoginEndpoint(Endpoint):
    """Handles requests to /auth/login."""

    __uri__ = '/auth/login'

    @validate(AuthenticateUserRequest, AuthenticateUserResponse)
    async def post(self, session, request):
        """Handles a POST /auth/login request by validating the user's
        credentials and issuing them a JSON Web Token."""
        body = request.json

        # Fetch the user's info from the DB
        user_row = user.select(session, body['username'])
        if not user_row:
            raise APIError('Unauthorized', status=401)

        # Check that the user's password is correct
        if not util.check_password(body['password'], user_row.secret):
            raise APIError('Unauthorized', status=401)

        # Issue the user a token
        token = util.create_jwt(user_row.identifier, self.server.config.secret)
        return response.json({'token': token}, status=200)
