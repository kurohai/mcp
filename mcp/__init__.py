#!/usr/bin/env python

app_name = 'mcp'
__version__ = '1.0.1'

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Base

appdir = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.dirname(appdir)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///{p}/{a}.db'.format(p=pwd, a='mcp')
SQLALCHEMY_BINDS = {
    'auth':    SQLALCHEMY_DATABASE_URI,
    'appdata':'sqlite:////{p}/{a}.db'.format(p=pwd, a='mcp-data')
}

app = Flask(app_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
db = SQLAlchemy(app, model_class=Base)
from models import OutletDevice
