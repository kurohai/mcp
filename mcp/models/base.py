#!/usr/bin/env python


import simplejson

from munch import Munch
from munch import unmunchify
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from flask_sqlalchemy import Model


@as_declarative()
class Base(Model):

    def __hash__(self):
        return hash(self.id)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
