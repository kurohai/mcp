#!/usr/bin/env python


import requests

import simplejson

from flask_restplus_patched import Resource
from flask_restplus_patched.swagger import Swagger
# from mcp import app
from mcp.controllers import api
from mcp.logutil import get_logger
from munch import Munch

log = get_logger(__name__)

ns = api.namespace('hdmi', description='HDMI Port Remote')

ha_url = 'http://mcp-03.kurohai.local:8123/api'
ha_harmony_cmd = '{u}/services/remote/send_command'.format(u=ha_url)

@api.doc(responses={404: 'Port not found'}, params={'port_number': 'The port number'})
@ns.route('/<int:port_number>/')
class HDMIPortControl(Resource):
    """docstring for HDMIPort"""

    @api.doc(description='Control HDPI by Port')
    def get(self, port_number):
        data = Munch()
        data.device = '58377647'
        data.command = int(port_number)
        headers = Munch()
        headers['x-ha-access'] = 'mermaidpuss'
        result = requests.post(ha_harmony_cmd, headers=headers, json=data.toDict())
        log.debug(result)

        if result.status_code == 200:
            return {'result': True}
        else:
            return {'result': False}

@api.doc(responses={404: 'Port not found'}, params={'direction': 'The port number'})
@ns.route('/direction/<string:direction>/')
class HDMIPortDirection(Resource):
    """docstring for HDMIPort"""

    @api.doc(description='Control HDMI Port with Direction')
    def get(self, direction):
        data = Munch()
        data.device = '58377647'
        if direction == 'right':
            data.command = 'DirectionRight'
        elif direction == 'left':
            data.command = 'DirectionLeft'
        # data.command = str(direction)
        headers = Munch()
        headers['x-ha-access'] = 'mermaidpuss'
        result = requests.post(ha_harmony_cmd, headers=headers, json=data.toDict())
        log.debug(result)
        if result.status_code == 200:
            return {'result': True}
        else:
            return {'result': False}
