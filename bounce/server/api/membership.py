"""Request handlers for the /users endpoint."""

from urllib.parse import unquote

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, verify_token
from ...db import club, membership
from ..resource import validate
from ..resource.membership import (DeleteMembershipRequest,
                                   GetMembershipRequest, GetMembershipResponse,
                                   PutMembershipRequest)


class MembershipEndpoint(Endpoint):
    """Handles requests to /memberships/<club_name>."""

    __uri__ = "/memberships/<club_name:string>"

    @validate(GetMembershipRequest, GetMembershipResponse)
    async def get(self, request, club_name):
        """
        Handles a GET /memberships/<club_name>?user_id=<user_id>&access=<role> request
        by returning the membership that associates the given user with the
        given club. If no user ID is given, returns all memberships for the
        given club.
        """
        # Decode the club name
        club_name = unquote(club_name)
        user_id = request.args.get('user_id', None)[0]
        editor_role = request.args.get('access')

        # Make sure the club exists
        club_row = club.select(self.server.db_session, club_name)
        if not club_row:
            raise APIError('No such club', status=404)

        # Fetch the club's memberships
        membership_info = membership.select(self.server.db_session, club_name,
                                            user_id, editor_role)
        return response.json(membership_info, status=200)

    # pylint: disable=unused-argument
    @verify_token()
    @validate(PutMembershipRequest, None)
    async def put(self, request, club_name, id_from_token=None):
        """Handles a PUT /memberships/<club_name>?user_id=<user_id>&access=<role>
        creating or updating the membership for the given user and club."""
        # Decode the club name
        club_name = unquote(club_name)
        user_id = 0  # TODO: default user id
        access = request.args.get('access')
        body = request.json
        # body = util.strip_whitespace(request.json)
        members_role = body.get('role')
        position = body.get('position')
        try:
            user_id = int(request.args.get('user_id')[0])
        except Exception:
            raise APIError('Invalid user ID', status=400)
        try:
            membership.insert(self.server.db_session, club_name, user_id,
                              access, members_role, position)
        except IntegrityError:
            raise APIError('Invalid user or club ID', status=400)
        return response.text('', status=201)

    # pylint: enable=unused-argument

    @verify_token()
    @validate(DeleteMembershipRequest, None)
    async def delete(self, request, club_name, id_from_token=None):
        """
        Handles a DELETE /memberships/<club_name>?user_id=<id>&editor_id=<id>editor_role=<role>&members_role=<role> request
        by deleting the membership that associates the given user with the
        given club.
        """
        # TODO: fix this when we have user roles set up. A user should only be
        # able to delete their own memberships and memberships on clubs they
        # are an admin/owner of.

        # Decode the club name
        club_name = unquote(club_name)
        user_id = 0  # TODO: default value
        editors_id = int(request.args.get('editor_id')[0])
        editors_role = request.args.get('editor_role')[0]
        members_role = request.args.get('member_role')[0]
        try:
            user_id = int(request.args.get('user_id')[0])
        except ValueError:
            raise APIError('Invalid user ID', status=400)

        if id_from_token != user_id:
            # Regular members can only delete their own memberships
            raise APIError('Forbidden', status=403)

        # Make sure the club exists
        club_row = club.select(self.server.db_session, club_name)
        if not club_row:
            raise APIError('No such club', status=404)

        # Delete the memberships
        if user_id:
            membership.delete(self.server.db_session, club_name, editors_id,
                              user_id, editors_role, members_role)
            return response.text('', status=204)
        else:
            membership.delete_all(self.server.db_session, club_name,
                                  editors_role, members_role)
            return response.text('', status=204)
