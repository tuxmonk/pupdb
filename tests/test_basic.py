"""
    Basic tests for the PupDB database.
"""

import logging
import os
import json

import pytest

from pupdb.core import PupDB

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(process)d | %(levelname)s | %(message)s'
)


TEST_DB_PATH = 'testdb.json'
TEST_DB_LOCK_PATH = '{}.lock'.format(TEST_DB_PATH)


@pytest.fixture(autouse=True)
def run_around_tests():
    """ Function is invoked around each test run. """

    logging.debug('Test started.')
    yield
    logging.debug('Test ended.')

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    if os.path.exists(TEST_DB_LOCK_PATH):
        os.remove(TEST_DB_LOCK_PATH)


def test_get_and_set():
    """ Tests the get() and set() methods of PupDB. """

    database = PupDB(TEST_DB_PATH)
    key, val = 'test_key', list(range(100))
    database.set(key, val)

    assert database.get(key) == val


def test_remove():
    """ Tests the remove() method of PupDB. """

    database = PupDB(TEST_DB_PATH)
    for i in range(10):
        database.set(i, i)

    # Removing key 0 from the database.
    database.remove(0)

    for i in range(10):
        if i == 0:
            assert database.get(i) is None
        else:
            assert database.get(i) is not None

    # Check the behavaiour for a non-existent key.
    with pytest.raises(KeyError):
        database.remove(1000)


def test_keys():
    """ Tests the keys() method of PupDB. """

    database = PupDB(TEST_DB_PATH)
    range_list = [str(i) for i in range(10)]
    for i in range_list:
        database.set(i, i)

    db_keys_list = list(database.keys())

    assert db_keys_list == range_list


def test_values():
    """ Tests the values() method of PupDB. """

    database = PupDB(TEST_DB_PATH)
    range_list = list(range(10))
    for i in range_list:
        database.set(i, i)

    db_values_list = list(database.values())

    assert db_values_list == range_list


def test_items():
    """ Tests the items() method of PupDB. """

    database = PupDB(TEST_DB_PATH)
    range_list = list(range(10))
    for i in range_list:
        database.set(i, i)

    items_list = [(str(i), i) for i in range_list]
    db_values_list = list(database.items())

    assert db_values_list == items_list


def test_dumps():
    """ Tests the dumps() method of PupDB. """

    database = PupDB(TEST_DB_PATH)
    range_list = list(range(10))
    for i in range_list:
        database.set(i, i)

    db_dict = {str(i): i for i in range_list}

    assert database.dumps() == json.dumps(db_dict)


def test_truncate_db():
    """ Tests the truncate_db() method of PupDB. """

    database = PupDB(TEST_DB_PATH)
    range_list = list(range(10))
    for i in range_list:
        database.set(i, i)

    db_dict = {str(i): i for i in range_list}
    assert database.dumps() == json.dumps(db_dict)

    database.truncate_db()

    assert database.dumps() == json.dumps({})


def test_length():
    """
        Tests whether len() on the PupDB instance returns it's proper length. 
    """

    database = PupDB(TEST_DB_PATH)
    num_items = 100
    range_list = list(range(num_items))
    for i in range_list:
        database.set(i, i)
    assert len(database) == 100


def test_get_database():
    """
        Tests whether _get_database() returns the dict for the DB.
    """

    database = PupDB(TEST_DB_PATH)
    num_items = 100
    range_list = list(range(num_items))
    for i in range_list:
        database.set(i, i)

    # pylint: disable=protected-access
    db_dict = database._get_database()
    assert json.dumps({str(i): i for i in range_list}) == json.dumps(db_dict)


def test_flush_database():
    """
        Tests whether _flush_database() writes to DB.
    """

    database = PupDB(TEST_DB_PATH)
    num_items = 100
    range_list = list(range(num_items))
    data_dict = {str(i): i for i in range_list}

    # pylint: disable=protected-access
    database._flush_database(data_dict)
    db_dict = database._get_database()

    assert json.dumps(data_dict) == json.dumps(db_dict)
