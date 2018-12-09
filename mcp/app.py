#!/usr/bin/env python


from flask import Blueprint
from flask import Flask
from flask_restplus import Api
# from flask_restplus import Model
# from flask_restplus import OrderedModel
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus.swagger import Swagger


from models import DeviceList
from models import Device


api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(
    api_v1, version='1.0',
    title='Device API',
    description='A device control API',
)

ns = api.namespace('devices', description='Google Home Devices')


swag = Swagger(api)

google_devices = DeviceList('living-room')
main_speaker = Device(name='main-speaker', ip='10.0.0.11', room='Living Room')
main_tv = Device(name='main-tv', ip='10.0.0.12', room='Living Room')
google_devices.add_device(main_tv)
google_devices.add_device(main_speaker)


# todo = api.model('Todo', {
#     'task': fields.String(required=True, description='The task details')
# })

# listed_todo = api.model('ListedTodo', {
#     'id': fields.String(required=True, description='The todo ID'),
#     'todo': fields.Nested(todo, description='The Todo')
# })


def abort_if_device_doesnt_exist(device_name):
    if device_name not in google_devices:
        api.abort(404, "Device {0} doesn't exist".format(device_name))


parser = api.parser()
parser.add_argument('name', type=str, required=True,
                    help='The device', location='form')
parser.add_argument('ip', type=str, required=True,
                    help='The device', location='form')
parser.add_argument('room', type=str, required=False,
                    help='The device', location='form')
parser.add_argument('type', type=str, required=False,
                    help='The device', location='form')
parser.add_argument('id', type=int, required=False,
                    help='The device')


@ns.route('/<string:device_name>/')
@api.doc(responses={404: 'Device not found'}, params={'device_name': 'The Device Name'})
class DeviceView(Resource):
    '''Show a single device and let you delete or update it'''

    @api.doc(description='device_name should be in {0}'.format(', '.join(google_devices.keys())))
    def get(self, device_name):
        '''Fetch a device resource'''
        print(
            'device_name should be in {0}'.format(
                ', '.join(google_devices.keys())
            )
        )
        abort_if_device_doesnt_exist(device_name)
        print('device requested: {0}'.format(google_devices[device_name]))
        return google_devices.get_device(device_name)

    @api.doc(responses={204: 'Device deleted'})
    def delete(self, device_name):
        '''Delete a device resource'''
        abort_if_device_doesnt_exist(device_name)
        del google_devices[device_name]
        return '', 204

    @api.doc(parser=parser)
    def put(self, device_name):
        '''Update a device resource'''
        args = parser.parse_args()
        print args
        device = Device(**args)
        google_devices.add_device(device)
        return google_devices.get_device(device.name)


@ns.route('/')
class DeviceList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''

    def get(self):
        '''List all device groups'''
        return google_devices.items()

    @api.doc(parser=parser)
    def post(self):
        '''Create a group of devices'''
        args = parser.parse_args()
        google_devices.add_device({'device': args['device']})
        return google_devices.get_device(device_name), 201


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    app.run(debug=True)
