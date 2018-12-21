"""Resources for the /clubs endpoint."""

from . import ResourceMeta


class PostClubsRequest(metaclass=ResourceMeta):
    """Defines the schema for a POST /clubs request."""
    __body__ = {
        'type': 'object',
        'required': ['name', 'description'],
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


class PutClubRequest(metaclass=ResourceMeta):
    """Defines the schema for a PUT /clubs/<name> request."""
    __body__ = {
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


class SearchClubsRequest(metaclass=ResourceMeta):
    """Defines the schema for a GET /clubs/search request."""
    __params__ = {
        'query': {
            'type': 'string',
        },
        'page': {
            'type': 'integer',
            'default':
            0,  # TODO: defaults aren't being set when param is not specified
        },
        'size': {
            'type': 'integer',
            'default':
            5,  # TODO: defaults aren't being set when param is not specified
        }
    }


class SearchClubsResponse(metaclass=ResourceMeta):
    """Defines the schema for a search query response."""
    __body__ = {
        'results': {
            'type': 'array',
            'items': {
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


class DeleteClubRequest(metaclass=ResourceMeta):
    """Defines the schema for a GET /clubs/<name> request."""
    __body__ = {'editor_role': {'enum': ['President', 'Admin', 'Member']}}
