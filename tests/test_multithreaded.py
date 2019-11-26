"""
    Tests to perform reads/writes to the database concurrently i.e.
    from multiple threads.
"""

import logging
import os
from threading import Thread
import json
import sys

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

    def __init__(self, data_range, database=None):
        """ Instance Initialization """

        super(PupDBWriterThread, self).__init__()
        self.data_range = data_range
        if database is None:
            self.database = PupDB(TEST_DB_PATH)
        else:
            self.database = database

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


def test_mt_get_and_set_mi():
    """
        Tests the get() and set() methods of PupDB,
        in a multi-threaded scenario, where each thread has it's own
        instance (object) of PupDB.
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


def test_mt_get_and_set_si():
    """
        Tests the get() and set() methods of PupDB,
        in a multi-threaded scenario, where all threads share a
        single instance (object) of PupDB.

        PupDB currently does not support multiple threads using the same
        PupDB instance, so the database file will get corrupted due to
        race condition.

        If you want to use PupDB with multiple threads, maintain separate
        PupDB instance for each thread.
    """

    if sys.version_info[0] < 3:
        error_cls = ValueError
    else:
        error_cls = json.decoder.JSONDecodeError

    with pytest.raises(error_cls):
        data_ranges = [
            range(1, 50),
            range(50, 100),
            range(100, 150),
            range(150, 201)
        ]
        writers = []
        database = PupDB(TEST_DB_PATH)

        # Write from multiple threads.
        for data_range in data_ranges:
            writer = PupDBWriterThread(data_range, database)
            writers.append(writer)
            writer.start()

        for writer in writers:
            writer.join()

        # Verify if all keys have been written properly.
        assert len(database) == 200
