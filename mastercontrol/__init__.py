#!/usr/bin/env python


app_name = __name__

import inspect
import os

from config import config
from config import json
from flask import Flask
from flask import redirect
from flask import request
from flask_admin import Admin
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from flask_moment import Moment
from flask_restplus_patched.swagger import Swagger
from flask_sqlalchemy import SQLAlchemy
from logutil import get_logger
from munch import Munch
from pprint import pformat
from pprint import pprint


log = get_logger(__name__)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
moment = Moment()


log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
    i=inspect.currentframe(),
    p=os.path.realpath(__file__),
    n=__name__)
)


def create_app(config_name):
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
        i=inspect.currentframe(),
        p=os.path.realpath(__file__),
        n=__name__)
    )
    app = Flask(__name__)

    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
        i=inspect.currentframe(),
        p=os.path.realpath(__file__),
        n=__name__)
    )

    # do configuration from config.py object
    app.config.from_object(config[config_name])

    # config[config_name].init_app(app)
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
        i=inspect.currentframe(),
        p=os.path.realpath(__file__),
        n=__name__)
    )
    # log.debug(config[config_name].__dict__)
    # log.debug(config[config_name]())
    # pprint(app.__dict__)

    # db init
    db.init_app(app)
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
        i=inspect.currentframe(),
        p=os.path.realpath(__file__),
        n=__name__)
    )
    # pprint(json.dumps(app.config, indent=4))
    # pprint(Munch(app.config).toDict())



    migrate.init_app(app, db)
    login.init_app(app)




    """
    Move this to utils or app file

    """
    def _check_path(url):
        if not url.endswith('/') and not url.endswith('.json'):
            return True
        else:
            return False

    @app.before_request
    def add_trailing():
        rp = request.path

        log.info('pre-path: {0}'.format(rp))
        log.info('method: {0}'.format(request.method))
        log.info('post-path: {0}'.format(str(request.path)))
        if _check_path(rp):
            return redirect(rp + '/')

    # do blueprint registrations
    # maybe some flask_restplus.Api config
    from .api import main as main_blueprint
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
        i=inspect.currentframe(),
        p=os.path.realpath(__file__),
        n=__name__)
    )

    from .api import api_v1
    from .basemodel import BaseModel
    from .models import Notable
    from .models import OutletDevice
    from .models import OutletGroup
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
        i=inspect.currentframe(),
        p=os.path.realpath(__file__),
        n=__name__)
    )

    app.register_blueprint(main_blueprint)
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
        i=inspect.currentframe(),
        p=os.path.realpath(__file__),
        n=__name__)
    )

    # api_v1.init_app(app)
    api_v1.add_model('notable', Notable)
    api_v1.add_model('notable', OutletDevice)
    api_v1.add_model('notable', OutletGroup)
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(
        i=inspect.currentframe(),
        p=os.path.realpath(__file__),
        n=__name__)
    )

    log.debug(pformat(app.__dict__, indent=4))
    swag = Swagger(api_v1)

    log.debug(pformat(app.__dict__, indent=4))
    log.debug(pformat(api_v1.__dict__, indent=4))

    log.debug(pformat(api_v1.blueprint, indent=4))
    # log.debug(pformat(api_v1.__schema__, indent=4))
    log.debug(pformat(api_v1.app.__dict__, indent=4))
    # log.debug(pformat(api_v1.specs_url, indent=4))

    log.debug(pformat(app.extensions['sqlalchemy'].__dict__, indent=4))
    # log.debug(pformat(config[config_name](), indent=4))


    return app
