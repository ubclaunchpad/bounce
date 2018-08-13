"""Request handlers for the /users endpoint."""

from urllib.parse import unquote

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, util, verify_token
from ...db import club, membership
from ..resource import validate
from ..resource.membership import (DeleteMembershipRequest,
                                   GetMembershipRequest, GetMembershipResponse,
                                   PostMembershipRequest, PutMembershipRequest)


class MembershipEndpoint(Endpoint):
    """Handles requests to /memberships/<club_name>."""

    __uri__ = "/memberships/<club_name:string>"

    @validate(GetMembershipRequest, GetMembershipResponse)
    async def get(self, request, club_name):
        """
        Handles a GET /memberships/<club_name>?user_id=<user_id> request
        by returning the membership that associates the given user with the
        given club. If no user ID is given, returns all memberships for the
        given club.
        """
        # Decode the club name
        club_name = unquote(club_name)
        user_id = request.args.get('user_id', None)

        # Make sure the club exists
        club_row = club.select(self.server.db_session, club_name)
        if not club_row:
            raise APIError('No such club', status=404)

        # Fetch the club's memberships
        membership_info = membership.select(
            self.server.db_session, club_name, user_id=user_id)
        return response.json(membership_info, status=200)

    @verify_token()
    @validate(DeleteMembershipRequest, None)
    async def delete(self, request, club_name, id_from_token=None):
        """
        Handles a DELETE /memberships/<club_name>?user_id=<user_id> request
        by deleting the membership that associates the given user with the
        given club. If no user ID is given, deletes all memberships for the
        given club.
        """
        # TODO: fix this when we have user roles set up. A user should only be
        # able to delete their own memberships and memberships on clubs they
        # are an admin/owner of.

        # Decode the club name
        club_name = unquote(club_name)
        user_id = request.args.get('user_id', None)

        if id_from_token != user_id:
            # Regular members can only delete their own memberships
            raise APIError('Forbidden', status=403)

        # Make sure the club exists
        club_row = club.select(self.server.db_session, club_name)
        if not club_row:
            raise APIError('No such club', status=404)

        # Delete the memberships
        membership.delete(self.server.db_session, club_name, user_id=user_id)
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
            raise APIError('Invalid user or club ID', status=400)
        return response.text('', status=201)
