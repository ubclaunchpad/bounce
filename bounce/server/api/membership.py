"""Request handlers for the /users endpoint."""

from urllib.parse import unquote

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, verify_token
from ...db import club, membership
from ..resource import validate
from ..resource.membership import (
    DeleteMembershipRequest, GetMembershipsRequest, GetMembershipsResponse,
    PutMembershipRequest)


class MembershipEndpoint(Endpoint):
    """Handles requests to /memberships/<club_name>."""

    __uri__ = "/memberships/<club_name:string>"

    @validate(GetMembershipsRequest, GetMembershipsResponse)
    async def get(self, session, request, club_name):
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
        club_row = club.select(session, club_name)
        if not club_row:
            raise APIError('No such club', status=404)

        # Fetch the club's memberships
        results = membership.select(
            session, club_name, user_id=user_id)
        info = {'results': results}
        return response.json(info, status=200)

    # pylint: disable=unused-argument
    @verify_token()
    @validate(PutMembershipRequest, None)
    async def put(self, session, request, club_name, id_from_token=None):
        """Handles a PUT /memberships/<club_name>?user_id=<user_id> request by
        creating or updating the membership for the given user and club."""
        # Decode the club name
        club_name = unquote(club_name)
        try:
            user_id = int(request.args.get('user_id'))
        except Exception:
            raise APIError('Invalid user ID', status=400)
        try:
            membership.insert(session, club_name, user_id)
        except IntegrityError:
            raise APIError('Invalid user or club ID', status=400)
        return response.text('', status=201)

    # pylint: enable=unused-argument

    @verify_token()
    @validate(DeleteMembershipRequest, None)
    async def delete(self, session, request, club_name, id_from_token=None):
        """
        Handles a DELETE /memberships/<club_name>?user_id=<user_id> request
        by deleting the membership that associates the given user with the
        given club..
        """
        # TODO: fix this when we have user roles set up. A user should only be
        # able to delete their own memberships and memberships on clubs they
        # are an admin/owner of.

        # Decode the club name
        club_name = unquote(club_name)
        try:
            user_id = int(request.args.get('user_id'))
        except ValueError:
            raise APIError('Invalid user ID', status=400)

        if id_from_token != user_id:
            # Regular members can only delete their own memberships
            raise APIError('Forbidden', status=403)

        # Make sure the club exists
        club_row = club.select(session, club_name)
        if not club_row:
            raise APIError('No such club', status=404)

        # Delete the memberships
        membership.delete(session, club_name, user_id=user_id)
        return response.text('', status=204)
