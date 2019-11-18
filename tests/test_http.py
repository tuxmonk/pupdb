"""
    Tests for the HTTP interface to PupDB.
"""

import logging
import os
import json

import pytest

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(process)d | %(levelname)s | %(message)s'
)

TEST_DB_PATH = 'testdb.json'
TEST_DB_LOCK_PATH = '{}.lock'.format(TEST_DB_PATH)


@pytest.fixture()
def test_client():
    """ Fixture function to get the Flask test client. """

    os.environ['PUPDB_FILE_PATH'] = TEST_DB_PATH

    # Lazy import for Lazy Initialization of APP instance.
    # pylint: disable=import-outside-toplevel
    from pupdb.rest import APP, DB

    DB.init_db()

    testing_client = APP.test_client()

    # Establish an application context before running the tests.
    ctx = APP.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    if os.path.exists(TEST_DB_LOCK_PATH):
        os.remove(TEST_DB_LOCK_PATH)


# pylint: disable=redefined-outer-name
def test_db_get_set(test_client):
    """ Test the HTTP db_get() and db_set() interface methods. """

    # Before adding any data
    res = test_client.get('/get?key=test')
    data = res.json
    assert data['value'] is None

    # Adding the data
    res = test_client.post(
        '/set',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'key': 'test', 'value': 'test'})
    )
    assert res.status_code == 200

    # After adding data
    res = test_client.get('/get?key=test')
    data = res.json
    assert data['value'] == 'test'


# pylint: disable=redefined-outer-name
def test_db_remove(test_client):
    """ Test the HTTP db_remove() interface method. """

    # Before adding any data
    res = test_client.delete('/remove/test')
    assert res.status_code == 404

    # Adding the data
    res = test_client.post(
        '/set',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'key': 'test', 'value': 'test'})
    )
    assert res.status_code == 200

    # After adding data
    res = test_client.delete('/remove/test')
    assert res.status_code == 200

    # Try the same request again,
    # this time get a 404 as key is already removed.
    res = test_client.delete('/remove/test')
    assert res.status_code == 404


# pylint: disable=redefined-outer-name
def test_db_keys(test_client):
    """ Test the HTTP db_keys() interface methods. """

    # Before adding any data
    res = test_client.get('/keys')
    data = res.json
    assert data['keys'] == []

    # Adding the data
    for i in range(10):
        res = test_client.post(
            '/set',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'key': 'test{}'.format(i), 'value': 'test'})
        )
        assert res.status_code == 200

    # After adding data
    res = test_client.get('/keys')
    data = res.json
    assert data['keys'] == ['test{}'.format(i) for i in range(10)]


# pylint: disable=redefined-outer-name
def test_db_values(test_client):
    """ Test the HTTP db_values() interface methods. """

    # Before adding any data
    res = test_client.get('/values')
    data = res.json
    assert data['values'] == []

    # Adding the data
    for i in range(10):
        res = test_client.post(
            '/set',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'key': 'test{}'.format(i), 'value': 'test{}'.format(i)
            })
        )
        assert res.status_code == 200

    # After adding data
    res = test_client.get('/values')
    data = res.json
    assert data['values'] == ['test{}'.format(i) for i in range(10)]


# pylint: disable=redefined-outer-name
def test_db_items(test_client):
    """ Test the HTTP db_items() interface methods. """

    # Before adding any data
    res = test_client.get('/items')
    data = res.json
    assert data['items'] == []

    # Adding the data
    for i in range(10):
        res = test_client.post(
            '/set',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'key': 'test{}'.format(i), 'value': 'test{}'.format(i)
            })
        )
        assert res.status_code == 200

    # After adding data
    res = test_client.get('/items')
    data = res.json
    assert data['items'] == [['test{}'.format(i)]*2 for i in range(10)]


# pylint: disable=redefined-outer-name
def test_db_dumbs(test_client):
    """ Test the HTTP db_dumbs() interface methods. """

    # Before adding any data
    res = test_client.get('/dumps')
    data = res.json
    assert data['database'] == {}

    # Adding the data
    for i in range(10):
        res = test_client.post(
            '/set',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'key': 'test{}'.format(i), 'value': 'test{}'.format(i)
            })
        )
        assert res.status_code == 200

    # After adding data
    res = test_client.get('/dumps')
    data = res.json
    assert data['database'] == {
        'test{}'.format(i): 'test{}'.format(i) for i in range(10)
    }


# pylint: disable=redefined-outer-name
def test_db_truncate(test_client):
    """ Test the HTTP db_truncate() interface methods. """

    # Adding the data
    res = test_client.post(
        '/set',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'key': 'test', 'value': 'test'})
    )
    assert res.status_code == 200

    # After adding data
    res = test_client.get('/get?key=test')
    data = res.json
    assert data['value'] == 'test'

    # Call to DB Truncate API
    res = test_client.post('/truncate-db')
    assert res.status_code == 200

    # After truncating the db
    res = test_client.get('/get?key=test')
    data = res.json
    assert data['value'] is None
