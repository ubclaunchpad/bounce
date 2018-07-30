"""
Defines a base Endpoint that can be subclassed when implementing HTTP
request endpoints.
"""

import asyncio
import logging

from sanic import response
from sanic.log import logger

HTTP_METHODS = set(
    ['get', 'put', 'post', 'delete', 'head', 'connect', 'options', 'trace'])


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

    def __init__(self, server):
        """Create a new endpoint served by the given server.

        Args:
            server (Server): the server that serves content for this endpoint
        """
        self.server = server
        self.allowed_methods = set([
            mthd for mthd in HTTP_METHODS
            if asyncio.iscoroutinefunction(getattr(self, mthd, None))
        ])

    @property
    def uri(self):
        """Returns the URI for this endpoint."""
        return self.__uri__

    async def handle_request(self, request, *args, **kwargs):
        """Routes requests to other handlers on this Endpoint
        based on their HTTP method.

        Args:
            request (Request): the incoming request to route
        """
        if request.method.lower() not in self.allowed_methods:
            # This endpoint does not accept HTTP requests with the given method
            return response.json({'error': 'Method not allowed'}, status=405)
        try:
            # Call the handler with the same name as the request method
            return await getattr(self, request.method.lower())(request, *args,
                                                               **kwargs)
        except APIError as err:
            # An error was raised by the handler because there was something
            # wrong with the request
            logger.exception(
                'An error occurred during the handling of a %s '
                'request to %s', request.method, self.__class__.__name__)
            return response.json({'error': err.message}, status=err.status)
        except Exception:
            # An error occurred during the handling of this request
            logger.exception(
                'An error occurred during the handling of a %s '
                'request to %s', request.method, self.__class__.__name__)
            return response.json(
                {
                    'error': 'Internal server error'
                }, status=500)
