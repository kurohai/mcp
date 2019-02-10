#!/usr/bin/env python


import logging
import nmap
import os
import sys
import inspect
print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

import simplejson

from cachy import CacheManager
from flask import Blueprint
from flask import Flask
from flask import session
from flask_restplus import Api
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus.reqparse import RequestParser
from flask_restplus.swagger import Swagger
from flask_sqlalchemy import SQLAlchemy
from munch import Munch
from munch import munchify
from munch import unmunchify
from pprint import pprint
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session
from sqlalchemy.orm import create_session
from sqlite3 import IntegrityError
# from mcp.parser import outletparser
from mcp.logutil import get_logger

from mcp.models.outlet import OutletDevice
from mcp.models.outlet import OutletGroup
from mcp.models.outlet import TuyaDevice

print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

from mcp import app
from mcp import db
from mcp.models import Base
from mcp.models.user import User

from mcp.controllers import api
from mcp.controllers import api_blueprint

logging.basicConfig(level=logging.DEBUG)
log = get_logger(__name__)
log.setLevel(logging.DEBUG)
logging.getLogger('pytuya').setLevel(logging.DEBUG)
appdir = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.dirname(appdir)

log.info('appdir: {0}'.format(appdir))
log.info('pwd: {0}'.format(pwd))

config_path = os.path.join(pwd, 'conf.d')
data_path = os.path.join(pwd + '/../', 'data')
scan_results = os.path.join(data_path, 'scan-results.json')


cache_dir = os.path.join(pwd, '.cache')

cachy_conf = Munch()
cachy_conf.default = 'file'
cachy_conf.serializer = 'json'
cachy_conf.stores = Munch()
cachy_conf.stores.file = Munch()
cachy_conf.stores.file.driver = 'file'
cachy_conf.stores.file.path = cache_dir
device_conf_file = os.path.join('conf.d', 'devices.json')

cache = CacheManager(cachy_conf)

# SQLALCHEMY_DATABASE_URI = 'sqlite:////{p}/{a}.db'.format(p=pwd, a='mcp')
# SQLALCHEMY_BINDS = {
#     'users':        'mysqldb://localhost/users',
#     'appmeta':      'sqlite:////path/to/appmeta.db'
# }


def prep_device_list(conf_file_path):
    # global device_list
    device_list = munchify(simplejson.load(open(conf_file_path, 'r')))
    # log.debug(muncherator(device_list))
    for k, v in device_list.items():
        v.mac = parse_mac_from_id(v.dev_id)
        device_list[k] = v
    return device_list


def muncherator(obj):
    return simplejson.dumps(
        unmunchify(obj),
        indent=4,
    )


def parse_mac_from_id(device_id):
    s = device_id[-12:]
    mac = str()
    for i in xrange(0, 12, 2):
        mac += ':' + s[i:i + 2]
    return mac[1:]


device_list = prep_device_list(device_conf_file)


def get_device(key):
    # for k, v in device_list.items():
    d = cache.get(key)
    if d is None:
        # cache.forget(key)
        return None
    else:
        print 'key', key
        device = munchify(d)
        print(muncherator(device))
        return device


# sys.exit(0)


# api_blueprint = Blueprint(
#     'api',
#     __name__,
#     url_prefix='/api/v1'
# )
# api = Api(
#     api_blueprint,
#     version='1.0',
#     title='Outlet API',
#     description='An outlet control API',
# )
ns = api.namespace('outlet', description='Smart Life Outlets')


# swag = Swagger(api)


# swag.register_model(OutletDevice)
# swag.register_model(OutletGroup)


global home_group
# home_group = Munch()
home_group = OutletGroup('Home')
# home_group.Home = OutletGroup('Home')
# outlet_list = OutletGroup('Office')
# home_group[outlet_list.name] = outlet_list


def add_to_group(device, group='Home'):
    global home_group
    if group == 'Home':
        home_group.add_device(device)
    # elif not group in home_group.keys():
    #     home_group[group] = OutletGroup(group)
    #     home_group[group].add_device(device)


# monitor_01 = OutletDevice(
#     '012007585ccf7f6bfc67',
#     '10.0.0.59',
#     '245ff3bcc2ba1c40',
#     name='monitor-01',
#     # group = 'Office'
# )
# monitor_01.add_to_group()

# office_desk_light = OutletDevice(
#     '01200885dc4f220f3beb',
#     '10.0.0.55',
#     'c667624bed01f961',
#     name='office-desk-light',
#     # group='Office'
# )
# outlet_list.add_device(monitor_01)

# add_to_group(monitor_01)
# for k in dnames:
#     device = get_device(k)
#     if device:
#         outlet = OutletDevice(
#             device.dev_id,
#             device.address,
#             device.local_key,
#             name=k,

#         )

#         add_to_group(outlet)

# @api.doc(
#     responses={404: 'Group not found'},
#     params={'group_name': 'The group name'}
# )
# @ns.route('/group/')
# @ns.route('/group/<string:group_name>/')
# class GroupDeviceList(Resource):

#     @api.doc(description='List of outlets in group')
#     def get(self, group_name=''):
#         if group_name in ['Home', 'All']:
#             return home_group.toDict()
#         elif group_name:
#             global home_group
#             return home_group[group_name].toDict()
#         else:
#             return home_group.toDict()

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


def database_setup(db, app):
    db.init_app(app)
    # db.drop_all()
    # db.create_all(bind='auth')
    # db.create_all(bind='appdata')
    db.create_all()
    return db, app


def setup_home_group():
    # hg = db.session.query(OutletGroup).filter(OutletGroup.name == 'Home').first()
    hg = OutletGroup.query.filter(
        OutletGroup.name == 'Home'
    ).first()

    if not hg:
        hg = home_group
        db.session.add(home_group)
        db.session.commit()


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


# app.register_blueprint(api_blueprint)
