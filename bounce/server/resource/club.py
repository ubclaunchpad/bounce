"""Resources for the /clubs endpoint."""

from . import ResourceMeta


class PostClubsRequest(metaclass=ResourceMeta):
    """Defines the schema for a POST /clubs request."""
    __params__ = {
        'type':
        'object',
        'required': [
            'name', 'description', 'website_url', 'facebook_url',
            'instagram_url', 'twitter_url'
        ],
        'additionalProperties':
        False,
        'properties': {
            'name': {
                'type': 'string'
            },
            'description': {
                'type': 'string',
            },
            'website_url': {
                'type': 'string',
            },
            'facebook_url': {
                'type': 'string',
            },
            'instagram_url': {
                'type': 'string',
            },
            'twitter_url': {
                'type': 'string',
            },
        }
    }


class PutClubRequest(metaclass=ResourceMeta):
    """Defines the schema for a PUT /clubs/<name> request."""
    __request__ = {
        'type': 'object',
        'required': ['name'],
        'additionalProperties': False,
        'properties': {
            'name': {
                'type': 'string'
            },
            'description': {
                'type': 'string',
            },
            'website_url': {
                'type': 'string',
            },
            'facebook_url': {
                'type': 'string',
            },
            'instagram_url': {
                'type': 'string',
            },
            'twitter_url': {
                'type': 'string',
            },
        }
    }


class GetClubResponse(metaclass=ResourceMeta):
    """Defines the schema for a GET /clubs/<name> response."""
    __body__ = {
        'type':
        'object',
        'required': [
            'name', 'description', 'website_url', 'facebook_url',
            'instagram_url', 'twitter_url', 'id', 'created_at'
        ],
        'additionalProperties':
        False,
        'properties': {
            'name': {
                'type': 'string'
            },
            'description': {
                'type': 'string',
            },
            'website_url': {
                'type': 'string',
            },
            'facebook_url': {
                'type': 'string',
            },
            'instagram_url': {
                'type': 'string',
            },
            'twitter_url': {
                'type': 'string',
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
