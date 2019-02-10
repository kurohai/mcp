#!/usr/bin/env python


import simplejson

from flask_sqlalchemy import Model
from mcp import Base
from mcp import db
from munch import Munch
from munch import unmunchify
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr


class User(Base):
    __bind_key__ = 'auth'

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password_hash

    # def __repr__(self):
    #     return '<User {0}>'.format(self.to_dict())

    def serialize(self):
        d = Munch()
        d.id = self.id
        d.username = self.username
        d.email = self.email
        return d
