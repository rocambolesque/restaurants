from flask import json, Response
from marshmallow import MarshalResult
from sqlalchemy.inspection import inspect

from models import db


class ApiResponse(Response):
    def __init__(self, response=None, status=None, headers=None, mimetype='application/json', content_type=None, direct_passthrough=False):
        response = str(json.dumps(response))
        super().__init__(
            response=response,
            status=status,
            headers=headers,
            mimetype=mimetype,
            content_type=content_type,
            direct_passthrough=direct_passthrough
        )
