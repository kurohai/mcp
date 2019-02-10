#!/usr/bin/env python


import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print 'time: {0}'.format(time.time() - start)
