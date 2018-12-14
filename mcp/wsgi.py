import os
import sys
from tuya_controller import app

port = os.environ.get('FLASK_PORT', 9004)
host = os.environ.get('FLASK_HOST', '0.0.0.0')
debug = os.environ.get('FLASK_DEBUG', False)
if debug:
    debug = True
runapp = os.environ.get('RUNAPP', False)

if runapp:
    app.run(
        host=host,
        port=port,
        debug=debug
    )
