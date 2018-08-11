"""Request handlers for the /users endpoint."""

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, util, verify_token
from ...db import membership
from ..resource import validate
from ..resource.membership import (GetMembershipResponse,
                                   PostMembershipRequest, PutMembershipRequest)


class MembershipEndpoint(Endpoint):
    """Handles requests to /memberships/<club_id>."""

    __uri__ = "/memberships/<club_id:string>"

    @verify_token()
    async def delete(self, _, club_id, id_from_token=None):
        """
        Handles a DELETE /memberships/<club_id> request by deleting the
        user's membership with the club with the given id.
        """
        # Fetch the membership using the user ID and club ID
        membership_row = membership.select(self.server.db_session, club_id,
                                           id_from_token)
        if not membership_row:
            raise APIError('No such membership', status=404)
        # Delete the membership
        membership.delete(self.server.db_session, club_id, id_from_token)
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
