API_MANGA = {
    "definitions": {
        "inspection": {
            "type": "object",
            "properties": {
                'id': {"type": 'number'},
                'title': {"type": 'string'},
                'alt_title': {"type": 'string'},
                'rating': {"type": 'number'},
                'thumbnail': {"type": 'string'},
                'image': {"type": 'string'},
                'description': {"type": 'string'},
                'source': {"type": 'string'},
            },
            'required': ['id', 'title', 'rating', 'description']
        },
    },
    "properties": {
        'count': {"type": "number"},
        'next': {"type": "string"},
        'previous': {"type": "string"},
        'results': {
            "type": "array",
            "maxProperties": 1,
            "minProperties": 1,
            "additionalProperties": {
                "$ref": "#/definitions/inspection"
            }
        }
    },
    'required': ['count', 'next', 'previous', 'results']
}

API_MANGA_ID = {
    'type': 'object',
    'properties': {
        'id': {"type": 'number'},
        'title': {"type": 'string'},
        'alt_title': {"type": 'string'},
        'rating': {"type": 'number'},
        'thumbnail': {"type": 'string'},
        'image': {"type": 'string'},
        'description': {"type": 'string'},
        'source': {"type": 'string'},

    },
    'required': ['id', 'title', 'rating', 'description']
}

API_MANGA_ID_CHAPTERS = {
    'type': 'object',
    'properties': {
        "id": {"type": 'number'},
        "title": {"type": 'string'},
        "link": {"type": 'string'},
        "number": {"type": 'number'},
        "volume": {"type": 'number'},
    }
}


class Resp:
    def __init__(self, response):
        self.response = response
        self.response_status = response.status_code
        self.response_headers = response.headers['content-type']

    def assert_status_code(self, status_code):
        if isinstance(status_code, list):
            assert self.response_status in status_code
        else:
            assert self.response_status == status_code
        return self

    def assert_headers(self, headers):
        if isinstance(headers, list):
            assert self.response_headers in headers
        else:
            assert self.response_headers == headers
        return self
