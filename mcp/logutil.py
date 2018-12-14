import logging
import os
import sys
from mcp import app_name
from logging.handlers import TimedRotatingFileHandler

pwd = os.path.dirname(os.path.realpath(__file__))

FORMATTER = logging.Formatter(
    '%(asctime)s  %(name)s  %(levelname)s  %(funcName)s:%(lineno)d  %(message)s'
)
LOG_DIR = os.path.join(pwd, 'log')
LOG_FILE = os.path.join(LOG_DIR, 'xiv-client-metrics.log')
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)


def get_file_name(metric_name):
    return '{d}/{p}-{f}.log'.format(
        d=LOG_DIR,
        p=app_name,
        f=metric_name,
    )


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(metric_name):
    file_handler = TimedRotatingFileHandler(
        get_file_name(metric_name), when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, metric_name='default'):
    logger = logging.getLogger(logger_name)

    # better to have too much log than not enough
    logger.setLevel(logging.DEBUG)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(metric_name))

    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False

    return logger
