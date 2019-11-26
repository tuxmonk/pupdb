<img src="logo.png" alt="PupDB Logo" width="400"/>

[![Build Status](https://travis-ci.org/tuxmonk/pupdb.svg?branch=master)](https://travis-ci.org/tuxmonk/pupdb) [![codecov](https://codecov.io/gh/tuxmonk/pupdb/branch/master/graph/badge.svg)](https://codecov.io/gh/tuxmonk/pupdb)

## What is it?

PupDB is an ernest attempt to create a simple file-based key-value database written in Python.

## Why PupDB?

The objective behind the creation of PupDB is to create a database system which performs simple persistence operations well and data can be accessed with a minimalist, easy-to-use API with least configuration.

### PupDB is the best choice when:

1. You need a simple NoSQL data store with an interface as simple as a Python `dict`, and want to start storing and retrieving data within a few minutes.
2. You want to create an application without bothering much about configuration and setup for storing data.
3. Your database is not very huge i.e. not greater than a few megabytes of data.

### When not to use PupDB:

1. You want to perform advanced queries on your data.
2. Your database is larger than a few megabytes of data.
3. You want a database software that supports advanced capabilities like indexing, partitioning etc.

## Salient Features

1. **Multi-processing support**: Same database file can be used across multiple processes concurrently.
2. **Mult-threading support**: Same database file (with separate `PupDB` instance per thread) can be used concurrently.
3. **REST-based HTTP Interface**: Apart from using it as a `python` package, you can also use PupDB via a `flask`-based HTTP interface. This way you can use PupDB with programming languages other than Python.

## Installation

PupDB can be installed using `pip`:

```bash
pip install pupdb
```

## Basic API Documentation and Usage

1. `set(key, value)`: Stores the `value` mapped to `key` in the database file.
2. `get(key)`: Returns the `value` mapped to `key` in the database file. Returns `None` if `key` is not found.
3. `remove(key)`: Removes the `key` from the database file. Raises a `KeyError` if `key` is not found in the database file.
4. `keys()`: Returns the keys present in the database file. Return type is `list` in Python 2 and [Dictionary view object](https://docs.python.org/3.8/library/stdtypes.html?highlight=keys#dict-views) (similar to [`dict.keys()`](https://docs.python.org/3.8/library/stdtypes.html?highlight=keys#dict.keys)) in Python 3.
5. `values()`: Returns the values of all keys present in the database file. Return type is `list` for Python 2 and [Dictionary view object](https://docs.python.org/3.8/library/stdtypes.html?highlight=keys#dict-views) (similar to [`dict.values()`](https://docs.python.org/3.8/library/stdtypes.html?highlight=keys#dict.values)) in Python 3.
6. `items()`: Returns the values of all keys present in the database file. Return type is `list` for Python 2 and [Dictionary view object](https://docs.python.org/3.8/library/stdtypes.html?highlight=keys#dict-views) (similar to [`dict.items()`](https://docs.python.org/3.8/library/stdtypes.html?highlight=keys#dict.items)) in Python 3.
7. `dumps()`: Returns a `json` dump of the entire database file.
8. `truncate_db()`: Removes all data from the database file i.e. truncates the database file.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the
[tags on this repository](https://github.com/tuxmonk/pupdb/tags).

## License

This project is licensed under the MIT License - see the
[LICENSE.txt](LICENSE.txt) file for more details.
