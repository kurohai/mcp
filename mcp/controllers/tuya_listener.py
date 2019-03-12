#!/usr/bin/env python


import inspect
import os
import socket
import sys
import time

from flask import current_app

print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

from mcp.logutil import get_logger
from mcp.logutil import logging
from mcp.utilities import json
from mcp.utilities import logpp
from munch import *
from pprint import pprint

print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

from mcp import app_name
from mcp import appdir
# from mcp.controllers import db
from mcp import Session
from mcp.models import TuyaScan
print('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

#from sqlalchemy import SQLAlchemy

#db = SQLAlchemy()


log = get_logger(__name__)
log.setLevel(logging.DEBUG)


# def init_db():
#     from mcp import Base
#     Base.metadata.create_all()
#     db.create_all()
#     sesh.create_all()

def get_existing_data(data):
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

    sesh = Session()
    t = sesh.query(TuyaScan).filter(TuyaScan.gwId == data.gwId).all()
    # pprint(t)
    if t is not None:
        if len(t) > 0:
            return t[0]
        else:
            return TuyaScan()

def main():
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

    # if not os.path.isfile(os.path.join(appdir, 'tuya-device.db')):
    #     init_db()
    log.info('starting port scan')
    # packets = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    port = 6666

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    counter = int()
    while True:
        sesh = Session()
        log.info('scan again...')
        data, addr = sock.recvfrom(port)
        ip, src_port = addr

        if data:
            d = Munch(json.loads(data[20:163]))
            log.info('ip: {0}  port: {1}'.format(addr[0], addr[1]))
            # log.info(data[20:163])

            device = get_existing_data(d)
            # if device:

            log.info(
                'device n db! ip: {device.ip}\tgwId: {device.gwId}'.format(
                    device=device,
                )
            )

            # device = TuyaScan()
            device.ip = ip
            device.gwId = d.gwId
            device.active = d.active
            device.ability = d.ability
            device.mode = d.mode
            device.encrypt = d.encrypt
            device.productKey = d.productKey
            device.version = d.version
            # device.get_dev_type()
            # print('\n\n\n\n\n\n\n')
            # log.info(sesh.new)
            # log.info(sesh.new)
            # log.info(sesh.dirty)
            # print('\n\n\n\n\n\n\n')
            log.info('updating record')

            # if not device in sesh.new:
            sesh.merge(device)
            # else:
            try:
                sesh.commit()
            except Exception as e:
                sesh.merge(device)
                sesh.commit()
                log.error('error in commit')
                log.error(e)
                # sesh.rollback()
            finally:
                sesh.close()

        counter += 1
        if counter == 19:
            log.info('sleeping a few secs...')
            for i in xrange(5):
                time.sleep(1)
                log.info(i)
            counter = 0
        elif counter > 19:
            counter = 0

if __name__ == '__main__':
    main()
