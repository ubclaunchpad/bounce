"""Resources for the /auth endpoint."""

from . import ResourceMeta


class AuthenticateUserRequest(metaclass=ResourceMeta):
    """Defines the schema for a POST /auth/login request."""
    __body__ = {
        'type': 'object',
        'required': ['username', 'password'],
        'additionalProperties': False,
        'properties': {
            'username': {
                'type': 'string',
            },
            'password': {
                'type': 'string',
            },
        }
    }


class AuthenticateUserResponse(metaclass=ResourceMeta):
    """Defines the schema for a POST /auth/login response."""
    __body__ = {
        'type': 'object',
        'required': ['token'],
        'additionalProperties': False,
        'properties': {
            'token': {
                'type': 'string',
            },
        }
    }
