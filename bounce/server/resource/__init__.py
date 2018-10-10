"""
Defines a base Resource class that allows easy endpoint and HTTP request
handler definition and registration.
"""

import json
import logging
from functools import wraps

import jsonschema
from jsonschema.validators import Draft4Validator
from sanic import response

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

    def set_defaults(schema, info):
        for prop_name, attributes in schema.items():
            if prop_name not in info and 'default' in attributes:
                #if isinstance(attributes, dict):
                    # TODO: run a recursion to set defaults of the dictionaries
                    # contained within the current dictionary
                default_value = attributes.get('default')
                info.update({prop_name: default_value})
        return info

    # pylint: disable=missing-docstring
    def decorator(coro):
        @wraps(coro)
        async def wrapper(endpoint, request, *args, **kwargs):
            if hasattr(request_cls, '__body__'):
                # Return a 400 if the request body does not meet the
                # required schema
                # Body values come as arrays of length 1 so turn
                # them into single values
                body_no_defaults = {key: request.form.get(key) for key in request.form}
                # TODO: set request.form with defaults
                try:
                    jsonschema.validate(
                        request.form or {},
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
                params_no_defaults = {key: request.args.get(key) for key in request.args}
                request = set_defaults(request_cls.__params__, params_no_defaults)
                try:
                    jsonschema.validate(
                        request,
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
                body_no_defaults = json.loads(result.body)
                # TODO: set defaults for body
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
