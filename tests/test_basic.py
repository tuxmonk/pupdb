"""
    Basic tests for the PupDB database.
"""

import os
import json

import pytest

from pupdb.core import PupDB

TEST_DB_PATH = 'testdb.json'
TEST_DB_LOCK_PATH = '{}.lock'.format(TEST_DB_PATH)


@pytest.fixture(autouse=True)
def run_around_tests():
    """ Function is invoked around each test run. """

    print('Test started.')
    yield
    print('Test ended.')

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
