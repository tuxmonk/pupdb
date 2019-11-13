"""
    Tests to perform reads/writes to the database concurrently i.e.
    from multiple threads.
"""

import logging
import os
from threading import Thread

import pytest

from pupdb.core import PupDB

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(process)d | %(levelname)s | %(message)s'
)


TEST_DB_PATH = 'testdb.json'
TEST_DB_LOCK_PATH = '{}.lock'.format(TEST_DB_PATH)


class PupDBWriterThread(Thread):
    """
        This class represents an instance of a thread that writes
        to the database.
    """

    def __init__(self, data_range):
        """ Instance Initialization """

        super(PupDBWriterThread, self).__init__()
        self.data_range = data_range
        self.database = PupDB(TEST_DB_PATH)

    def run(self):
        """ Method performs write to the database."""

        for i in self.data_range:
            self.database.set(i, i)


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


def test_mt_get_and_set():
    """
        Tests the get() and set() methods of PupDB,
        in a multi-threaded scenario.
    """

    data_ranges = [
        range(1, 50),
        range(50, 100),
        range(100, 150),
        range(150, 201)
    ]
    writers = []

    # Write from multiple threads.
    for data_range in data_ranges:
        writer = PupDBWriterThread(data_range)
        writers.append(writer)
        writer.start()

    for writer in writers:
        writer.join()

    # Verify if all keys have been written properly.
    database = PupDB(TEST_DB_PATH)
    assert len(database) == 200
