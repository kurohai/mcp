#!/usr/bin/env python


import inspect
import os
import sys

from flask import Blueprint
from flask_restplus_patched import Api
from flask_restplus_patched import Namespace
from flask_restplus_patched import Resource
from flask_restplus_patched.model import ModelSchema
from munch import Munch
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from flask_restplus_patched import fields

from mcp.models import TuyaScan
from mcp.utilities import json
from mcp import db, engine_mcp
from mcp.logutil import get_logger

log = get_logger(__name__)


class Outlets(db.Model):

    # __tablename__ = 'smart_outlets'
    __bind_key__ = 'appdata'
    # schema = OutletsSchema

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=True)
    mac_address = db.Column(db.String(80), unique=True, nullable=True)

    dev_id = db.Column(db.String(80), unique=True, nullable=False)
    local_key = db.Column(db.String(80), unique=False, nullable=True)
    dev_type = db.Column(db.String(80), unique=False,
                      nullable=False, default='device')
    dev_type_id = db.Column(db.Integer, unique=False, nullable=True)

    status = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    timer = db.Column(db.Integer, unique=False, nullable=True, default=0)
    current = db.Column(db.Integer, unique=False, nullable=True, default=0)
    power = db.Column(db.Integer, unique=False, nullable=True, default=0)
    voltage = db.Column(db.Integer, unique=False, nullable=True, default=0)


    # name = fields.Integer()
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def id(self):
        return db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return '<{1} {0}>'.format(
            str(self.to_dict()),
            self.__class__
        )

    def get_dev_type(self):
        self.mac_address = self._mac_addr()
        self.dev_type_id = self._dev_type_id()

    def _dev_type_id(self):
        return self.dev_id[:8].lower()

    def _mac_addr(self):
        return self.dev_id[8:].lower()

    def serialize(self):
        d = Munch()
        d.name = self.name
        d.id = self.id
        d.address = self.address
        d.mac_address = self.mac_address

        d.dev_id = self.dev_id
        d.local_key = self.local_key
        d.dev_type = self.dev_type
        d.dev_type_id = self.dev_type_id

        d.timer = self.timer
        d.current = self.current
        d.power = self.power
        d.voltage = self.voltage

        d.status = self.status

        d.outletgroup_id = self.outletgroup_id
        return d

    def to_json(self):
        return self.serialize().toJSON()

    def to_dict(self):
        return self.serialize().toDict()

class OutletsSchema(ModelSchema):
    class Meta:
        model = Outlets



# data = Munch()
# for i in xrange(10):
#     data = Outlets()

#     data.name = 'test-outlet-{0}'.format(str(i).zfill(2))
#     data.dev_id = '123devid{0}'.format(str(i).zfill(2))
#     data.status = 'False'
#     db.session.add(data)
#     db.session.commit()

# # db.
# Outlets.metadata.create_all(bind=engine_mcp)


log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

# api = Api(
#     title='Outlet Device Control API',
#     description='Control them outlets like a boss.',
#     # prefix='/api/v1',
#     # endpoint='/api/v1',
# )

# ns = api.namespace(
#     'outlets',
#     description='Outlet Device Control API',
#     path='/outlets'
# )
api_view = Blueprint('outlets', __name__, url_prefix='/api/v1')

ns = Namespace(
    api_view,
    description='Outlet Device Control API',
    path='/outlets'
)

# model = ns.model(name='Outlets', model=Outlets)

log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))



@ns.route('/')
@ns.doc('List Outlet Devices')
class OutletsListAPI(Resource):
    """docstring for OutletsAPI"""

    @ns.response(OutletsSchema(many=True))
    def get(self):
        log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

        data = db.session.query(Outlets).all()
        return data



@ns.route('/<string:outlet_name>/')
class OutletsAPI(Resource):
    """docstring for OutletsAPI"""


    # @ns.doc('Get Outlet Device by Name', params={'outlet_name': 'The outlet name'})
    @ns.response(OutletsSchema())
    @ns.doc('Get Outlet Device by Name', responses={404: 'Outlet not found'})
    def get(self, outlet_name):
        log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
        log.info('getting outlet: {0}'.format(outlet_name))
        name = str(outlet_name).lower().strip().replace(' ', '-')
        data = db.session.query(Outlets).filter(Outlets.name == name).first()
        if data is None:
            log.error('outlet not found: {0}'.format(outlet_name))
            return {'result': 'error 404'}, 404
        else:
            return data

    # @ns.response(OutletsSchema())
    @ns.expect(OutletsSchema())
    @ns.doc('Create New Outlet Device')
    def post(self, outlet_name):
        return {'post': 'success'}



log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
