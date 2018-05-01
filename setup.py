#!/usr/bin/env python

from setuptools import setup, find_packages

from swiftype.version import VERSION

setup(
    name = 'swiftype',
    version = VERSION,
    description = 'Swiftype API Client for Python',
    author = 'Swiftype',
    author_email = 'team@swiftype.com',
    url = 'https://swiftype.com/',
    packages = find_packages(),
    install_requires = ["anyjson", "six"],
    test_suite='nose.collector',
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
