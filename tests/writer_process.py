""" Script to write specified range of keys to DB. """

import os
import sys
import logging

from pupdb.core import PupDB

from test_multiprocess import TEST_DB_PATH

logging.basicConfig(
    level=logging.INFO,
    format='%(process)d | %(levelname)s | %(message)s'
)


def write_to_db(data_range):
    """ Method performs write to the database."""

    database = PupDB(TEST_DB_PATH)

    for i in data_range:
        database.set(i, i)

    logging.info(
        'Process %s wrote range(%s, %s) to DB successfully.',
        os.getpid(), data_range.start, data_range.stop
    )


if __name__ == '__main__':
    write_to_db(range(int(sys.argv[1]), int(sys.argv[2])))
