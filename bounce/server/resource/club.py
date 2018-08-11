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
            'instagram_url', 'twitter_url', 'id', 'created_at', 'tsvector'
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
            'search_vector': {
                'type': 'tsvector'
            },
        }
    }

<<<<<<< 3a858a8631b8afed8d1e2a859f5fb036d499fafb

class SearchClubsRequest(metaclass=ResourceMeta):
    """Defines the schema for a GET /clubs/search request."""
    __params__ = {
        'query': {
            'type': 'string',
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
        }
    }
=======
    class SearchClubResponse(metaclass=ResourceMeta):
        """Defines the schema for a search query response."""
        __body__ = {
            'results': {
                'type':
                'array',
                'items': {
                    'type':
                    'object',
                    'required': [
                        'name', 'description', 'website_url', 'facebook_url',
                        'instagram_url', 'twitter_url', 'id', 'created_at', 'tsvector'
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
                        'search_vector': {
                            'type': 'tsvector'
                        },
                    }
                }
            }
        }
>>>>>>> make changes based on review
