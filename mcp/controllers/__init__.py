#!/usr/bin/env python


from flask import Blueprint
from flask import redirect
from flask import request
from flask_restplus import Api
from flask_restplus.swagger import Swagger

# from mcp import Base
# from mcp import db


# db.init_app(app)

api_blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api/v1'
)
api = Api(
    api_blueprint,
    version='1.0',
    title='Device Remote API',
    description='An remote control API',
)
swag = Swagger(api)

from mcp import app

# from hdmi import ns as hdmi_ns
from outlet import ns as outlet_ns

# api.add_namespace(hdmi_ns)
app.register_blueprint(api_blueprint)
