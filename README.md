<img src="https://raw.githubusercontent.com/tuxmonk/pupdb/master/logo.png" alt="PupDB Logo" width="400"/>

[![Build Status](https://travis-ci.org/tuxmonk/pupdb.svg?branch=master)](https://travis-ci.org/tuxmonk/pupdb) [![codecov](https://codecov.io/gh/tuxmonk/pupdb/branch/master/graph/badge.svg)](https://codecov.io/gh/tuxmonk/pupdb) [![PyPI version fury.io](https://badge.fury.io/py/pupdb.svg)](https://pypi.python.org/pypi/pupdb/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/pupdb.svg)](https://pypi.python.org/pypi/pupdb/)

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
7. `dumps()`: Returns a `json` dump of the entire database file sorted by key.
8. `truncate_db()`: Removes all data from the database file i.e. truncates the database file.

## Using the PupDB HTTP/REST Interface

**Using the HTTP/REST Interface, all PupDB-related operations can be performed without using PupDB as a Python package. As a result, PupDB can be used in any programming language that can make HTTP requests.**

To start PupDB's `gunicorn`-based `flask` server:

```python
from pupdb.server import start_http_server

# Start the gunicorn server (with 4 worker threads).
start_http_server()
```

The server will listen to local port 4000. The server will be available at `http://localhost:4000`.

### HTTP API Endpoints

1. `/get?key=<key-goes-here>` (Method: `GET`): This API endpoint is an interface to PupDB's `get()` method. e.g.:

```bash
curl -XGET http://localhost:4000/get?key=test
```

The above `curl` request will fetch the result for key `test`.

2. `/set` (Method: `POST`): This API endpoint is an interface to PupDB's `set()` method. e.g.:

```bash
curl -XPOST http://localhost:4000/set -H 'Content-Type: application/json' -d '{"key": "test", "value": "1234"}'
```

The above `curl` request will set the value `1234` to key `test` in the database.

3. `/remove/<key-goes-here>` (Method: `DELETE`): This API endpoint is an interface to PupDB's `remove()` method. e.g.:

```bash
curl -XDELETE http://localhost:4000/remove/test
```

The above `curl` request will remove the key `test` in the database. It returns a `404 Not Found` if the key does not exist in the database.

4. `/keys` (Method: `GET`): This API endpoint is an interface to PupDB's `keys()` method. e.g.:

```bash
curl -XGET http://localhost:4000/keys
```

The above `curl` request will return a payload containing the `list` of keys in the database.

5. `/values` (Method: `GET`): This API endpoint is an interface to PupDB's `values()` method. e.g.:

```bash
curl -XGET http://localhost:4000/values
```

The above `curl` request will return a payload containing the `list` of values of all keys in the database.

6. `/items` (Method: `GET`): This API endpoint is an interface to PupDB's `items()` method. e.g.:

```bash
curl -XGET http://localhost:4000/items
```

The above `curl` request will return a payload containing the `list` of `[key, value]` pairs in the database.

7. `/dumps` (Method: `GET`): This API endpoint is an interface to PupDB's `dumps()` method. e.g.:

```bash
curl -XGET http://localhost:4000/dumps
```

The above `curl` request will return a payload containing the string dump of the entire database.

7. `/truncate-db` (Method: `POST`): This API endpoint is an interface to PupDB's `truncate_db()` method. e.g.:

```bash
curl -XPOST http://localhost:4000/truncate-db
```

The above `curl` request will truncate i.e. remove all key-value pairs from the database.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the
[tags on this repository](https://github.com/tuxmonk/pupdb/tags).

## License

This project is licensed under the MIT License - see the
[LICENSE.txt](https://github.com/tuxmonk/pupdb/blob/master/LICENSE.txt) file for more details.
