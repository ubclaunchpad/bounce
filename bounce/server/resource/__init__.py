"""
Defines a base Resource class that allows easy endpoint and HTTP request
handler definition and registration.
"""

import json
import logging
from functools import wraps

from sanic import response

import jsonschema
from jsonschema.validators import Draft4Validator

# Set up logger for this module
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ResourceMeta(type):
    """
    Metaclass for Bounce resources. A Bounce resource is just a collection
    of information with a scpecific format (schema) that is sent between the
    back-end and the front-end.
    """

    def __new__(mcs, cls_name, superclasses, attributes):
        """
        Return a new class by the given name with the given attributes and
        subclasses.

        This will validate the body and params schemas declared on a resource
        and raise a ValidationError if the schema is invalid.

        Args:
            mcs (type): the metaclass
            cls_name (str): the name of the new class
            superclasses (list[type]): list of the classes superclasses
            attributes (dict): a mapping from attribute name to attribute
                value on the new class
        """
        if hasattr(attributes, '__body__'):
            # Check that the body schema is valid
            try:
                Draft4Validator.check_schema(attributes['__body__'])
            except jsonschema.ValidationError:
                raise jsonschema.ValidationError(
                    f'Invalid body schema declared for resource {cls_name}')

        if hasattr(attributes, '__params__'):
            # Check that the params schema is valid
            try:
                Draft4Validator.check_schema(attributes['__params__'])
            except jsonschema.ValidationError:
                raise jsonschema.ValidationError(
                    f'Invalid params schema declared for resource {cls_name}')

        # Create the class
        return super(ResourceMeta, mcs).__new__(mcs, cls_name, superclasses,
                                                attributes)


def validate(request_cls, response_cls):
    """
    Wraps a request handler in a JSONSchema validator to ensure that the
    request and response bodies match their respective schemas.

    Args:
        request_cls (object): the class containing the schema the request
            body should match
        response_cls (object): the class containing the schema the response
            body should match
    """

    # pylint: disable=missing-docstring
    def decorator(coro):
        @wraps(coro)
        async def wrapper(endpoint, request, *args, **kwargs):
            if hasattr(request_cls, '__body__'):
                # Return a 400 if the request body does not meet the
                # required schema
                try:
                    jsonschema.validate(
                        request.json or {},
                        request_cls.__body__,
                        format_checker=jsonschema.FormatChecker())
                except jsonschema.ValidationError as err:
                    logger.exception(
                        'request body does not fit schema for resource %s',
                        request_cls.__name__)
                    return response.json({'error': err}, status=400)

            if hasattr(request_cls, '__params__'):
                # Return a 400 if the request params do not meet the
                # required schema
                # Params values always come as arrays of length 1 so turn
                # them into single values
                params = {key: request.args.get(key) for key in request.args}
                try:
                    jsonschema.validate(
                        params,
                        request_cls.__params__,
                        format_checker=jsonschema.FormatChecker())
                except jsonschema.ValidationError as err:
                    logger.exception(
                        'request params do not fit schema for resource %s',
                        request_cls.__name__)
                    return response.json({'error': err}, status=400)

            # Call the request handler
            result = await coro(endpoint, request, *args, **kwargs)

            if hasattr(response_cls, '__body__'):
                # Return a 500 if the response does not meet the required
                # format and raise an error
                try:
                    jsonschema.validate(
                        json.loads(result.body),
                        response_cls.__body__,
                        format_checker=jsonschema.FormatChecker())
                except jsonschema.ValidationError as err:
                    logger.exception(
                        'response body does not fit schema for resource %s',
                        response_cls.__name__)
                    return response.json({'error': err}, status=500)

            return result

        return wrapper

    return decorator
