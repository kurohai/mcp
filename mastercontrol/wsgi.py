#!/usr/bin/env python


import inspect
import os
import sys

from . import create_app
from . import db
from .logutil import get_logger
from pprint import pprint


log = get_logger(__name__)
app = create_app('default')

port = os.environ.get('FLASK_PORT', 9008)
host = os.environ.get('FLASK_HOST', '0.0.0.0')
debug = os.environ.get('FLASK_DEBUG', True)

if debug:
    debug = True


log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(),
    p=os.path.realpath(__file__),
    n=__name__)
)

# pprint(app)

log.debug('url map: {0}'.format(app.url_map))

if __name__ == '__main__':

    app.run(
        port=port,
        host=host,
        debug=debug,
    )
