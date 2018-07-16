"""Resources for the /users endpoint."""

from . import ResourceMeta


class PostUsersRequest(metaclass=ResourceMeta):
    """Defines the schema for a POST /users request."""
<<<<<<< 58ddae63f22bf2f54edd5143cbf322eef552066b
    __body__ = {
=======
    __body__ = {  #shouldn't it be __params__?
>>>>>>> first commit
        'type': 'object',
        'required': ['full_name', 'username', 'email'],
        'additionalProperties': False,
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
<<<<<<< 58ddae63f22bf2f54edd5143cbf322eef552066b
    __body__ = {
=======
    __body__ = {  #shouldn't it be __params__?
>>>>>>> first commit
        'type': 'object',
        'additionalProperties': False,
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
        'additionalProperties': False,
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
