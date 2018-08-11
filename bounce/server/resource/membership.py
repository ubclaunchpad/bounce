'''Create a Membership resource in bounce/server/resource/membership.py that specifies all the information required for creating a new membership.'''

from . import ResourceMeta


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
                'type': 'string',
                'minimum': 0,
            },
            'membership_id': {
                'type': 'integer',
                'minimum': 0,
            },
            'created_at': {
                'type': 'integer',
            },
        }
    }


class GetMembershipResponse(metaclass=ResourceMeta):
    """Defines the schema for a GET /users/<username> response."""
    __body__ = {
        'type': 'object',
        'required': ['user_id', 'club_id', 'created_at'],
        'additionalProperties': False,
        'properties': {
            'user_id': {
                'type': 'string'
            },
            'club_id': {
                'type': 'string',
            },
            'created_at': {
                'type': 'integer',
            },
        }
    }
