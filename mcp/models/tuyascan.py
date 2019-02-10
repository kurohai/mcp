#!/usr/bin/env python


import os, inspect
import simplejson
print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

# from mcp import Base, TuyaBase
from flask_sqlalchemy import Model
from mcp.logutil import get_logger
from mcp.models import TuyaBase
print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

from munch import *
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

print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))




class TuyaScan(TuyaBase):
    __bind_key__ = 'tuya_device'


    ip              = Column(String(80), unique=False, nullable=True)
    gwId            = Column(String(80), unique=True, nullable=False, primary_key=True)
    active          = Column(String(80), unique=False, nullable=True)
    ability         = Column(String(80), unique=False, nullable=True)
    mode            = Column(String(80), unique=False, nullable=True)
    encrypt         = Column(String(80), unique=False, nullable=True)
    productKey      = Column(String(80), unique=False, nullable=True)
    version         = Column(String(80), unique=False, nullable=True)
    mac_address     = Column(String(80), unique=False, nullable=True)
    dev_type_id     = Column(String(80), unique=False, nullable=True)
    dev_type_name   = Column(String(80), unique=False, nullable=True)

    def get_dev_type(self):
        self.mac_address = self._mac_address()
        self.dev_type_id = self._dev_type_id()

    def _dev_type_id(self):
        return self.gwId[:8].lower()

    def _mac_address(self):
        return self.gwId[8:].lower()



    # @_mac_address.setter
    # def _mac_address(self, dev_id):
    #     """Set the value of mac_address.
    #     """

    #     self.mac_address = dev_id[8:].lower()

    def get_dev_type_name(self, dev_type_id, productKey):
        """TODO: Add product name lookup here
        """
        # return session.query(TuyaProduct) # etc...
        return 'outlet-device'


    def get_session(self):
        self._session = Session()
        return self._session


    def serialize(self):
        d = Munch()
        d.ip = self.ip
        d.gwId = self.gwId
        d.active = self.active
        d.ability = self.ability
        d.mode = self.mode
        d.encrypt = self.encrypt
        d.productKey = self.productKey
        d.version = self.version
        d.mac_address = self.mac_address
        d.dev_type_id = self.dev_type_id
        d.dev_type_name = self.dev_type_name

        return d


print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
