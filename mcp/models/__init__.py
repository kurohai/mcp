#!/usr/bin/env python

import inspect
import os

from mcp.logutil import get_logger

log = get_logger(__name__)

log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))

from base import Base
log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))

from base import TuyaBase
log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))

from tuyascan import TuyaScan
log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))

# from user import User
# print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

from outlet import OutletDevice
from outlet import OutletGroup
log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))
