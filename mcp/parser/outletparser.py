#!/usr/bin/env python


from flask_restplus.reqparse import RequestParser
from mcp.logutil import get_logger
from munch import Munch
from munch import munchify
from munch import unmunchify
from pprint import pprint

log = get_logger(__name__)

parser_base = Munch()
parser_base.name = ''
parser_base.type = str
parser_base.required = True
parser_base.help = 'Data'
parser_base.location = 'form'


parser_name = parser_base.copy()
parser_name.name = 'name'
parser_name.help = 'The device name'

parser_dev_id = parser_base.copy()
parser_dev_id.name = 'dev_id'

parser_address = parser_base.copy()
parser_address.name = 'address'

parser_local_key = parser_base.copy()
parser_local_key.name = 'local_key'

parser_group = parser_base.copy()
parser_group.name = 'group'
parser_group.required = False

# for k, v in parser_dev_id.items():
#     if isinstance(v, threading.Thread):
#         parser_dev_id.pop(k)
# parser = api.parser()
parser = RequestParser()
# parser.add_argument(**parser_name.toDict())
# parser.add_argument(**parser_dev_id.toDict())
parser.add_argument(
    name=parser_dev_id.name,
    type=parser_dev_id.type,
    required=parser_dev_id.required,
    help=parser_dev_id.help,
    location=parser_dev_id.location,
)
# parser.add_argument(**parser_address.toDict())
# parser.add_argument(**parser_group.toDict())
# parser.add_argument(**parser_local_key.toDict())

pprint(parser.__dict__)
log.debug('parser args:')
for a in parser.args:
    log.debug('name: {0}\ttype: {1}'.format(a.name, a.type))
