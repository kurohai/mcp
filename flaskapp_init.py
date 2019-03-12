#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: kurohai
# @Date:   2015-11-18 21:47:31
# @Last Modified by:   Evan
# @Last Modified time: 2016-05-04 19:54:50


from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, inspect
from sqlalchemy import MetaData, Table
from sqlalchemy.ext.declarative import *
from flask import Flask
import datetime
import os
from dicto import dicto
import flask.ext.restless
from flask.ext.socketio import SocketIO
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from settings import config
import logging


appname = config.appname
appnamed = config.appnamed
pwd = config.pwd

dbpath = config.dbpath
dburi = config.dburi
# if os.path.exists(dbpath):
#     print 'db path yes'
# print 'pwd:', pwd
# print 'dburi:', dburi
# print 'dbpath:', dbpath

@as_declarative()
class BaseBase(dicto):

    def __hash__(self):
        return hash(self.id)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = BaseBase

engine = create_engine(dburi)
metadata = MetaData(bind=engine)
session = Session(engine)
db_session = scoped_session(
    sessionmaker(
        autocommit=True,
        autoflush=True,
        bind=engine
    )
)

Base.metadata = metadata
Base.query = db_session.query_property()


from models import *
from log_models import Log
from app import flasktemplate, log
from forms import *
from login import login_manager
from views import blueprint
from log_view import log_blueprint

flasktemplate.register_blueprint(blueprint)
flasktemplate.register_blueprint(log_blueprint)
