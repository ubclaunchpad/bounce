"""Request handlers for the /clubs endpoint."""

import os
from urllib.parse import unquote

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import IMAGE_SIZE_LIMIT, APIError, Endpoint, util, verify_token
from ...db import Roles, club, image, membership
from ...db.club import MAX_SIZE, MIN_SIZE
from ...db.image import EntityType
from ..resource import validate
from ..resource.club import (DeleteClubRequest, GetClubResponse,
                             PostClubsRequest, PutClubRequest,
                             SearchClubsRequest, SearchClubsResponse)


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
    async def put(self, request, club_name, id_from_token=None):
        """Handles a PUT /clubs/<name> request by updating the club with
        the given name and returning the updated club info."""
        # Decode the name, since special characters will be URL-encoded
        club_name = unquote(club_name)
        body = util.strip_whitespace(request.json)
        try:
            membership_attr = membership.select(self.server.db_session,
                                                club_name, id_from_token,
                                                Roles.president)
            editors_role = membership_attr.get('role')
            updated_club = club.update(
                self.server.db_session,
                club_name,
                editors_role,
                new_name=body.get('name', None),
                description=body.get('description', None),
                website_url=body.get('website_url', None),
                facebook_url=body.get('facebook_url', None),
                instagram_url=body.get('instagram_url', None),
                twitter_url=body.get('twitter_url', None))
        except PermissionError:
            raise APIError('Unauthorized', status=403)
        return response.json(updated_club, status=200)

    @verify_token()
    @validate(DeleteClubRequest, None)
    async def delete(self, request, club_name, id_from_token=None):
        """Handles a DELETE /clubs/<name> request by deleting the club with
        the given name."""
        # Decode the name, since special characters will be URL-encoded
        club_name = unquote(club_name)
        try:
            membership_attr = membership.select(self.server.db_session,
                                                club_name, id_from_token,
                                                Roles.president)
            editors_role = membership_attr.get('role')
            club.delete(self.server.db_session, club_name, editors_role)
        except PermissionError:
            raise APIError('Unauthorized', status=403)
        return response.text('', status=204)


class ClubsEndpoint(Endpoint):
    """Handles requests to /clubs."""

    __uri__ = '/clubs'

    @verify_token()
    @validate(PostClubsRequest, None)
    async def post(self, request, id_from_token=None):
        # import pdb
        # pdb.set_trace()
        """Handles a POST /clubs request by creating a new club."""
        # Put the club in the DB
        body = util.strip_whitespace(request.json)
        try:
            club.insert(
                self.server.db_session,
                name=body.get('name', None),
                description=body.get('description', None),
                website_url=body.get('website_url', None),
                facebook_url=body.get('facebook_url', None),
                instagram_url=body.get('instagram_url', None),
                twitter_url=body.get('twitter_url', None))

        except IntegrityError:
            raise APIError('Club already exists', status=409)
        # Make the creator have a President membership of this club.
        # Use the creators id from token to create the membership.
        membership.insert(self.server.db_session, body.get(
            'name'), id_from_token, Roles.president, Roles.president, 'Owner')
        return response.text('', status=201)


class SearchClubsEndpoint(Endpoint):
    """Handles requests to /clubs/search."""

    __uri__ = '/clubs/search'

    @validate(SearchClubsRequest, SearchClubsResponse)
    async def get(self, request):
        """Handles a GET /club/search request by returning
        clubs that contain content from the query."""

        query = None
        if 'query' in request.args:
            query = request.args['query']
        page = int(request.args['page'])
        size = int(request.args['size'])
        if size > MAX_SIZE:
            raise APIError('size too high', status=400)
        if size < MIN_SIZE:
            raise APIError('size too low', status=400)

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


class ClubImagesEndpoint(Endpoint):
    """Handles requests to /clubs/<club_name>/images/<image_name>."""

    __uri__ = '/clubs/<club_name>/images/<image_name>'

    async def get(self, _, club_name, image_name):
        """
        Handles a GET /clubs/<club_name>/images/<image_name> request
        by returning the club's image with the given name.
        """

        if not util.check_image_name(image_name):
            raise APIError('Invalid image name', status=400)
        try:
            return await response.file(
                os.path.join(self.server.config.image_dir,
                             EntityType.CLUB.value, club_name, image_name))
        except FileNotFoundError:
            raise APIError('No such image', status=404)

    # @verify_token()
    async def put(self, request, club_name, image_name):
        """
        Handles a PUT /clubs/<club_name>/images/<image_name> request
        by updating the image at the given path.
        """
        # For now, only allow clubs to upload profile pictures
        if image_name != 'profile' or not util.check_image_name(image_name):
            raise APIError('Invalid image name', status=400)

        # Make sure the user is updating an image they own
        club_info = club.select(self.server.db_session, club_name)
        if not club_info:
            raise APIError('No such image', status=404)

        # Save the image
        image_upload = request.files.get('image')
        if not image_upload:
            raise APIError('No image provided', status=400)
        if (image_upload.type != 'image/png'
                and image_upload.type != 'image/jpeg'):
            raise APIError(
                'Only png and jpeg images are supported', status=400)
        if len(image_upload.body) > IMAGE_SIZE_LIMIT:
            raise APIError('Image too large', status=400)

        image.save(self.server.config.image_dir, EntityType.CLUB, club_name,
                   image_name, image_upload.body)

        return response.text('', status=200)

    # @verify_token()
    async def delete(self, _, club_name, image_name):
        """Handles a DETELE by deleting the club's image by the given name."""

        if not util.check_image_name(image_name):
            raise APIError('Invalid image name', status=400)
        # Make sure the user is deleting their own image
        club_info = club.select(self.server.db_session, club_name)
        if not club_info:
            raise APIError('No such image', status=404)
        try:
            image.delete(
                self.server.config.image_dir,
                EntityType.CLUB,
                club_name,
                image_name,
                must_exist=True)
        except FileNotFoundError:
            raise APIError('No such image', status=404)
        return response.text('', status=200)
