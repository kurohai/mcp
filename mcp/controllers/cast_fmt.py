#!/usr/bin/env python


import os, sys, inspect
import simplejson as json
from munch import *
from pprint import pprint


cast_devices = [
{"ip_address": "10.0.0.12", "port": 8009,    "device": { "friendly_name": "Main TV", "model_name": "Chromecast Ultra", "manufacturer": "Google Inc.", "uuid": "e7a91137\-93b2\-b3ee\-a269\-928419d2d235", "cast_type": "cast" } },
{"ip_address": "10.0.0.14", "port": 8009,    "device": { "friendly_name": "Office TV", "model_name": "Chromecast", "manufacturer": "Google Inc.", "uuid": "5be5043b\-a50c\-da4e\-ded6\-5396c7b72bd0", "cast_type": "cast" } },
{"ip_address": "10.0.0.15", "port": 8009,    "device": { "friendly_name": "Bedroom Speaker", "model_name": "Google Home Mini", "manufacturer": "Google Inc.", "uuid": "386cebfe\-c712\-792a\-8712\-765a1e382121", "cast_type": "cast" } },
{"ip_address": "10.0.0.53", "port": 42435,   "device": { "friendly_name": "Office Group", "model_name": "Google Cast Group", "manufacturer": "Google Inc.", "uuid": "6d596165\-c50f\-46eb\-a902\-02c44b9ad434", "cast_type": "group" } },
{"ip_address": "10.0.0.53", "port": 8009,    "device": { "friendly_name": "Office Audio", "model_name": "Chromecast Audio", "manufacturer": "Google Inc.", "uuid": "ec3316e7\-26cc\-0f66\-9981\-e4ee467f213e", "cast_type": "audio" } },
{"ip_address": "10.0.0.54", "port": 8009,    "device": { "friendly_name": "Bedroom TV", "model_name": "Chromecast", "manufacturer": "Google Inc.", "uuid": "3c9c5159\-9ab1\-473a\-52c9\-346a20d21917", "cast_type": "cast" } },
{"ip_address": "10.0.0.61", "port": 42055,   "device": { "friendly_name": "Living Room Group", "model_name": "Google Cast Group", "manufacturer": "Google Inc.", "uuid": "df99063e\-e447\-4d6d\-8689\-6f9e87a021de", "cast_type": "group" } },
{"ip_address": "10.0.0.61", "port": 42162,   "device": { "friendly_name": "Everywhere", "model_name": "Google Cast Group", "manufacturer": "Google Inc.", "uuid": "db168f82\-f398\-4099\-9be3\-adbf090e9753", "cast_type": "group" } },
{"ip_address": "10.0.0.61", "port": 8009,    "device": { "friendly_name": "Main Audio", "model_name": "Chromecast Audio", "manufacturer": "Google Inc.", "uuid": "73fe48e2\-9f2f\-5fe0\-1e1a\-afc5a200412e", "cast_type": "audio" } },
{"ip_address": "10.0.0.73", "port": 8009,    "device": { "friendly_name": "Kitchen display", "model_name": "Google Home Hub", "manufacturer": "Google Inc.", "uuid": "5c73e0db\-540c\-a021\-85b8\-159fed2e67b2", "cast_type": "cast" } },
{"ip_address": "10.0.0.77", "port": 8009,    "device": { "friendly_name": "Office display", "model_name": "Google Home Hub", "manufacturer": "Google Inc.", "uuid": "793bad02\-4ead\-87b2\-6804\-a8fc6e394ea0", "cast_type": "cast" } },
{"ip_address": "10.0.0.78", "port": 8009,    "device": { "friendly_name": "Desk TV", "model_name": "Chromecast", "manufacturer": "Google Inc.", "uuid": "152ce471\-3fc5\-c03f\-6412\-15e9906c3234", "cast_type": "cast" } },
{"ip_address": "10.0.0.79", "port": 8009,    "device": { "friendly_name": "Bathroom display", "model_name": "Google Home Hub", "manufacturer": "Google Inc.", "uuid": "1aac3b50\-63f7\-877d\-6dba\-1cbe4e357ab0", "cast_type": "cast" } },
{"ip_address": "10.0.0.80", "port": 8009,    "device": { "friendly_name": "Living Room display", "model_name": "Google Home Hub", "manufacturer": "Google Inc.", "uuid": "4643265a\-7482\-962d\-9855\-5a3f3d07ee74", "cast_type": "cast" } }
]

if __name__ == "__main__":
    # main( }
    data = munchify(cast_devices)
    pprint(unmunchify(data))

    with open('/mnt/data/code/mcp/data/cast_devices.json', 'wb') as f:
        f.write(json.dumps(unmunchify(data), indent=4) + '\n')


