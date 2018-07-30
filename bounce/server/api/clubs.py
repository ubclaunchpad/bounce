"""Request handlers for the /clubs endpoint."""

from sanic import response
from sqlalchemy.exc import IntegrityError

from . import APIError, Endpoint
from ...db import club
from ..resource import validate
from ..resource.club import GetClubResponse, PostClubsRequest, PutClubRequest


class ClubEndpoint(Endpoint):
    """Handles requests to /clubs/<name>."""

    __uri__ = "/clubs/<name:string>"

    @validate(None, GetClubResponse)
    async def get(self, _, name):
        """Handles a GET /clubs/<name> request by returning the club with
        the given name."""
        # Fetch club data from DB
        club_data = club.select(self.server.db_session, name)
        if not club_data:
            # Failed to find a club with that name
            raise APIError('No such club', status=404)
        return response.json(club_data, status=200)
    
    @validate(PutClubRequest, GetClubResponse)
    async def put(self, request, name):
        """Handles a PUT /clubs/<name> request by updating the club with
        the given name and returning the updated club info."""
        body = request.json
        updated_club = club.update(
            self.server.db_session,
            name,
            new_name=body.get('name', None),
            description=body.get('description', None),
            website_url=body.get('website_url', None),
            facebook_url=body.get('facebook_url', None),
            instagram_url=body.get('instagram_url', None),
            twitter_url=body.get('twitter_url', None))
        return response.json(updated_club, status=200)

    async def delete(self, _, name):
        """Handles a DELETE /clubs/<name> request by deleting the club with
        the given name."""
        club.delete(self.server.db_session, name)
        return response.text('', status=204)


class ClubsEndpoint(Endpoint):
    """Handles requests to /clubs."""

    __uri__ = '/clubs'

    @validate(PostClubsRequest, None)
    async def post(self, request):
        """Handles a POST /clubs request by creating a new club."""
        # Put the club in the DB
        body = request.json
        try:
            club.insert(self.server.db_session, 
                        body['name'], body['description'], 
                        body['website_url'], body['facebook_url'], 
                        body['instagram_url'], body['twitter_url'])
        except IntegrityError:
            raise APIError('Club already exists', status=400)
        return response.text('', status=201)
