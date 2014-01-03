#!/usr/bin/env python

from setuptools import setup, find_packages

import os
execfile(os.path.join('swiftype', 'version.py'))

setup(
    name = 'swiftype',
    version = VERSION,
    description = 'Swiftype API Client for Python',
    author = 'Swiftype',
    author_email = 'team@swiftype.com',
    url = 'https://swiftype.com/',
    packages = find_packages(),
    install_requires = ["anyjson"],
    test_suite='nose.collector',
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
