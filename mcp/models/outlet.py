#!/usr/bin/env python


from munch import Munch
from munch import unmunchify
from munch import munchify
# from flask_restplus import Model
# from flask_restplus import OrderedModel
# from flask_restplus import Resource
from pytuya import Device as TuyaDevice
import simplejson


from mcp import Base, db



class OutletDevice(Base):
    """docstring for OutletDevice"""
    __bind_key__ = 'auth'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=True)
    dev_id = db.Column(db.String(80), unique=True, nullable=True)
    local_key = db.Column(db.String(80), unique=True, nullable=True)
    dev_type = db.Column(db.String(80), unique=False, nullable=True)
    outletgroup_id = db.Column(db.Integer, db.ForeignKey('outletgroup.id'),
        nullable=False)


    def __init__(self, dev_id, address, local_key=None, name='', **kwargs):
        self.dev_type = 'device'
        # super(OutletDevice, self).__init__(dev_id, address, local_key)
        self.name = name or address
        self.address = address
        self.dev_id = dev_id
        self.local_key = local_key
        # if 'group' in kwargs.keys():
        #     self.group = kwargs.pop('group')
        # else:
        #     self.group = 'NoGroup'


    def serialize(self):
        d = Munch()
        d.name = self.name
        d.id = self.id
        d.address = self.address
        d.dev_id = self.dev_id
        d.local_key = self.local_key
        d.dev_type = self.dev_type
        d.outletgroup_id = self.outletgroup_id
        return d

    def to_json(self):
        return self.serialize().toJSON()

    def to_dict(self):
        return self.serialize().toDict()

    def connect_device(self):
        return TuyaDevice(self.dev_id, self.address, local_key=self.local_key)



    # def __repr__(self):
        # for k, v in self.
        # return str(Munch(self).toDict())

class OutletGroup(Base):
    """docstring for OutletGroup"""
    __bind_key__ = 'auth'
    # __tablename__ = 'outlet_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    devices = db.relationship('OutletDevice', backref='outletgroup', lazy=True)


    def __init__(self, name):
        super(OutletGroup, self).__init__()
        self.name = name
    #     self.devices = Munch()

    def add_device(self, device):
        # self.devices[device.name] = device
        # self.add_group('Home')
        if isinstance(device, OutletDevice):
            self.devices.append(device)
        # else:
            # self.devices[device.name.lower()] = OutletDevice(device)


        # if hasattr(device, 'group'):
        #     self.add_group(device.group)

    def list_devices(self):
        # print self.devices.toDict()
        return unmunchify(self.devices)

    def get_device(self, name):
        return self.devices[name]

    # def get_group_by_name(self, name):
    #     if self.name == name:
    #         return self
    #     elif name.lower() in self.keys():

    #         return self.__getattribute__('name')

    # def add_group(self, group):
        # if 'home' in group.lower():
        #     self.devices[]
        # self.devices = self.get_group_by_name(group)

