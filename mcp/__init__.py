#!/usr/bin/env python

app_name = 'mcp'
__version__ = '1.0.1'

import inspect
import os

from flask import Flask
from flask import redirect
from flask import request
from flask_sqlalchemy import SQLAlchemy
from munch import *
from pprint import pprint
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from models import Base
from models import TuyaBase
from utilities.sesh import db_connection
from utilities.sesh import db_session


appdir = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.dirname(appdir)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///{p}/{a}.db'.format(p=pwd, a='mcp')
SQLALCHEMY_BINDS = Munch({
    'appdata': SQLALCHEMY_DATABASE_URI,
    'tuya_device':'sqlite:////{p}/{a}.db'.format(p=pwd, a='tuya-device'),
    # 'auth':    SQLALCHEMY_DATABASE_URI,
    # 'appdata': 'sqlite:////{p}/{a}.db'.format(p=pwd, a='mcp-data'),
})

app = Flask(app_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS.toDict()


pprint(type(Base))
Session = sessionmaker(
    binds = {
        Base: create_engine(SQLALCHEMY_BINDS.appdata),
        TuyaBase: create_engine(SQLALCHEMY_BINDS.tuya_device),
    },
    expire_on_commit = False,
)
# pprint(type(Base))
# pprint(dir(Base))
# pprint(type(Base.metadata.tables))
# pprint(Base.metadata.tables)
db_sesh_mcp, engine_mcp = db_connection(SQLALCHEMY_BINDS.appdata)
db_sesh_tuya, engine_tuya = db_connection(SQLALCHEMY_BINDS.tuya_device)
Base.metadata.create_all(engine_mcp)
TuyaBase.metadata.create_all(engine_tuya)

# Session_mcp = sessionmaker(engine_mcp)
# Session_tuya = sessionmaker(engine_tuya)

# Base.metadata = MetaData(bind=engine_mcp)
# Base.query = db_sesh_mcp.query_property()

# TuyaBase.metadata = MetaData(bind=engine_tuya)
# TuyaBase.query = db_sesh_tuya.query_property()



# db = SQLAlchemy(app, model_class=Base)
db = SQLAlchemy(app)

@app.before_request
def add_trailing():
    rp = request.path
    if not rp.endswith('/'):
        return redirect(rp + '/')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
    db_sesh_mcp.remove()
    db_sesh_tuya.remove()
