"""Resources for the /users and /user endpoints."""

from . import ResourceMeta


class PostUsersRequest(metaclass=ResourceMeta):
    """Defines the schema for a POST /users request."""
    __body__ = {
        'type': 'object',
        'required': ['full_name', 'username', 'password', 'email'],
        'additionalProperties': False,
        'properties': {
            'full_name': {
                'type': 'string'
            },
            'username': {
                'type': 'string',
            },
            'password': {
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
        'additionalProperties': False,
        'properties': {
            'full_name': {
                'type': 'string'
            },
            'password': {
                'type': 'string'
            },
            'new_password': {
                'type': 'string'
            },
            'email': {
                'type': 'string',
                'format': 'email'
            }
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


class SearchUsersRequest(metaclass=ResourceMeta):
    """Defines the schema for a GET /users/search request."""
    __params__ = {
        'query': {
            'type': 'string',
        },
        'page': {
            'type': 'string',
            'default': '0',
            'minimum': '0',
        },
        'size': {
            'type': 'string',
            'default': '20',
            'minimum': '0',
        }
    }


class SearchUsersResponse(metaclass=ResourceMeta):
    """Defines the schema for a search query response."""
    __body__ = {
        'results': {
            'type': 'array',
            'items': {
                'type':
                'object',
                'required':
                ['full_name', 'username', 'email', 'id', 'created_at'],
                'additionalProperties':
                False,
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
        },
        'resultCount': {
            'type': 'integer',
            'minimum': 0,
        },
        'page': {
            'type': 'integer',
            'minimum': 0,
        },
        'totalPages': {
            'type': 'integer',
            'minimum': 0,
        }
    }
