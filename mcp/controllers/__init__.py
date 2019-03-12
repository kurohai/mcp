#!/usr/bin/env python

import inspect
import os
import sys

from flask import Flask
from flask_restplus_patched import Api

# from .outlets import api_view as outlets_view

from mcp.logutil import get_logger

log = get_logger(__name__)

# from .outlets import api as outlets_api

log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))


# api_root = Api(
#     title='Outlet Device Control API',
#     description='Control them outlets like a boss.',
#     prefix='/api/v1',
#     # doc='/docs'
#     # endpoint='/api/v1',
# )

# api_root = Api(
#     # 'api_root',
#     title='Home Control API',
#     version='1.0',
#     # endpoint='/api/v1',
# )

from .outlet import ns as outlets_ns
from .outlets import ns as outlets_ns2

log.info('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))

# api_root.add_namespace(outlets_ns)
