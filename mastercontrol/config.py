#!/usr/bin/env python2.7


try:
    import simplejson as json
except ImportError:
    import json
import logging
import os
from munch import Munch
from logutil import get_logger
from flask_config import FlaskBaseConfig


log = get_logger(__name__)


class BaseConfig(FlaskBaseConfig):
    """docstring for BaseConfig"""

    def __init__(self, *args, **kwargs):
        super(BaseConfig, self).__init__(*args, **kwargs)
        self.loglevel = logging.INFO
        self.debug = False
        self.verbose = False

        # conf files and paths
        self.pwd = os.path.abspath(
            os.path.dirname(os.path.realpath(__file__))
        )
        self.flask_port = '9008'


        self.conf_dir = 'conf.d'
        self.api_token_path = 'secrets'
        self.creds_path = 'secure'
        self.tuya_device_default_values_file = 'tuya-devices-default-info.json'
        self.data_dir = 'data'

        self.api_token_file_prefix = 'host-'

        self.creds_file = 'credentials.json'
        self.hosts_file = 'host-list.json'
        self.hosts_file_test = 'host-list-testing.json'

        self.write_to_disk = False
        # self.load_credentials()

    @property
    def tuya_default_data(self):

        return Munch(
            json.load(
                open(
                    os.path.join(
                        self.pwd,
                        self.conf_dir,
                        self.tuya_device_default_values_file,
                    )
                )
            )
        )

    def load_credentials(self):
        with open(self.get_creds_path()) as f:
            obj = Munch(json.loads(f.read()))
            self.username = obj.username
            self.password = obj.password

    def get_token_path(self, addr):
        return os.path.join(
            self.api_token_path,
            self.api_token_file_prefix + addr + '.json'
        )

    @property
    def data_prefix(self):
        return '{.current_metric}-stats'.format(self)

    def get_data_dir(self, metric_name):
        return os.path.join(
            self.data_prefix, '{.data_prefix}-{mn}.json'.format(
                self, mn=metric_name)
        )

    @property
    def get_conf_dir(self):
        return os.path.join(
            self.pwd,
            self.conf_dir,
            # '{.data_prefix}-{mn}.json'.format(
            #     self, mn=metric_name
            # )
        )

    def get_data_dir(self):
        return os.path.join(
            self.pwd,
            self.data_dir,
        )

    def get_creds_path(self):
        return os.path.join(
            self.pwd,
            self.creds_path,
            self.creds_file,
        )


class DevelopmentConfig(BaseConfig):
    """docstring for DevelopmentConfig"""

    def __init__(self, *args, **kwargs):
        super(DevelopmentConfig, self).__init__(*args, **kwargs)
        self.loglevel = logging.DEBUG
        self.write_to_disk = True
        self.hosts_file = 'host-list.json'


class TestingConfig(BaseConfig):
    """docstring for TestingConfig"""

    def __init__(self, *args, **kwargs):
        super(TestingConfig, self).__init__(*args, **kwargs)
        self.loglevel = logging.INFO
        self.write_to_disk = False


class ProductionConfig(BaseConfig):
    """docstring for ProductionConfig"""

    def __init__(self, *args, **kwargs):
        super(ProductionConfig, self).__init__(*args, **kwargs)
        self.loglevel = logging.WARN
        self.write_to_disk = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
