#!/usr/bin/env python


import simplejson

# from flask_restplus import Model
from flask_restplus import OrderedModel
from flask_restplus import Resource
from munch import Munch
from munch import unmunchify
from pytuya import Device as TuyaDevice
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, ForeignKey, Float
from flask_sqlalchemy import Model
from mcp import Base, db


class User(Base, Munch):
    __bind_key__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User {0}>'.format(self.username)
