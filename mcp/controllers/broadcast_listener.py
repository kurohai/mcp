#!/usr/bin/env python


import os
import sys
import select
import socket
from munch import *
from mcp.logutil import get_logger
from mcp.timer import timer
import datetime
from pprint import pprint
try:
    import simplejson as json
except ImportError:
    import json


dt = datetime.datetime.now().isoformat()


log = get_logger(__name__)

log.info('timestamp: {0}'.format(dt))

host = os.environ.get(BIND_ADDR, '0.0.0.0')
port = sys.argv[1]  # where do you expect to get a msg?
bufferSize = 1024 # whatever you need
filepath = os.path.join('/mnt/data/code/mcp/data/', 'tuyas-port-listener-{date}.pcap'.format(date=dt))


log.info('filepath: {0}'.format(filepath))

def write_data(filepath, data):
    log.info('writing data to file!')
    with open(filepath, 'ab') as f:
        f.write(data)


def listener(s):
    # while True:
    log.info('listner gen!')

    result = select.select([s],[],[])
    yield result[0][0].recv(bufferSize)


def enum_buffer(filepath, buffer):
    log.info('writing buffer!')
    for data in buffer:
        write_data(filepath, data)


def parse_packet_data(packet):
    for k, v in enumerate(packet):
        print(k, v)


def mksocket(host, port=6666):
    log.info('creating socket with addr: {0}:{1}'.format(host, port))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    s.setblocking(0)
    return s

def main(port):
    log.info('starting in main()!')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    s.setblocking(0)

    data_buffer = list()
    packet_gen = listener(s)
    packet = packet_gen.next()
    try:
        while True:
            log.info('going around!')
            log.info('packet: {0}'.format(packet))

            for k, v in enumerate(packet):
                if '{' in v:
                    log.info('found open brace: {0}'.format(k))
                    data_start = k
                elif '}' in v:
                    data_end = abs(k)+1
                    log.info('found close brace: {0}'.format(k))
                    log.info('remaining: {0}'.format(k-len(packet)))
            # parse_packet_data(packet[data_start:data_end])
            packet_data = packet[data_start:data_end]
            packet_obj = Munch(json.loads(packet[data_start:data_end]))
            # log.info('json data: {0}'.format(json.dumps(packet)))
            log.info('json dobj: {0}'.format(packet_obj.toDict()))
            data_buffer.append(packet_data)
            log.debug('packet: {0}'.format(packet_data))

            if len(data_buffer) == 10:
                log.info('buffer hit 10!')
                enum_buffer(data_buffer)
                data_buffer = list()
                # for k, data in enumerate(data_buffer):
                #     write_data(filepath, data)
                #     data_buffer.pop()
            packet = packet_gen.next()

    except KeyboardInterrupt as e:
        sys.exit(0)
    except Exception as e:
        # log.error(dir(e))
        # log.error(type(e.args))
        # log.error(dir(e.message))
        log.error(e)
        log.error(e.args)
        log.error(e.message)


if __name__ == '__main__':
    port = int(sys.argv[1])
    main(port)