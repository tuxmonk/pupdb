"""
    This module represent the RESTful HTTP interface to PupDB.
"""

import os
import json
import traceback

from flask import Flask, request, Response, jsonify

from pupdb.core import PupDB


# pylint: disable=too-many-ancestors
class CustomResponse(Response):
    """ Custom Response Class for the Flask Application. """

    # pylint: disable=arguments-differ
    @classmethod
    def force_type(cls, rv, environ=None):
        """ Overriden method to jsonify payload. """
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(CustomResponse, cls).force_type(rv, environ)


def init_module():
    """ Initializes the Flask App. """

    app = Flask(__name__)
    app.response_class = CustomResponse
    database = PupDB(os.environ.get('PUPDB_FILE_PATH') or 'pupdb.json')
    return app, database


APP, DB = init_module()


@APP.route('/get', methods=['GET'])
def db_get():
    """ Endpoint Function to interact with PupDB's get() method. """

    key = request.args.get('key')
    if not key:
        return {'error': 'Missing parameter \'key\''}, 400
    return {'key': key, 'value': DB.get(key)}, 200


@APP.route('/set', methods=['POST'])
def db_set():
    """ Endpoint Function to interact with PupDB's set() method. """

    try:
        key = request.json.get('key')
        value = request.json.get('value')
        if not key:
            return {'error': 'Missing parameter \'key\''}, 400
        if not value:
            return {'error': 'Missing parameter \'value\''}, 400

        result = DB.set(key, value)

        if result:
            return {
                'message': 'Key \'{}\' set to Value \'{}\''.format(key, value)
            }, 200
        return {
            'error':
            'There was a problem saving ({}, {}) to the DB.'.format(
                key, value
            )
        }, 400
    except Exception:
        return {'error': 'Unable to process this request.'}, 422


@APP.route('/remove/<key>', methods=['DELETE'])
def db_remove(key):
    """ Endpoint Function to interact with PupDB's remove() method. """

    try:
        if not key:
            return {'error': 'Missing parameter \'key\''}, 400

        try:
            result = DB.remove(key)
        except KeyError as key_err:
            return {'error': str(key_err)[1:-1]}, 404

        if result:
            return {
                'message': 'Key \'{}\' removed from DB.'.format(key)
            }, 200

        return {
            'error':
            'There was a problem removing Key \'{}\' from the DB.'.format(key)
        }, 400
    except Exception:
        return {
            'error':
                'Unable to process this request. Details: %s' %
                traceback.format_exc(),
        }, 422


@APP.route('/keys', methods=['GET'])
def db_keys():
    """ Endpoint Function to interact with PupDB's keys() method. """

    return {'keys': list(DB.keys())}, 200


@APP.route('/values', methods=['GET'])
def db_values():
    """ Endpoint Function to interact with PupDB's values() method. """

    return {'values': list(DB.values())}, 200


@APP.route('/items', methods=['GET'])
def db_items():
    """ Endpoint Function to interact with PupDB's items() method. """

    return {'items': [list(item) for item in DB.items()]}, 200


@APP.route('/dumps', methods=['GET'])
def db_dumps():
    """ Endpoint Function to interact with PupDB's dumps() method. """

    return {'database': json.loads(DB.dumps())}, 200


@APP.route('/truncate-db', methods=['POST'])
def db_truncate():
    """ Endpoint Function to interact with PupDB's truncate_db() method. """

    result = DB.truncate_db()

    if result:
        return {
            'message': 'DB has been truncated successfully.'
        }, 200

    return {
        'error': 'There was a problem truncating the DB.'
    }, 400
