#!/usr/bin/env python


import requests

from controllers import api
from flask_restplus import Resource
from flask_restplus.swagger import Swagger
from munch import Munch

from mcp import app
from mcp.logutil import get_logger


ns = api.namespace('hdmi', description='HDMI Port Remote')

ha_url = 'http://mcp-03.kurohai.local:8123/api'
ha_harmony_cmd = '{u}/services/remote/send_command'.format(u=ha_url)

@api.doc(responses={404: 'Port not found'}, params={'port_number': 'The port number'})
@ns.route('/<int:port_number>/')
class HDMIPortControl(Resource):
    """docstring for HDMIPort"""

    @api.doc(description='Control outlets')
    def get(self, port_number):
        data = Munch()
        data.device = '58377647'
        data.command = int(port_number)
        result = request.post(ha_harmony_cmd, json=data.toDict())
        log.debug(result.json)

