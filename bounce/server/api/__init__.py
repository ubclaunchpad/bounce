"""
Defines a base Endpoint that can be subclassed when implementing HTTP
request endpoints.
"""

import asyncio
import logging
from functools import wraps

from sanic import response
from sanic.log import logger

from . import util

HTTP_METHODS = set(
    ['get', 'put', 'post', 'delete', 'head', 'connect', 'options', 'trace'])

# Maximum number of bytes in an image upload
IMAGE_SIZE_LIMIT = 1000000


class APIError(Exception):
    """Represents an error that occurs while handling a request."""

    def __init__(self, message, status=500):
        """Creates a new APIError

        Args:
            message (str): the error message
            status (int): the HTTP status code to return
        """
        super().__init__(message)
        self._message = message
        self._status = status

    @property
    def message(self):
        """Returns a message about the error that occurred while handling the
        request."""
        return self._message

    @property
    def status(self):
        """Returns the HTTP status code to be returned when this error is
        raised."""
        return self._status


class Endpoint:
    """
    Represents an endpoint to which requests can be made in order to manage
    a REST resource.
    """

    __uri__ = '/'

    logger = logging.getLogger(__name__)

    def __init__(self, server, allowed_origin=None):
        """Create a new endpoint served by the given server.

        If an allowed origin is specified it will be included in the header
        of all responses.

        Args:
            server (Server): the server that serves content for this endpoint
            allowed_origin (str): the name of a domain that can access
                this resource
        """
        self.server = server
        self._allowed_methods = set([
            mthd.upper() for mthd in HTTP_METHODS
            if asyncio.iscoroutinefunction(getattr(self, mthd, None))
        ])
        self._allowed_origin = allowed_origin

    @property
    def uri(self):
        """Returns the URI for this endpoint."""
        return self.__uri__

    @property
    def allowed_methods(self):
        """Returns a list of HTTP methods allowed on this endpoint."""
        return list(self._allowed_methods)

    # pylint: disable=unused-argument
    async def options(self, _, *args, **kwargs):
        """Default handler for OPTIONS requests.

        This will respond with an HTTP 405 Method not allowed unless an
        allowed origin was set, in which case this handler will respond with
        an HTTP 200 with the appropriate headers.
        """
        if self._allowed_origin:
            methods = ','.join(self._allowed_methods)
            return response.text(
                '',
                status=200,
                headers={
                    'Access-Control-Allow-Origin': self._allowed_origin,
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Methods': methods,
                })
        return response.json({'error': 'Method not allowed'}, status=405)

    # pylint: enable=unused-argument

    async def handle_request(self, request, *args, **kwargs):
        """Routes requests to other handlers on this Endpoint
        based on their HTTP method.

        Args:
            request (Request): the incoming request to route
        """
        # Create a SQLAlchemy session for handling DB transactions in this
        # request
        session = self.server.db_session
        result = None
        try:
            # Call the handler with the same name as the request method
            result = await getattr(self, request.method.lower())(
                session, request, *args, **kwargs)
        except APIError as err:
            # An error was raised by the handler because there was something
            # wrong with the request
            logger.exception(
                'An error occurred during the handling of a %s '
                'request to %s', request.method, self.__class__.__name__)
            result = response.json({'error': err.message}, status=err.status)
        except Exception:
            # An error occurred during the handling of this request
            logger.exception(
                'An error occurred during the handling of a %s '
                'request to %s', request.method, self.__class__.__name__)
            result = response.json(
                {
                    'error': 'Internal server error'
                }, status=500)
        finally:
            # Set CORS header if necessary
            if self._allowed_origin and not hasattr(
                    result.headers, 'Access-Control-Allow-Origin'):
                result.headers[
                    'Access-Control-Allow-Origin'] = self._allowed_origin
            # Make sure the session is closed
            session.close()

        return result


def verify_token():
    """Wraps request handlers in with a wrapper that validates
    JSON web tokens in requests before calling the request handlers. Any
    request handlers wrapped with this decorator should accept `id_from_token`
    as a keyword argument. This wrapper will pass a user ID for the
    authenticated user as the `id_from_token` keyword argument if the token in
    the request is valid.
    """

    # pylint: disable=missing-docstring
    def decorator(coro):
        @wraps(coro)
        async def wrapper(endpoint, session, request, *args, **kwargs):
            if not request.token:
                logger.error('No token provided in request')
                return response.json({'error': 'Unauthorized'}, status=401)
            user_id = util.check_jwt(request.token,
                                     endpoint.server.config.secret)
            if not user_id:
                logger.error('Invalid auth token')
                return response.json({'error': 'Unauthorized'}, status=401)
            kwargs['id_from_token'] = user_id

            # Call the request handler
            try:
                return await coro(endpoint, session, request, *args, **kwargs)
            except APIError as err:
                return response.json({'error': err.message}, status=err.status)
            except Exception:
                logger.exception(
                    'An error occurred during the hanlding of a request')
                # Return an error response if an error occurred in
                # the request handler
                logger.exception(
                    'An error occurred during the handling of a %s '
                    'request to %s', request.method, request.url)
                return response.json(
                    {
                        'error': 'Internal server error'
                    }, status=500)

        return wrapper

    return decorator
