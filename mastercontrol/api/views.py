#!/usr/bin/env python


from . import ns
from .. import db
from ..logutil import get_logger
from ..models import Notable
from ..models import NotableSchema
from ..utilities import *
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_restplus_patched import Resource
from munch import Munch
from munch import munchify
from munch import unmunchify
from pprint import pformat
from pprint import pprint


log = get_logger(__name__)


@ns.route('/')
@ns.doc(description='Do the damn note thing.')
class NotableListAPI(Resource):
    """docstring for NotableAPI"""

    # @ns.response(200)
    @ns.response(NotableSchema(many=True))
    def get(self):
        results = munchify(Notable.query.all())
        return [r for r in results]


@ns.route('/<string:name>/')
@ns.doc(description='Do the damn note thing.')
class NotableAPI(Resource):
    """docstring for NotableAPI"""

    @ns.response(NotableSchema())
    def get(self, name):
        results = Notable.query.filter(Notable.name == name).first()
        return results


@ns.route('/add/')
@ns.doc(description='Do the damn add note thing.')
class NotableAddAPI(Resource):
    """docstring for NotableAddAPI"""

    def put(self):
        content = request.get_json()
        # log.debug(logpp(content.__dict__))
        log.debug(logpp(content['name']))
        log.debug(pformat(content['name'], indent=4))
        log.info(pformat(ns.payload, indent=4))
        note = Notable()
        note.name = content['name']
        db.session.add(note)
        db.session.commit()
        return note.to_json()
