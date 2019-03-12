#!/usr/bin/env python


from flask import Blueprint
from flask_restplus_patched import Api
from ..logutil import get_logger


log = get_logger(__name__)


main = Blueprint('api', __name__, url_prefix='/api/v1')

api_v1 = Api(
    main,
    version='1.0',
    title='Notable Events API',
    description='Add those damn notes.',
    default='notable'
)

# ns = api.namespace('notable', description='Add those damn notes.', path='/api/v1')
ns = api_v1.namespace('notable', description='Add those damn notes.')
ns_o = api_v1.namespace('outlets', description='Control those damn outlets.')
api_v1.default = 'notable'
from . import views
from . import views_outlets
