#!/usr/bin/env python

app_name = 'mcp'
__version__ = '1.0.1'

import inspect
import os

from flask import Flask
from flask import redirect
from flask import request
from flask_restplus_patched import Swagger
from flask_sqlalchemy import SQLAlchemy
from munch import *
from pprint import pformat
from pprint import pprint
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from flask_restplus_patched import Api

from logutil import get_logger
from logutil import logging
from models import Base
from models import TuyaBase
from utilities.sesh import db_connection
from utilities.sesh import db_session

log = get_logger(__name__)
log.setLevel(logging.DEBUG)
logging.getLogger('pytuya').setLevel(logging.DEBUG)

appdir = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.dirname(appdir)

SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI = 'sqlite:///{p}/{a}.db'.format(p=pwd, a='mcp')
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
MYSQL_HOSTNAME = os.environ.get('MYSQL_HOSTNAME', 'kurohai.com')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'mastercontrol')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{u}:{p}@{h}/{d}'.format(
    u=MYSQL_USERNAME,
    p=MYSQL_PASSWORD,
    h=MYSQL_HOSTNAME,
    d=MYSQL_DATABASE,
)

SQLALCHEMY_BINDS = Munch({
    'appdata': SQLALCHEMY_DATABASE_URI,
    'tuya_device': 'sqlite:////{p}/{a}.db'.format(p=pwd, a='tuya-device'),
    # 'auth':    SQLALCHEMY_DATABASE_URI,
    # 'appdata': 'sqlite:////{p}/{a}.db'.format(p=pwd, a='mcp-data'),
})

app = Flask(app_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS.toDict()

# def init_app(app):
#     api_v1_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
#     api.api_v1.init_app(api_v1_blueprint)
#     app.register_blueprint(api_v1_blueprint)


# pprint(type(Base))
Session = sessionmaker(
    binds={
        Base: create_engine(SQLALCHEMY_BINDS.appdata),
        TuyaBase: create_engine(SQLALCHEMY_BINDS.tuya_device),
    },
    expire_on_commit=False,
)

db_sesh_mcp, engine_mcp = db_connection(SQLALCHEMY_BINDS.appdata)
db_sesh_tuya, engine_tuya = db_connection(SQLALCHEMY_BINDS.tuya_device)
db = SQLAlchemy(app)
from models import OutletDevice
from models import OutletGroup
from models import TuyaScan

# Session_mcp = sessionmaker(engine_mcp)
# Session_tuya = sessionmaker(engine_tuya)

# Base.metadata = MetaData(bind=engine_mcp)
Base.query = db_sesh_mcp.query_property()

# TuyaBase.metadata = MetaData(bind=engine_tuya)
TuyaBase.query = db_sesh_tuya.query_property()


# db = SQLAlchemy(app, model_class=Base)

def _check_path(url):
    if not url.endswith('/') and not url.endswith('.json'):
        return True
    else:
        return False

@app.before_request
def add_trailing():
    rp = request.path

    log.info('pre-path: {0}'.format(rp))
    log.info('method: {0}'.format(request.method))
    log.info('post-path: {0}'.format(str(request.path)))
    if _check_path(rp):
        return redirect(rp + '/')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
    db_sesh_mcp.remove()
    db_sesh_tuya.remove()


log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

api_root = Api(
    title='Outlet Device Control API',
    description='Control them outlets like a boss.',
    prefix='/api/v1',
    # doc='/docs'
    # endpoint='/api/v1',
)


# from controllers import outlets_api
from controllers import outlets_ns
from controllers import outlets_ns2
# from controllers import Outlets
# pprint(dir(api_root))
# print('\n\n\n')
log.debug(pformat(api_root.__dict__, indent=4))
# api_root.init_app(app)
# log.debug(pformat(api_root.__dict__, indent=4))
log.debug(pformat(app.__dict__, indent=4))
api_root.add_namespace(outlets_ns)
api_root.init_app(app)
# app.register_blueprint(outlets_view)
# print('\n\n\n')
# pprint(dir(api_root))
# api_root.
# swag = Swagger(api_root)


log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
# log.debug(dir(api_root))
# outlets_api.register_model()




# print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
# from controllers import api
# # swag = Swagger(api)

# from controllers import api_blueprint
# from controllers.outlet import api as outlet_api
# from controllers.outlet import ns as outlet_ns
# # from controllers.outlet import ns as outlet_ns
# # from controllers.hdmi import ns as hdmi_ns
# # from controllers.hdmi import ns as hdmi_ns

# print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
# # app.register_blueprint(api_blueprint)
# # outlet_api.init_app(app)

# # outlet_api.add_namespace(outlet_ns)
# outlet_ns.add_model('OutletDevice', OutletDevice)
# # outlet_ns.model(name='OutletDevice', model=OutletDevice)
# # outlet_api.app = app
# app.register_blueprint(api_blueprint)

# swag = Swagger(outlet_api)

# # OutletDevice.name = OutletDevice.__class__
# # schema = swag.serialize_schema(OutletDevice)
# # swag.register_model(OutletDevice)

# # outlet_api._schema = swag.as_dict()
# # swag.register_model(TuyaScan)
# print('api stuff')
# pprint(dir(Base))
# pprint(Base.__dict__)
# print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
# pprint(dir(outlet_api))
# pprint(outlet_api.__dict__)
# print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
# pprint(dir(outlet_ns))
# pprint(outlet_ns.__dict__)
# print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
# print(outlet_api.models)
