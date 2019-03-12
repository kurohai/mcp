#!/usr/bin/env python


# from flask_restplus_patched import Model
# from flask_restplus_patched import OrderedModel
# from flask_restplus_patched import Resource
# from sqlalchemy.ext.declarative import declared_attr
import inspect
import os
import simplejson
print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))

from flask_restplus_patched.model import Model
from flask_restplus_patched.model import ModelSchema
from munch import Munch
from munch import munchify
from munch import unmunchify
from pytuya import AESCipher
from pytuya import Device
from pytuya import PROTOCOL_VERSION_BYTES
from six import with_metaclass
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
# from sqlalchemy.orm import synonym_for

from mcp.logutil import get_logger
from mcp.models import Base


log = get_logger(__name__)
log.info('controller.outlet')
print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))


class OutletDevice(Base):
    """docstring for OutletDevice"""

    __bind_key__ = 'appdata'

    # schema = Base.__schema__


    name = Column(String(80), unique=True, nullable=False)
    address = Column(String(80), unique=False, nullable=True)
    mac_address = Column(String(80), unique=True, nullable=True)

    dev_id = Column(String(80), unique=True, nullable=True)
    local_key = Column(String(80), unique=False, nullable=True)
    dev_type = Column(String(80), unique=False,
                      nullable=False, default='device')
    dev_type_id = Column(Integer, unique=False, nullable=True)

    status = Column(Boolean, unique=False, nullable=False, default=False)

    timer = Column(Integer, unique=False, nullable=True, default=0)
    current = Column(Integer, unique=False, nullable=True, default=0)
    power = Column(Integer, unique=False, nullable=True, default=0)
    voltage = Column(Integer, unique=False, nullable=True, default=0)

    outletgroup_id = Column(
        Integer,
        ForeignKey('outletgroup.id'),
        nullable=False,
        default=1
    )

    def __init__(self, dev_id, address, local_key=None, name='', **kwargs):
        self.dev_type = 'device'
        self.name = name.lower() or address.lower()
        self.address = address.lower()
        self.dev_id = dev_id.lower()
        self.local_key = local_key.lower()
        self.get_dev_type()

    def get_dev_type(self):
        self.mac_address = self._mac_addr()
        self.dev_type_id = self._dev_type_id()

    def _dev_type_id(self):
        return self.dev_id[:8].lower()

    def _mac_addr(self):
        return self.dev_id[8:].lower()

    @validates('dev_id')
    def validate_dev_id(self, dev_id):
        assert len(self.dev_id) == 20
        return dev_id

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

    def connect_device(self):
        return TuyaDevice(self.dev_id, self.address, local_key=self.local_key, dev_type=self.dev_type)


# class OutletDeviceSchema(ModelSchema):
#     class Meta:
#         model = OutletDevice


class OutletGroup(Base):
    """docstring for OutletGroup"""

    # __bind_key__ = 'appdata'

    name = Column(String(80), unique=True, nullable=False)
    devices = relationship('OutletDevice', backref='outletgroup', lazy=True)

    def __init__(self, name):
        super(OutletGroup, self).__init__()
        self.name = name

    def add_device(self, device):
        if isinstance(device, OutletDevice):
            self.devices.append(device)

    def list_devices(self):
        # print self.devices.toDict()
        return str(Munch(self.devices).toDict())

    def get_device(self, name):
        return self.devices[name]


class TuyaDevice(Device):
    """docstring for TuyaDevice"""
    # def __init__(self, dev_id, address, local_key, dev_type):
    #     super(TuyaDevice, self).__init__(dev_id, address, local_key, dev_type)
    #     self.arg = arg

    def turn_on(self, switch=1):
        """Turn the device on"""
        data = self.set_status(True, switch)
        return self.status()

    def turn_off(self, switch=1):
        """Turn the device off"""
        data = self.set_status(False, switch)
        return self.status()

    def _parse_status_result(self, data):
        # log.debug('parsing status data=%r', data)
        log.debug('parsing status data: {0}'.format(data))
        for k, v in enumerate(data):
            if v == b'{':
                log.debug('found it: {0}: {1}'.format(k, v))
        jsondata = simplejson.loads(data[20:-8])

        # log.debug('data decode: {0}'.format(data.decode()))
        result = data[20:-8]  # hard coded offsets
        # result = data[data.find('{'):data.rfind('}')+1]  # naive marker search, hope neither { nor } occur in header/footer
        #print('result %r' % result)
        if result.startswith(b'{'):
            # this is the regular expected code path
            if not isinstance(result, str):
                result = result.decode()
            result = simplejson.loads(result)
        elif result.startswith(PROTOCOL_VERSION_BYTES):
            # got an encrypted payload, happens occasionally
            # expect resulting json to look similar to:: {"devId":"ID","dps":{"1":true,"2":0},"t":EPOCH_SECS,"s":3_DIGIT_NUM}
            # NOTE dps.2 may or may not be present
            # remove version header
            result = result[len(PROTOCOL_VERSION_BYTES):]
            # remove (what I'm guessing, but not confirmed is) 16-bytes of MD5 hexdigest of payload
            result = result[16:]
            cipher = AESCipher(self.local_key)
            result = cipher.decrypt(result)
            log.info('decrypted result=%r', result)
            if not isinstance(result, str):
                result = result.decode()
            result = simplejson.loads(result)
        else:
            log.error('Unexpected status() payload=%r', result)

        return result

    def status(self):
        log.debug('status() entry')
        # open device, send request, then close connection
        payload = self.generate_payload('status')

        data = self._send_receive(payload)
        return self._parse_status_result(data)
