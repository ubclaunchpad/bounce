"""Request handlers for the /users endpoint."""

from urllib.parse import unquote

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, util, verify_token
from ...db import PermissionError, Roles, club, membership
from ..resource import validate
from ..resource.membership import (
    DeleteMembershipRequest, GetMembershipsRequest, GetMembershipsResponse,
    PutMembershipRequest)


class MembershipEndpoint(Endpoint):
    """Handles requests to /memberships/<club_name>."""

    __uri__ = "/memberships/<club_name:string>"

    @verify_token() 
    @validate(GetMembershipsRequest, GetMembershipsResponse)
    async def get(self, request, club_name, id_from_token=None):
        """
        Handles a GET /memberships/<club_name> request
        by returning the membership that associates the given user with the
        given club. If no user ID is given, returns all memberships for the
        given club.
        """
        # Decode the club name
        club_name = unquote(club_name)

        # Make sure the club exists
        club_row = club.select(self.server.db_session, club_name)
        if not club_row:
            raise APIError('No such club', status=404)

        body = util.strip_whitespace(request.json)
        user_id = body.get('user_id', None)

        try:
            membership_attr = membership.select(self.server.db_session,
                                                club_name, id_from_token,
                                                Roles.member)
            editors_role = membership_attr.get('role')
            # Fetch the club's memberships
            membership_info = membership.select(
                self.server.db_session, club_name, user_id, editors_role)
        except PermissionError:
            raise APIError('Unauthorized', status=403)
        return response.json(membership_info, status=200)

    # pylint: disable=unused-argument
    @verify_token()
    @validate(PutMembershipRequest, None)
    async def put(self, request, club_name, id_from_token=None):
        """Handles a PUT /memberships/<club_name>
        creating or updating the membership for the given user and club."""
        # Decode the club name
        club_name = unquote(club_name)
        body = util.strip_whitespace(request.json)
        members_role = body.get('members_role', None)
        position = body.get('position', None)
        try:
            user_id = int(request.args.get('user_id')[0])
        except Exception:
            raise APIError('Invalid user ID', status=400)
        try:
            membership_attr = membership.select(self.server.db_session,
                                                club_name, id_from_token,
                                                Roles.president)
            editors_role = membership_attr.get('role')
            membership.insert(self.server.db_session, club_name, user_id,
                              editors_role, members_role, position)
        except PermissionError:
            raise APIError('Unauthorized', status=403)
        except IntegrityError:
            raise APIError('Invalid user or club ID', status=400)
        return response.text('', status=201)

    # pylint: enable=unused-argument

    @verify_token()
    @validate(DeleteMembershipRequest, None)
    async def delete(self, request, club_name, id_from_token=None):
        """
        Handles a DELETE /memberships/<club_name> request
        by deleting the membership that associates the given user with the
        given club.
        """
        # TODO: fix this when we have user roles set up. A user should only be
        # able to delete their own memberships and memberships on clubs they
        # are an admin/owner of.

        # Decode the club name
        club_name = unquote(club_name)

        # Make sure the club exists
        club_row = club.select(self.server.db_session, club_name)
        if not club_row:
            raise APIError('No such club', status=404)

        # Get members_role from body
        body = util.strip_whitespace(request.json)
        members_role = body.get('members_role', None)

        try:
            user_id = int(request.args.get('user_id')[0])
        except ValueError:
            raise APIError('Invalid user ID', status=400)

        try:
            membership_attr = membership.select(self.server.db_session,
                                                club_name, id_from_token,
                                                Roles.president)
            editors_role = membership_attr.get('role')
            if user_id:
                membership.delete(self.server.db_session, club_name,
                                  id_from_token, user_id, editors_role,
                                  members_role)
            else:
                membership.delete_all(self.server.db_session, club_name,
                                      editors_role, members_role)
        except PermissionError:
            raise APIError('Unauthorized', status=403)
        except IntegrityError:
            raise APIError('Invalid user or club ID', status=400)
        return response.text('', status=201)
