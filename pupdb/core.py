"""
    Core module containing entrypoint functions for PupDB.
"""

import os
import json
import traceback

from filelock import FileLock


class PupDB:
    """ This class represents the core of the PupDB database. """

    def __init__(self, db_file_path):
        """ Initializes the PupDB database instance. """

        self.db_lock_file_path = '{}.lock'.format(db_file_path)
        self.db_file_path = db_file_path

        self.db_lock = FileLock(self.db_lock_file_path, timeout=10)
        self.init_db()

    def __repr__(self):
        """ String representation of this class instance. """

        return str(self._get_database())

    def __len__(self):
        """ Function to return the size of iterable. """

        return len(self._get_database())

    def init_db(self):
        """ Initializes the database file. """

        with self.db_lock:
            if not os.path.exists(self.db_file_path):
                with open(self.db_file_path, 'w') as db_file:
                    db_file.write(json.dumps({}))
        return True

    def _get_database(self):
        """ Returns the database json object. """

        with open(self.db_file_path, 'r') as db_file:
            database = json.loads(db_file.read())
            return database

    def set(self, key, val):
        """
            Sets the value to a key in the database.
            Overwrites the value if the key already exists.
        """

        try:
            with self.db_lock, open(self.db_file_path, 'r+') as db_file:
                database = json.loads(db_file.read())
                database[key] = val
                db_file.seek(0)
                db_file.write(json.dumps(database))
                db_file.truncate()
        except Exception:
            print('Error while writing to DB: {}'.format(
                traceback.format_exc()))
            return False
        return True

    def get(self, key):
        """
            Gets the value of a key from the database.
            Returns None if the key is not found in the database.
        """

        key = str(key)
        database = self._get_database()
        return database.get(key, None)

    def remove(self, key):
        """
            Removes a key from the database.
        """

        try:
            key = str(key)
            with self.db_lock, open(self.db_file_path, 'r+') as db_file:
                database = json.loads(db_file.read())
                if key not in database:
                    raise ValueError(
                        'Non-existent Key {} in database'.format(key)
                    )
                del database[key]
                db_file.seek(0)
                db_file.write(json.dumps(database))
                db_file.truncate()
        except Exception:
            print('Error while writing to DB: {}'.format(
                traceback.format_exc()))
            return False
        return True

    def keys(self):
        """
            Returns an iterator of all the keys in the database.
        """

        return self._get_database().keys()

    def values(self):
        """
            Returns an iterator of all the values in the database.
        """

        return self._get_database().values()

    def items(self):
        """
            Returns an iterator of all the items i.e. (key, val) pairs
            in the database.
        """

        return self._get_database().items()

    def dumps(self):
        """ Returns a string dump of the entire database. """

        return json.dumps(self._get_database())

    def truncate_db(self):
        """ Truncates the entire database (makes it empty). """

        with self.db_lock:
            with open(self.db_file_path, 'w') as db_file:
                db_file.write(json.dumps({}))
        return True
