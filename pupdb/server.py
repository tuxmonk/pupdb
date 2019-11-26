"""
    Entrypoint module for PupDB's gunicorn-based Flask server.
"""

import os
import subprocess

from pupdb import rest


def start_http_server():
    """ Python wrapper around start_http_server script. """

    dirpath = os.path.dirname(rest.__file__)
    subprocess.call(
        'env PYTHONPATH={} {}/start_http_server'.format(
            dirpath, dirpath), shell=True
    )
