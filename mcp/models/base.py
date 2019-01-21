#!/usr/bin/env python


import simplejson

from munch import Munch
from munch import unmunchify
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from six import with_metaclass

# from flask_sqlalchemy import Model
from flask_restplus.model import Model
# from mcp import db


@as_declarative()
class Base(object):

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
