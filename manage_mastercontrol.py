#!/usr/bin/env python


import cherrypy
import os

from flask_script import Manager
from mastercontrol import create_app
from mastercontrol import db
from mastercontrol.logutil import get_logger
# from mastercontrol.basemodel import BaseModel
from mastercontrol.models import Notable
from mastercontrol.models import OutletDevice
from mastercontrol.models import OutletGroup
from mastercontrol.utilities.sesh import db_connection
from mastercontrol.utilities.sesh import db_session
from pprint import pformat
from pprint import pprint
from sqlalchemy.orm.session import Session

log = get_logger(__name__)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
# db.init_app(app)
# migrate = Migrate(app, db)
port = os.environ.get('FLASK_PORT', 9008)
host = os.environ.get('FLASK_HOST', '0.0.0.0')
debug = os.environ.get('FLASK_DEBUG', True)


@manager.command
def dbinit():
    # from mastercontrol.basemodel import BaseModel
    from mastercontrol.models import Notable
    from mastercontrol.models import OutletDevice
    from mastercontrol.models import OutletGroup
    log.debug(pformat(db.__dict__, indent=4))
    log.debug(pformat(dir(db), indent=4))
    # log.debug(app.config.SQLALCHEMY_DATABASE_URI.__dict__)
    # sesh = db_session(app.config['SQLALCHEMY_DATABASE_URI'])
    with db_session(app.config['SQLALCHEMY_DATABASE_URI']) as sesh:
        # BaseModel.metadata.create_all(bind=sesh.connection())
        Notable.metadata.create_all(bind=sesh.connection())
        OutletDevice.metadata.create_all(bind=sesh.connection())
        OutletGroup.metadata.create_all(bind=sesh.connection())

@manager.command
def dbredo():
    # from mastercontrol.basemodel import BaseModel
    from mastercontrol.models import Notable
    from mastercontrol.models import OutletDevice
    from mastercontrol.models import OutletGroup
    log.debug(pformat(db.__dict__, indent=4))
    log.debug(pformat(dir(db), indent=4))
    # log.debug(app.config.SQLALCHEMY_DATABASE_URI.__dict__)
    # sesh = db_session(app.config['SQLALCHEMY_DATABASE_URI'])
    with db_session(app.config['SQLALCHEMY_DATABASE_URI']) as sesh:
        # BaseModel.metadata.drop_all(bind=sesh.connection())
        Notable.metadata.drop_all(bind=sesh.connection())
        OutletDevice.metadata.drop_all(bind=sesh.connection())
        OutletGroup.metadata.drop_all(bind=sesh.connection())
        # BaseModel.metadata.create_all(bind=sesh.connection())
        Notable.metadata.create_all(bind=sesh.connection())
        OutletDevice.metadata.create_all(bind=sesh.connection())
        OutletGroup.metadata.create_all(bind=sesh.connection())





@manager.command
def quick(port=port):
    # Mount the application
    cherrypy.tree.graft(app, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = host
    server.socket_port = int(port)
    server.thread_pool = 30

    # For SSL Support
    # server.ssl_module            = 'pyopenssl'
    # server.ssl_certificate       = 'ssl/certificate.crt'
    # server.ssl_private_key       = 'ssl/private.key'
    # server.ssl_certificate_chain = 'ssl/bundle.crt'

    # Subscribe this server
    server.subscribe()

    # Example for a 2nd server (same steps as above):
    # Remember to use a different port

    # server2             = cherrypy._cpserver.Server()

    # server2.socket_host = "0.0.0.0"
    # server2.socket_port = 8081
    # server2.thread_pool = 30
    # server2.subscribe()

    # Start the server engine (Option 1 *and* 2)

    try:
        cherrypy.engine.start()
        cherrypy.engine.block()
    except KeyboardInterrupt:
        cherrypy.engine.stop()


@manager.command
def go():
    app.run(debug=True, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    manager.run()
