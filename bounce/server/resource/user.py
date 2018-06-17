"""Resources for the /users endpoint."""

from . import ResourceMeta


class PutUserRequest(metaclass=ResourceMeta):
    """Defines the schema for a PUT /users request."""
    __body__ = {
        'type': 'object',
        'required': ['full_name', 'username', 'email'],
        'properties': {
            'full_name': {
                'type': 'string'
            },
            'username': {
                'type': 'string'
            },
            'email': {
                'type': 'string',
                'format': 'email'
            },
        }
    }


class PutUserResponse(metaclass=ResourceMeta):
    """Defines the schema for a PUT /users response."""
    pass


class GetUserRequest(metaclass=ResourceMeta):
    """Defines the schema for a GET /users request."""
    __params__ = {
        'type': 'object',
        'required': ['username'],
        'properties': {
            'username': {
                'type': 'string',
            }
        }
    }


class GetUserResponse(metaclass=ResourceMeta):
    """Defines the schema for a GET /users response."""
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
