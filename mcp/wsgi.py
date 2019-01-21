#!/usr/bin/env python


import os
import sys
from controllers.outlet import app

port = os.environ.get('FLASK_PORT', 9004)
host = os.environ.get('FLASK_HOST', '0.0.0.0')
debug = os.environ.get('FLASK_DEBUG', False)
if debug:
    debug = True

if __name__ == '__main__':

    app.run(
        port=port,
        host=host,
        debug=debug,
    )
