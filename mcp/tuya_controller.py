#!/usr/bin/env python


import logging
# import pytuya
import sys

from flask import Blueprint
from flask import Flask
from flask import session
from flask_restplus import Api
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus.reqparse import RequestParser
from flask_restplus.swagger import Swagger
from models import GroupList
from models import OutletDevice
from models import OutletGroup
from munch import Munch
from pprint import pprint


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.getLogger('pytuya').setLevel(logging.DEBUG)


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
parser.add_argument(**parser_name.toDict())
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
home_group = Munch()
home_group = GroupList('')
home_group.Home = OutletGroup('Home')
outlet_list = OutletGroup('Office')
home_group[outlet_list.name] = outlet_list

def add_to_group(device, group='Home'):
    global home_group
    if not group in home_group.keys():
        home_group[group] = OutletGroup(group)
    home_group[group].add_device(device)


monitor_01 = OutletDevice(
    '012007585ccf7f6bfc67',
    '10.0.0.59',
    '245ff3bcc2ba1c40',
    name='monitor-01',
    group = 'Office'
)
# monitor_01.add_to_group()

office_desk_light = OutletDevice(
    '01200885dc4f220f3beb',
    '10.0.0.55',
    'c667624bed01f961',
    name='office-desk-light'
)
# outlet_list.add_device(monitor_01)

add_to_group(office_desk_light)


@api.doc(
    responses={404: 'Group not found'},
    params={'group_name': 'The group name'}
)
@ns.route('/group/')
@ns.route('/group/<string:group_name>/')
class GroupDeviceList(Resource):

    @api.doc(description='List of outlets in group')
    def get(self, group_name=''):
        if group_name in ['Home', 'All']:
            return home_group.toDict()
        elif group_name:
            global home_group
            return home_group[group_name].toDict()
        else:
            return home_group.toDict()

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
        return outlet_list.get_device(outlet_name)

    @api.doc(parser=parser, description='Add new outlet')
    def put(self, outlet_name):
        global home_group

        args = parser.parse_args()
        d = Munch(args).toDict()
        pprint(d)
        device = OutletDevice(name=outlet_name, dev_id=args.dev_id, address=args.address, local_key=args.local_key, group=args.group)
        group = home_group[args.group]
        add_to_group(device, args.group)


if __name__ == '__main__':
    log.info(api)
    pprint(api.__dict__)
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    app.run(
        debug=True,
        port=8080,
        host='0.0.0.0'
    )
