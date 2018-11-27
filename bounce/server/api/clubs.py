"""Request handlers for the /clubs endpoint."""

from urllib.parse import unquote

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint, util
from ...db import PermissionError, club
from ..resource import validate
from ..resource.club import (DeleteClubRequest, GetClubResponse,
                             PostClubsRequest, PutClubRequest,
                             SearchClubsRequest, SearchClubsResponse)

MAX_SIZE = 20


class ClubEndpoint(Endpoint):
    """Handles requests to /clubs/<name>."""

    __uri__ = "/clubs/<name:string>"

    @validate(None, GetClubResponse)
    async def get(self, _, name):
        """Handles a GET /clubs/<name> request by returning the club with
        the given name."""
        # Decode the name, since special characters will be URL-encoded
        name = unquote(name)
        # Fetch club data from DB
        club_data = club.select(self.server.db_session, name)
        if not club_data:
            # Failed to find a club with that name
            raise APIError('No such club', status=404)
        return response.json(club_data, status=200)

    @verify_token()
    @validate(PutClubRequest, GetClubResponse)
    async def put(self, request, name, id_from_token=None):
        """Handles a PUT /clubs/<name> request by updating the club with
        the given name and returning the updated club info."""
        # Decode the name, since special characters will be URL-encoded
        # TODO: Check the schema for roles, and if it needs body.get()
        name = unquote(name)
        body = util.strip_whitespace(request.json)
        try:
            updated_club = club.update(
                self.server.db_session,
                name,
                new_name=body.get('name', None),
                description=body.get('description', None),
                website_url=body.get('website_url', None),
                facebook_url=body.get('facebook_url', None),
                instagram_url=body.get('instagram_url', None),
                twitter_url=body.get('twitter_url', None),
                editor_role)
        except PermissionError:
            raise APIError('Unauthorized', status=403)
        return response.json(updated_club, status=200)

    @validate(DeleteClubRequest, None)
    async def delete(self, request, name):
        """Handles a DELETE /clubs/<name>?access=<role> request by deleting the club with
        the given name."""
        # Decode the name, since special characters will be URL-encoded
        name = unquote(name)
        body = util.strip_whitespace(request.json)
        try:
            club.delete(
                self.server.db_session,
                name,
                editor_role=body.get('editor_role', None))
        except PermissionError:
            raise APIError('Unauthorized', status=403)
        return response.text('', status=204)


class ClubsEndpoint(Endpoint):
    """Handles requests to /clubs."""

    __uri__ = '/clubs'

    @validate(PostClubsRequest, None)
    async def post(self, request):
        """Handles a POST /clubs request by creating a new club."""
        # Put the club in the DB
        body = util.strip_whitespace(request.json)
        try:
            club.insert(
                self.server.db_session,
                name = body.get('name', None),
                description=body.get('description', None),
                website_url=body.get('website_url', None),
                facebook_url=body.get('facebook_url', None),
                instagram_url=body.get('instagram_url', None)
                twitter_url=body.get('twitter_url', None)
        except IntegrityError:
            raise APIError('Club already exists', status=409)
        return response.text('', status=201)


class SearchClubsEndpoint(Endpoint):
    """Handles requests to /clubs/search."""

    __uri__ = '/clubs/search'

    @validate(SearchClubsRequest, SearchClubsResponse)
    async def get(self, request):
        """Handles a GET /club/search request by returning
        clubs that contain content from the query."""

        # default values, TODO: set default value in json-schema
        query = ''
        page = 0
        size = 20

        if 'query' in request.args:
            query = request.args['query'][0]
        if 'page' in request.args:
            page = int(request.args['page'][0])
        if 'size' in request.args:
            size = int(request.args['size'][0])
        if size > MAX_SIZE:
            raise APIError('size too high', status=400)

        queried_clubs, result_count, total_pages = club.search(
            self.server.db_session, page, size, query)
        if not queried_clubs:
            # Failed to find clubs that match the query
            raise APIError('No clubs match your query', status=404)
        results = []
        for result in queried_clubs.all():
            results.append(result.to_dict())
        info = {
            'results': results,
            'result_count': result_count,
            'page': page,
            'total_pages': total_pages
        }

        return response.json(info, status=200)
