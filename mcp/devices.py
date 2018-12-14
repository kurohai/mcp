#!/usr/bin/env python


import logging
import nmap
import os
import simplejson
import sys

from logutil import get_logger
from munch import Munch
from munch import munchify
from munch import unmunchify
from nmap import PortScanner
from nmap import PortScannerAsync
from pprint import pprint
from time import sleep
from cachy import CacheManager

logging.basicConfig(level=logging.DEBUG)
log = get_logger(__name__, 'netscan')
# log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.getLogger('pytuya').setLevel(logging.DEBUG)
logging.getLogger('nmap').setLevel(logging.DEBUG)

appdir = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.dirname(appdir)
log.info('appdir: {0}'.format(appdir))
log.info('pwd: {0}'.format(pwd))

config_path = os.path.join(pwd, 'conf.d')
data_path = os.path.join(pwd, 'data')
scan_results = os.path.join(data_path, 'scan-results.json')
cache_dir = os.path.join(pwd, '.cache')

def mkdir_if_nodir(dirpath):
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)

mkdir_if_nodir(cache_dir)
mkdir_if_nodir(config_path)
mkdir_if_nodir(data_path)

cachy_conf = Munch()
cachy_conf.default = 'file'
cachy_conf.serializer = 'json'
cachy_conf.stores = Munch()
cachy_conf.stores.file = Munch()
cachy_conf.stores.file.driver = 'file'
cachy_conf.stores.file.path = cache_dir

cache = CacheManager(cachy_conf)

global device_list
global netdevices
netdevices = Munch()



def prep_device_list(conf_file_path):
    global device_list
    device_list = munchify(simplejson.load(open(conf_file_path, 'r')))
    # log.debug(muncherator(device_list))
    for k, v in device_list.items():
        v.mac = parse_mac_from_id(v.dev_id)
        device_list[k] = v
    return device_list



def parse_mac_from_id(device_id):
    s = device_id[-12:]
    mac = str()
    for i in xrange(0, 12, 2):
        mac += ':' + s[i:i + 2]
    return mac[1:]



def muncherator(obj):
    return simplejson.dumps(
        unmunchify(obj),
        indent=4,
    )


@cache
def check_mac(macaddr, address):
    global device_list
    log.debug('testing mac: {0}'.format(macaddr))
    log.debug('address ip: {0}'.format(address))
    for k, v in device_list.items():
        if v.mac.lower() == macaddr.lower():
            v.address = address
            return k, v
            # cache.forever(k, v)
            log.debug('found address for ' + muncherator(k) + ' as ' + address)
            log.debug(muncherator(v))
        device_list[k] = v


def write_data(data):
    with open(scan_results, 'ab') as f:
        f.write(simplejson.dumps(data, indent=4))


def scan_callback(host, data):
    global device_list
    log.info('found: {0}'.format(host))
    data = munchify(data)

    if data.nmap.scanstats.uphosts:
        log.info('writing data for: {0}'.format(host))
        # write_data(data)
        for scan in data.scan:
            if not str(host) in str(scan):
                log.warn('str(host) not in in str(scan)')
            else:
                if 'mac' in data.scan[str(host)].addresses:
                    macaddr = data.scan[host].addresses.mac
                    write_data(data)
                    check_mac(macaddr, host)
                else:
                    macaddr = 'nomac'
                print 'Results:', host, macaddr
                log.info(
                    'Results: ip={i} mac={m}'.format(
                        i=host,
                        m=macaddr,
                    )
                )
                log.debug(scan)
    # global netdevices
    # netdevices[host] = data
    # print(simplejson.dumps(data.toDict(), indent=4))

    # if host in data.scan.keys():
    #     pprint(data.scan.toDict())

    return data


def main():
    global device_list
    device_conf_file = os.path.join('conf.d', 'devices.json')
    device_list = prep_device_list(device_conf_file)
    log.debug(muncherator(device_list))
    if os.path.isfile(scan_results):
        os.remove(scan_results)

    scanner = PortScannerAsync()
    for i in xrange(30, 100, 10):
        log.debug('scanning: 10.0.0.{0}-{1}'.format(i, i+10))
        scanner.scan(
            hosts='10.0.0.{0}-{1}'.format(i, i+10),
            # hosts='10.0.0.0/25',
            ports='6668',
            arguments='-Pn -n',
            # arguments='-Pn -n --open',
            sudo=True,
            callback=scan_callback
        )
    # scanner.scan(
    #     hosts='10.0.0.66-100',
    #     # hosts='10.0.0.0/25',
    #     ports='6668',
    #     arguments='-Pn -n',
    #     # arguments='-Pn -n --open',
    #     sudo=True,
    #     callback=scan_callback
    # )
    # scanner.scan(
    #     hosts='10.0.0.30-65',
    #     # hosts='10.0.0.0/25',
    #     ports='6668',
    #     arguments='-Pn -n',
    #     # arguments='-Pn -n --open',
    #     sudo=True,
    #     callback=scan_callback
    # )
    i = int()
    # while scanner.still_scanning():
    #     log.info('still scanning {0}'.format(i))
    #     i += 1
    #     sleep(1)
    scanner.wait(timeout=300)
    print(muncherator(device_list))
    sleep(2)
    for key, value in device_list.items():
        device = cache.get(key)
        print muncherator(device)

    # for name, device in device_list.items():


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'scan':
        for i in xrange(5):
            main()
            sleep(3)
    elif cmd == 'rpt':
        device_conf_file = os.path.join('conf.d', 'devices.json')
        device_list = prep_device_list(device_conf_file)
        count = int()
        for key, value in device_list.items():
            device = munchify(cache.get(key))
            if device:
                if not 'null' in device:
                    if device.address == "":
                        cache.forget(key)
                    else:
                        count += 1
                        print muncherator(device)
        log.info('count: ' + str(count))
    elif cmd == 'flush':
        cache.flush()
