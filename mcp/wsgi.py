#!/usr/bin/env python


import inspect
import os
import sys

from . import app
from .logutil import get_logger

log = get_logger(__name__)


port = os.environ.get('FLASK_PORT', 9002)
host = os.environ.get('FLASK_HOST', '0.0.0.0')
debug = os.environ.get('FLASK_DEBUG', False)

if debug:
    debug = True

from pprint import pprint
pprint('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(), p=os.path.realpath(__file__), n=__name__))
pprint(app)
if __name__ == '__main__':

    app.run(
        port=port,
        host=host,
        debug=debug,
    )
