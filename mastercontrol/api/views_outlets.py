#!/usr/bin/env python


from . import ns_o as ns
from .. import db
from ..logutil import get_logger
from ..models import OutletDevice
from ..models import OutletDeviceSchema
from ..models import OutletDevice
from ..models import OutletDeviceSchema
from ..utilities import *
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_restplus_patched import Resource
from munch import Munch
from munch import munchify
from munch import unmunchify
from pprint import pformat
from pprint import pprint


log = get_logger(__name__)

# ns = api_v1.namespace('OutletDevice', description='Add those damn notes.')

@ns.route('/')
@ns.doc(description='Do the damn note thing.')
class OutletListAPI(Resource):
    """docstring for OutletDeviceAPI"""

    # @ns.response(200)
    @ns.response(OutletDeviceSchema(many=True))
    def get(self):
        results = munchify(OutletDevice.query.all())
        return [r for r in results]


@ns.route('/<string:name>/')
@ns.doc(description='Do the damn note thing.')
class OutletDeviceAPI(Resource):
    """docstring for OutletDeviceAPI"""

    @ns.response(OutletDeviceSchema())
    def get(self, name):
        results = OutletDevice.query.filter(OutletDevice.name == name).first()
        return results


@ns.route('/add/')
@ns.doc(description='Do the damn add note thing.')
class OutletDeviceAddAPI(Resource):
    """docstring for OutletDeviceAddAPI"""

    def put(self):
        content = request.get_json()
        # log.debug(logpp(content.__dict__))
        log.debug(logpp(content['name']))
        log.debug(pformat(content['name'], indent=4))
        log.info(pformat(ns.payload, indent=4))
        o = OutletDevice()
        o.name = content['name']
        o.address = content['address']
        o.mac_address = content['mac_address']
        o.dev_id = content['dev_id']
        o.local_key = content['local_key']
        o.status = False
        o.outletgroup_id = 1
        db.session.add(o)
        db.session.commit()
        return o.to_json()
