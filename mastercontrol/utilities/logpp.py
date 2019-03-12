#!/usr/bin/env python


from pprint import pformat
from ..logutil import get_logger

log = get_logger(__name__)


def logpp(data):
    log.debug('format message sent to logpp and make it pretty')
    return pformat(data, indent=4)
