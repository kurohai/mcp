#!/usr/bin/env python


import inspect
import os
import simplejson

from flask_restplus_patched.model import Model
from flask import current_app
from munch import Munch
from munch import unmunchify
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from mcp.logutil import get_logger


log = get_logger(__name__)


log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))


# @as_declarative()
class Base(Model):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return '<{1} {0}>'.format(
            str(self.to_dict()),
            self.__class__
        )

    def serialize(self):
        d = Munch()
        d.id = self.id
        return d

    def to_json(self):
        return self.serialize().toJSON()

    def to_dict(self):
        return self.serialize().toDict()


# @as_declarative()
class TuyaBase(Model):
    """docstring for TuyaBase"""


    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # @declared_attr
    # def id(self):
    #     return Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return '<{1} {0}>'.format(
            str(self.to_dict()),
            self.__class__
        )

    def serialize(self):
        d = Munch()
        d.id = self.id
        return d

    def to_json(self):
        return self.serialize().toJSON()

    def to_dict(self):
        return self.serialize().toDict()
