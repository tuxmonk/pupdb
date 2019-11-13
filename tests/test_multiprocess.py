"""
    Tests to perform reads/writes to the database parallely i.e.
    from multiple processes.
"""

import logging
import os
import subprocess

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


def test_mp_get_and_set():
    """
        Tests the get() and set() methods of PupDB,
        in a multi-processing scenario.
    """

    data_ranges = [(0, 100), (100, 200), (200, 300), (300, 400)]

    for data_range in data_ranges:
        proc = subprocess.Popen(
            'python writer_process.py {} {}'.format(*data_range), shell=True)
        proc.wait()

    database = PupDB(TEST_DB_PATH)
    assert len(database) == 400
