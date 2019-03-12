    #!/usr/bin/env python


try:
    import simplejson as json
except ImportError:
    import json
import logging
import os
from munch import Munch
from logutil import get_logger
from pprint import pprint


log = get_logger(__name__)


class FlaskBaseConfig(Munch):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get(
        'MAIL_USE_TLS',
        'true'
    ).lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{p}/{a}'.format(p='root:M3rmaidPuss@kurohai.com', a='mastercontrol')

    PROPAGATE_EXCEPTIONS = True
    TESTING = True
    DEBUG = True

    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass

    @classmethod
    def print_conf(cls, app):
        log.debug(munchify(cls))
        pprint(munchify(cls))
        return munchify(cls)[0]



# config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,

#     'default': DevelopmentConfig
# }
