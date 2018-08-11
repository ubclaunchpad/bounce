'''Create a post method for a Memberships endpoint in bounce/server/api/memberships.py (see users.py as an example).'''

"""Request handlers for the /users endpoint."""
#???
from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, util, verify_token
from ...db import membership
from ..resource import validate
from ..resource.membership import GetMembershipResponse, PostMembershipRequest, PutMembershipRequest


class MembershipEndpoint(Endpoint):
    """Handles requests to /memberships/<membership>."""

    __uri__ = "/memberships/<membership:string>"

    @verify_token()
    async def delete(self, _, id):
        """Handles a DELETE /memberships/<membership> request by deleting the membership with
        the given id. """
        # Make sure the ID from the token is for the membership we're deleting
        membership_row = membership.select(self.server.db_session, id)
        if not membership_row:
            raise APIError('No such membership', status=404)
        elif membership_row.identifier != id:
            raise APIError('Forbidden', status=403)
        # Delete the user
        membership.delete(self.server.db_session, id)
        return response.text('', status=204)


class MembershipsEndpoint(Endpoint):
    """Handles requests to /memberships."""

    __uri__ = '/memberships'

    @validate(PostMembershipRequest, None)
    async def post(self, request):
        """Handles a POST /users request by creating a new user."""
        body = request.json
        # Put the membership in the DB
        try:
            membership.insert(self.server.db_session, body['user_id'],
                        body['club_id'])
        except IntegrityError:
            raise APIError('Membership already exists', status=409)
        return response.text('', status=201)
