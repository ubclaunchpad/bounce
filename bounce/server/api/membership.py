"""Request handlers for the /users endpoint."""

from urllib.parse import unquote

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, util, verify_token
from ...db import Roles, club, membership
from ...db.club import validate_club
from ...db.user import validate_user
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
        try:
            # If not a member, the editors_role is defaulted to None
            editors_role = None
            # Otherwise, check his or her membership
            membership_attr = membership.select(
                self.server.db_session, club_name, id_from_token, Roles.member)
            if membership_attr:
                editors_role = membership_attr[0]['role']
            # Fetch the club's memberships
            if 'user_id' in request.args:
                user_id = int(request.args['user_id'])
                membership_info = membership.select(
                    self.server.db_session, club_name, user_id, editors_role)
            else:
                membership_info = membership.select_all(
                    self.server.db_session, club_name, editors_role)
        except PermissionError:
            raise APIError('Unauthorized', status=403)
        return response.json(membership_info, status=200)

    @verify_token()
    @validate(PutMembershipRequest, None)
    async def put(self, request, club_name, id_from_token=None):
        """Handles a PUT /memberships/<club_name>
        creating or updating the membership for the given user and club."""
        # Decode the club name
        club_name = unquote(club_name)
        body = util.strip_whitespace(request.json)
        position = body.get('position', None)
        members_role = body.get('members_role', None)
        try:
            # get the id of the user we want to edit a membership
            user_id = int(request.args.get('user_id')[0])
        except Exception:
            raise APIError('No user ID provided', status=400)
        try:
            # validate whether the user ID corresponds to an existing user
            validate_user(self.server.db_session, user_id)
            # validate whether the club exists
            validate_club(self.server.db_session, club_name)
            # get the editors role using id_from_token
            # to see if the editor has access to insert/update the memberships table.
            editor_attr = membership.select(self.server.db_session, club_name,
                                            id_from_token, Roles.president)
            editors_role = editor_attr[0]['role']
            membership_attr = membership.select(
                self.server.db_session, club_name, user_id, Roles.president)
            # If the membership exists already in the table, update entry
            if membership_attr:
                current_members_role = membership_attr[0]['role']
                membership.update(self.server.db_session, club_name, user_id,
                                  editors_role, current_members_role, position,
                                  members_role)
            # Otherwise, insert new entry
            else:
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

        try:
            # get the id of the user we want to add a membership
            user_id = int(request.args.get('user_id'))
        except ValueError:
            raise APIError('Invalid user ID', status=400)

        try:
            # validate whether the user ID corresponds to an existing user
            validate_user(self.server.db_session, user_id)
            # validate whether the club exists
            validate_club(self.server.db_session, club_name)

            editor_attr = membership.select(self.server.db_session, club_name,
                                            id_from_token, Roles.president)

            editors_role = editor_attr[0]['role']

            member_attr = membership.select(self.server.db_session, club_name,
                                            user_id, Roles.president)
            members_role = member_attr[0]['role']
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
