"""Resources for the /users endpoint."""

from . import ResourceMeta


class PostUsersRequest(metaclass=ResourceMeta):
    """Defines the schema for a POST /users request."""
    __body__ = {
        'type': 'object',
        'required': ['full_name', 'username', 'email'],
        'properties': {
            'full_name': {
                'type': 'string'
            },
            'username': {
                'type': 'string',
            },
            'email': {
                'type': 'string',
                'format': 'email',
            },
        }
    }


class PutUserRequest(metaclass=ResourceMeta):
    """Defines the schema for a PUT /users/<username> request."""
    __body__ = {
        'type': 'object',
        'properties': {
            'full_name': {
                'type': 'string'
            },
            'email': {
                'type': 'string',
                'format': 'email'
            },
        }
    }


class GetUserResponse(metaclass=ResourceMeta):
    """Defines the schema for a GET /users/<username> response."""
    __body__ = {
        'type': 'object',
        'required': ['full_name', 'username', 'email', 'id', 'created_at'],
        'properties': {
            'full_name': {
                'type': 'string'
            },
            'username': {
                'type': 'string',
            },
            'email': {
                'type': 'string',
                'format': 'email',
            },
            'id': {
                'type': 'integer',
                'minimum': 0,
            },
            'created_at': {
                'type': 'integer',
            },
        }
    }
