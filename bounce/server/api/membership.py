"""Request handlers for the /users endpoint."""

from urllib.parse import unquote

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, util, verify_token
from ...db import Roles, club, membership
from ..resource import validate
from ..resource.membership import (
    DeleteMembershipRequest, GetMembershipsRequest, GetMembershipsResponse,
    PutMembershipRequest)


class MembershipEndpoint(Endpoint):
    """Handles requests to /memberships/<club_name>."""

    __uri__ = "/memberships/<club_name:string>"

    @verify_token()
    @validate(GetMembershipsRequest, GetMembershipsResponse)
    async def get(self, session, request, club_name, id_from_token=None):
        """
        Handles a GET /memberships/<club_name> request
        by returning the membership that associates the given user with the
        given club. If no user ID is given, returns all memberships for the
        given club.
        """

        # Decode the club name
        club_name = unquote(club_name)

        # Make sure the club exists
        club_row = club.select(session, club_name)
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
            raise APIError('Forbidden', status=403)
        return response.json(membership_info, status=200)

    @verify_token()
    @validate(PutMembershipRequest, None)
    async def put(self, session, request, club_name, id_from_token=None):
        """Handles a PUT /memberships/<club_name>?user_id=<user_id> request by
        creating or updating the membership for the given user and club."""
        # Decode the club name
        club_name = unquote(club_name)
        body = util.strip_whitespace(request.json)
        position = body.get('position', None)
        members_role = body.get('members_role', None)

        try:
            # get the id of the user we want to edit a membership
            user_id = int(request.args['user_id'])
        except KeyError:
            raise APIError('No user ID provided', status=400)

        # get the editors role using id_from_token
        # to see if the editor has access to insert/update
        # the memberships table.
        editor_attr = membership.select(session, club_name, id_from_token,
                                        Roles.president)
        if not editor_attr:
            # Either the club doesn't exist, or the user is not a member of
            # the club
            raise APIError('Bad request', status=400)

        editors_role = editor_attr[0]['role']
        membership_attr = membership.select(session, club_name, user_id,
                                            Roles.president)

        try:
            # If the membership exists already in the table, update entry
            if membership_attr:
                current_members_role = membership_attr[0]['role']
                membership.update(session, club_name, user_id, editors_role,
                                  current_members_role, position, members_role)
            # Otherwise, insert new entry
            else:
                membership.insert(session, club_name, user_id, editors_role,
                                  members_role, position)
        except PermissionError:
            raise APIError('Forbidden', status=403)
        except IntegrityError:
            raise APIError('Bad request', status=400)
        return response.text('', status=201)

    @verify_token()
    @validate(DeleteMembershipRequest, None)
    async def delete(self, session, request, club_name, id_from_token=None):
        """
        Handles a DELETE /memberships/<club_name> request
        by deleting the membership that associates the given user with the
        given club.
        """

        # Decode the club name
        club_name = unquote(club_name)

        # Make sure the club exists
        club_row = club.select(session, club_name)
        if not club_row:
            raise APIError('No such club', status=404)

        try:
            editor_attr = membership.select(session, club_name, id_from_token,
                                            Roles.president)

            editors_role = editor_attr[0]['role']

            if 'user_id' in request.args:
                user_id = int(request.args['user_id'])
                member_attr = membership.select(session, club_name, user_id,
                                                Roles.president)
                if not member_attr:
                    raise APIError('Bad request', status=400)

                members_role = member_attr[0]['role']
                membership.delete(session, club_name, id_from_token, user_id,
                                  editors_role, members_role)
            else:
                membership.delete_all(session, club_name, editors_role)
        except PermissionError:
            raise APIError('Forbidden', status=403)
        return response.text('', status=201)
