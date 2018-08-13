'''Create a Membership resource in bounce/server/resource/membership.py that specifies all the information required for creating a new membership.'''

from . import ResourceMeta


class GetMembershipRequest(metaclass=ResourceMeta):
    """Defines the schema for a GET /membership/<club_name> request."""
    __params__ = {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'user_id': {
                'type': 'string',
                'minimum': 0,
            },
        }
    }


class GetMembershipResponse(metaclass=ResourceMeta):
    """Defines the schema for a GET /membership/<club_name> response."""
    __body__ = {
        'type': 'array',
        'items': {
            'type': 'object',
            'required': [
                'user_id',
                'created_at',
                'full_name',
                'username',
            ],
            'properties': {
                'user_id': {
                    'type': 'integer'
                },
                'created_at': {
                    'type': 'integer',
                },
                'full_name': {
                    'type': 'string',
                },
                'username': {
                    'type': 'string',
                },
            }
        }
    }


class PostMembershipRequest(metaclass=ResourceMeta):
    """Defines the schema for a POST /membership request."""
    __body__ = {
        'type': 'object',
        'required': ['user_id', 'club_id'],
        'additionalProperties': False,
        'properties': {
            'user_id': {
                'type': 'integer',
                'minimum': 0,
            },
            'club_id': {
                'type': 'integer',
                'minimum': 0,
            },
        }
    }


class PutMembershipRequest(metaclass=ResourceMeta):
    """Defines the schema for a PUT /users/<username> request."""
    __body__ = {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'user_id': {
                'type': 'integer',
                'minimum': 0,
            },
            'created_at': {
                'type': 'integer',
            },
        }
    }


class DeleteMembershipRequest(metaclass=ResourceMeta):
    """Defines the schema for a DELETE /members/<club_name> request."""
    __params__ = {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'user_id': {
                'type': 'string',
            },
        }
    }
