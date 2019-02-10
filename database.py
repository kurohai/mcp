#!/usr/bin/env python



import inspect
import os
import sys

from mcp import Base
from mcp import Session
from mcp import TuyaBase
from mcp.logutil import get_logger

# from mcp import SQLALCHEMY_BINDS
# from mcp import engine_mcp
# from mcp import engine_tuya
# from mcp.utilities.sesh import db_connection
# from mcp.utilities.sesh import db_session


log = get_logger(__name__)



def initdb():
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))

    sesh = Session(bind=Base)
    Base.metadata.create_all(bind=sesh.get_bind())
    sesh = Session(bind=TuyaBase)
    TuyaBase.metadata.create_all(bind=sesh.get_bind())
    log.info('tables created')


def deldb():
    log.debug('here inspecting:\n\t{p}\n\t{n}\n\t{i.f_lineno}'.format(i=inspect.currentframe(),p=os.path.realpath(__file__),n=__name__))
    try:

        sesh = Session(bind=Base)
        Base.metadata.drop_all(bind=sesh.get_bind())
        sesh = Session(bind=TuyaBase)
        TuyaBase.metadata.drop_all(bind=sesh.get_bind())
        log.info('tables deleted')

    except Exception as e:
        log.error(e)



if __name__ == '__main__':
    deldb()
    initdb()
