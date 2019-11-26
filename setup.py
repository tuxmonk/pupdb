"""
    Python canonical setup script.
"""

from os import path
from setuptools import setup

with open(
        path.join(path.abspath(path.dirname(__file__)), 'README.md'),
        encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='pupdb',
    packages=['pupdb'],
    version='0.1.3',
    license='MIT',
    description='A simple file-based key-value database written in Python.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    download_url=(
        'https://github.com/tuxmonk/pupdb/archive/master.zip'
    ),
    url='https://github.com/tuxmonk/pupdb',
    author='tuxmonk',
    author_email='30048080+tuxmonk@users.noreply.github.com',
    keywords=[
        'file-based', 'key-value-store', 'python', 'database', 'rest-api',
        'process-safe', 'cross-language'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True
)
