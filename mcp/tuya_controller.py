#!/usr/bin/env python


import logging
import nmap
import os
import sys

from cachy import CacheManager
from flask import Blueprint
from flask import Flask
from flask import session
from flask_restplus import Api
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus.reqparse import RequestParser
from flask_restplus.swagger import Swagger
from logutil import get_logger
from models import GroupList
from models import OutletDevice
from models import OutletGroup
from munch import Munch
from munch import munchify
from munch import unmunchify
from pprint import pprint
import simplejson


logging.basicConfig(level=logging.DEBUG)
log = get_logger(__name__)
log.setLevel(logging.DEBUG)
logging.getLogger('pytuya').setLevel(logging.DEBUG)
appdir = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.dirname(appdir)

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


def prep_device_list(conf_file_path):
    global device_list
    device_list = munchify(simplejson.load(open(conf_file_path, 'r')))
    # log.debug(muncherator(device_list))
    for k, v in device_list.items():
        v.mac = parse_mac_from_id(v.dev_id)
        device_list[k] = v
    return device_list


dnames = [
    'smart-outlet-01',
    'smart-outlet-02',
    'smart-outlet-03',
    'smart-outlet-04',
    'smart-outlet-05',
    'smart-outlet-06',
    'bedroom-lamp',
    'media-controller',
    'main-strip-01',
    'dblr-box',
    'dblr-screen',
    'office-desk-light',
    'office-lamp'
]


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
        cache.forget(key)
        return None
    else:
        print 'key', key
        device = munchify(d)
        print(muncherator(device))
        return device


# sys.exit(0)


api_blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api/v1'
)
api = Api(
    api_blueprint,
    version='1.0',
    title='Outlet API',
    description='An outlet control API',
)
ns = api.namespace('outlet', description='Smart Life Outlets')

parser_base = Munch()
parser_base.name = ''
parser_base.type = str
parser_base.required = True
parser_base.help = 'Data'
parser_base.location = 'form'


parser_name = parser_base.copy()
parser_name.name = 'name'
parser_name.help = 'The device name'

parser_dev_id = parser_base.copy()
parser_dev_id.name = 'dev_id'

parser_address = parser_base.copy()
parser_address.name = 'address'

parser_local_key = parser_base.copy()
parser_local_key.name = 'local_key'

parser_group = parser_base.copy()
parser_group.name = 'group'
parser_group.required = False


# parser = api.parser()
parser = RequestParser()
# parser.add_argument(**parser_name.toDict())
parser.add_argument(**parser_dev_id.toDict())
parser.add_argument(**parser_address.toDict())
parser.add_argument(**parser_group.toDict())
parser.add_argument(**parser_local_key.toDict())
pprint(parser.args)
for a in parser.args:
    print a.name
    print a.type
# parser.add_argument(
#     'name',
#     type=str,
#     required=True,
#     help='The device',
#     location='form'
# )

swag = Swagger(api)


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
for k in dnames:
    device = get_device(k)
    if device:
        outlet = OutletDevice(
            device.dev_id,
            device.address,
            device.local_key,
            name=k,

        )
        add_to_group(outlet)

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
        global home_group

        # return outlet_list.list_devices()
        return home_group.toDict()


@api.doc(responses={404: 'Outlet not found'}, params={'outlet_name': 'The outlet name'})
@ns.route('/device/<string:outlet_name>/')
class OutletEndpoint(Resource):

    @api.doc(description='List of all outlets')
    def get(self, outlet_name):
        global home_group
        return home_group.get_device(outlet_name)

    @api.doc(parser=parser, description='Add new outlet')
    def put(self, outlet_name):
        global home_group

        args = parser.parse_args()
        d = Munch(args).toDict()
        pprint(d)
        device = OutletDevice(name=outlet_name, dev_id=args.dev_id,
                              address=args.address, local_key=args.local_key)
        # group = home_group[args.group]
        home_group.add_device(device)
        return unmunchify(device)


@api.doc(responses={404: 'Outlet not found'}, params={'outlet_name': 'The outlet name', 'action': 'on or off'})
@ns.route('/device/<string:outlet_name>/control/<string:action>/')
@ns.route('/device/<string:outlet_name>/control/<string:action>/<int:switch>/')
class OutletControl(Resource):

    @api.doc(description='Control outlets')
    def get(self, outlet_name, action, switch=1):
        global home_group
        device = home_group.get_device(outlet_name)
        if action == 'on':
            device.turn_on(switch=switch)
        elif action == 'off':
            device.turn_off(switch=switch)

        # device.set_status(action)
        return device.status()


app = Flask(__name__)
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    log.info(api)
    pprint(api.__dict__)
    # app = Flask(__name__)
    app.run(
        debug=True,
        port=8080,
        host='0.0.0.0'
    )
