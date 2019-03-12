#!/usr/bin/env python


import inspect
import logging
import nmap
import os
import sys
print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))

import simplejson

from cachy import CacheManager
from flask import Blueprint
from flask import Flask
from flask import session
from flask_restplus_patched import Api
from flask_restplus_patched import Resource
from flask_restplus_patched import fields
from flask_restplus_patched.reqparse import RequestParser
from flask_restplus_patched.swagger import Swagger
from flask_sqlalchemy import SQLAlchemy
from mcp.logutil import get_logger
from munch import Munch
from munch import munchify
from munch import unmunchify
from pprint import pprint
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session
from sqlalchemy.orm import create_session
from sqlite3 import IntegrityError

from mcp.models.outlet import OutletDevice
from mcp.models.outlet import OutletGroup
from mcp.models.outlet import TuyaDevice

print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))

from mcp import app_name
from mcp import appdir
from mcp import db
from mcp import pwd
from mcp.models import Base

from mcp.controllers import api


log = get_logger(__name__)

log.info('appdir: {0}'.format(appdir))
log.info('pwd: {0}'.format(pwd))

config_path = os.path.join(pwd, 'conf.d')
data_path = os.path.join(pwd + '/../', 'data')
scan_results = os.path.join(data_path, 'scan-results.json')


cache_dir = os.path.join(pwd, '.cache')

device_conf_file = os.path.join('conf.d', 'devices.json')

ns = api.namespace('outlet', description='Outlet Device Control')

@api.doc(responses={404: 'Outlet not found'})
@ns.route('/')
class ListAllDevices(Resource):
    @api.doc(description='List of all outlets')
    def get(self):

        # return outlet_list.list_devices()
        # o = [Munch(d) for d in db.session.query(OutletDevice).all()]
        # o = db.session.query(OutletDevice).all()
        o = OutletDevice.query.all()
        # print(o.serialize().toDict())
        for d in o:
            log.info(d.serialize().toDict())
        # data =
        # log.info(o)
        return [d.serialize().toDict()for d in o]


@api.doc(responses={404: 'Outlet not found'}, params={'outlet_name': 'The outlet name'})
@ns.route('/<string:outlet_name>/')
class OutletEndpoint(Resource):

    @api.doc(description='List of all outlets')
    def get(self, outlet_name):
        # global home_group
        # return home_group.get_device(outlet_name)
        o = db.session.query(OutletDevice).filter(
            OutletDevice.name == outlet_name.lower()).first()

        log.info(o.to_json())
        if o:
            return o.serialize().toDict()
        else:
            return 404
    # @api.doc(parser=outletparser, description='Add new outlet')
    # @api.doc(description='Add new outlet')
    # def put(self, outlet_name):
    #     global home_group

    #     args = parser.parse_args()
    #     d = Munch(args).toDict()
    #     pprint(d)
    #     device = OutletDevice(name=outlet_name, dev_id=args.dev_id,
    #                           address=args.address, local_key=args.local_key)
    #     # group = home_group[args.group]
    #     home_group.add_device(device)
    #     return unmunchify(device)


# @api.doc(responses={404: 'Outlet not found'}, params={'outlet_name': 'The outlet name', 'action': 'on or off'})
# @ns.route('/<string:outlet_name>/status/')


@api.doc(responses={404: 'Outlet not found'}, params={'outlet_name': 'The outlet name', 'action': 'on or off'})
@ns.route('/<string:outlet_name>/<string:action>/')
@ns.route('/<string:outlet_name>/<string:action>/<int:switch>/')
@ns.route('/<string:outlet_name>/control/<string:action>/')
@ns.route('/<string:outlet_name>/control/<string:action>/<int:switch>/')
class OutletControl(Resource):

    @api.doc(description='Control outlets')
    def get(self, outlet_name, action, switch=1):
        outlet_name = outlet_name.lower()
        o = OutletDevice.query.filter(
            OutletDevice.name == outlet_name
        ).first()
        if o is None:
            return {
                "message": "Device not found",
                "name": outlet_name,
            }, 500
        log.debug(o.to_dict())
        device = o.connect_device()
        if action == 'on':
            status = device.turn_on(switch=switch)
            # device.set_status('on', switch=switch)
        elif action == 'off':
            # device.set_status('off', switch=switch)
            status = device.turn_off(switch=switch)
        elif action == 'status':
            status = device.status()

        if isinstance(status, str):

            status = Munch(simplejson.loads(status))
            log.debug('string to json: {0}}'.format(status))
        elif isinstance(status, dict):
            status = Munch(status)

        log.debug('status return type: {0}'.format(type(status)))
        log.debug('status: {0}'.format(status))
        # status = Munch(device.status())
        if status.dps['1'] is True:
            o.status = 1
        elif status.dps['1'] is False:
            o.status = 0
        if o.dev_type_id == 1200758:

            o.timer = status.dps.get('2', 0)

            o.current = status.dps.get('4', 0)
            o.power = status.dps.get('5', 0)
            o.voltage = status.dps.get('6', 0)

        db.session.add(o)
        db.session.commit()
        # device.set_status(action)
        # return simplejson.dumps(o.serialize().toDict())
        return o.serialize().toDict()


def setup_user():
    # user = User(username='Kuro', email='kurohat@gmail.com')
    euser = db.session.query(User).get(1)
    if euser:
        db.session.delete(euser)
        db.session.commit()
    user = User()
    # user.id = 1
    user.username = 'kurohai'
    user.email = 'kurohai@gmail.com'

    db.session.add(user)
    db.session.commit()
    pprint([u.username for u in db.session.query(User).all()])

    pprint(db.session.query(User).get(1))
    # pprint(User.query({'id': 1}))


def setup_device_data():

    scan_results = os.path.join(data_path, 'scan-results.json')

    with open(scan_results, 'r') as f:
        devices = munchify(simplejson.load(f))

    for d in devices:
        for k, v in d.items():
            d[str(k).lower().strip()] = str(v).lower().strip()
            print('value of d: {0}'.format(v))

        # log.debug('adding device: {0}'.format(str(d.toDict())))
        # hg = db.session.query(OutletGroup).filter(
        #     OutletGroup.name == 'Home').first()
        # hg = OutletGroup.query.filter(
        #     OutletGroup.name == 'Home').first()
        if not d:
            pprint(d)
            pprint(type(d))
        else:

            log.info('device matched: {0}'.format(d.name))
            # add_to_group(outlet)
            # dev = OutletDevice.query.filter(
            #     OutletDevice.address == d.address).first()
            dev = OutletDevice.query.filter(
                OutletDevice.dev_id == d.dev_id
            ).first()

            if dev is not None:
                log.debug(dev.to_dict())
                log.info('device {0} found!'.format(d.name))
                if not dev.local_key:
                    dev.local_key = d.local_key
                    db.session.merge(dev)
                    db.session.commit()
                # log.debug(dev.to_dict())
            else:
                log.debug(d.toDict())
                log.info('device {0} not found'.format(d.name))
            # if not db.session.query(OutletDevice).filter(OutletDevice.address == d.address).first():
                outlet = OutletDevice(
                    d.dev_id,
                    d.address,
                    d.local_key,
                    name=d.name,
                )
                outlet.outletgroup_id = 1

                # hg.add_device(outlet)
                db.session.add(outlet)
                try:
                    db.session.commit()
                # except IntegrityError as e:
                    # log.error(e)
                except Exception as e:
                    pass
                    log.error(e)
                # finally:
                #     db.session.rollback()
                #     db.session.flush()
# from flask import current_app
# app = current_app()
# app.register_blueprint(api_blueprint)
