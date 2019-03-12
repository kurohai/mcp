#!/usr/bin/env python


from datetime import datetime as dt
from flask_restplus_patched.model import ModelSchema
from logutil import get_logger
from munch import Munch
from munch import munchify
from munch import unmunchify
from flask_marshmallow import Schema
from .basemodel import BaseModel
from .basemodel import db



log = get_logger(__name__)


class Notable(BaseModel, db.Model):
    """docstring for Notable"""

    # __tablename__ = 'notable'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(64), unique=False, nullable=False)
    time_created = db.Column(
        db.DateTime,
        unique=False,
        nullable=False,
        default=dt.now
    )

    def serialize(self):
        d = Munch()
        d.id = self.id
        d.name = self.name
        d.time_created = self.time_created.strftime('%Y-%m-%d-%H%M')
        return d

    # def to_json(self):
    #     return self.serialize().toJSON()

    # def to_dict(self):
    #     return self.serialize().toDict()


class NotableSchema(ModelSchema):
    class Meta:
        model = Notable

Notable.__schema__ = NotableSchema



class OutletDevice(BaseModel, db.Model):
    """docstring for OutletDevice"""

    __tablename__ = 'outletdevice'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=True)
    mac_address = db.Column(db.String(80), unique=True, nullable=True)

    dev_id = db.Column(db.String(80), unique=True, nullable=True)
    local_key = db.Column(db.String(80), unique=False, nullable=True)
    dev_type = db.Column(db.String(80), unique=False,
                      nullable=False, default='device')
    dev_type_id = db.Column(db.Integer, unique=False, nullable=True)

    status = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    timer = db.Column(db.Integer, unique=False, nullable=True, default=0)
    current = db.Column(db.Integer, unique=False, nullable=True, default=0)
    power = db.Column(db.Integer, unique=False, nullable=True, default=0)
    voltage = db.Column(db.Integer, unique=False, nullable=True, default=0)


    outletgroup_id = db.Column(
        db.Integer,
        db.ForeignKey('outletgroup.id'),
        nullable=False,
        default=1
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


class OutletDeviceSchema(ModelSchema):
    class Meta:
        model = OutletDevice

OutletDevice.__schema__ = OutletDeviceSchema


class OutletGroup(BaseModel, db.Model):
    """docstring for OutletGroup"""

    # __bind_key__ = 'appdata'
    __tablename__ = 'outletgroup'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(80), unique=True, nullable=False)
    devices = db.relationship('OutletDevice', backref='outletgroup', lazy=True)


    def add_device(self, device):
        if isinstance(device, OutletDevice):
            self.devices.append(device)

    def list_devices(self):
        # print self.devices.toDict()
        return str(Munch(self.devices).toDict())

    def get_device(self, name):
        return self.devices[name]


class OutletGroupSchema(ModelSchema):
    class Meta:
        model = OutletGroup

OutletGroup.__schema__ = OutletGroupSchema
