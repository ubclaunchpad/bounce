"""Resources for the /memberships endpoint."""

from . import ResourceMeta


class GetMembershipRequest(metaclass=ResourceMeta):
    """Defines the schema for a GET /membership/<club_name> request."""
    __params__ = {
        'type': 'object',
        'additionalProperties': False,
        'required': ['user_id'],
        'properties': {
            'user_id': {
                'type': 'integer',
                'minimum': 0,
            }
        }
    }


class GetMembershipResponse(metaclass=ResourceMeta):
    """Defines the schema for a GET /membership/<club_name> response."""
    __body__ = {
        'type': 'dictionary',
        'items': {
            'type':
            'object',
            'required': [
                'user_id',
                'created_at',
                'position',
                'role',
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
                'role': {
                    'enum': ['President', 'Admin', 'Member']
                },
                'position': {
                    'type': 'string'
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


class PutMembershipRequest(metaclass=ResourceMeta):
    """Defines the schema for a PUT /memberships/<club_name> request."""
    __params__ = {
        'user_id': {
            'type': 'integer',
        },
    }

    __body__ = {
        'type': 'object',
        'additionalProperties': False,
        'required': ['members_role', 'position'],
        'properties': {
            'members_role': {
                'enum': ["President", "Admin", "Member"]
            },
            'position': {
                'type': 'string'
            },
        }
    }


class DeleteMembershipRequest(metaclass=ResourceMeta):
    """Defines the schema for a DELETE /memberships/<club_name> request."""
    __params__ = {
        'type': 'object',
        'additionalProperties': False,
        'required': ['user_id'],
        'properties': {
            'user_id': {
                'type': 'integer',
            },
        }
    }

    __body__ = {
        'type': 'object',
        'additionalProperties': False,
        'required': ['role', 'position'],
        'properties': {
            'members_role': {
                'enum': ["President", "Admin", "Member"]
            }
        }
    }
