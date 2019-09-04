#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install

from swiftype.version import VERSION


class PostInstallMessage(install):
    def run(self):
        print("DEPRECATION WARNING: The swiftype package has been deprecated and replaced by elastic-site-search")
        install.run(self)


setup(
    name='swiftype',
    version=VERSION,
    description='A Deprecated Swiftype Site Search API Client for Python.  - Use new elastic-site-search package instead.',
    author='Swiftype',
    author_email='team@swiftype.com',
    url='https://swiftype.com/',
    packages=find_packages(),
    install_requires=["anyjson", "six"],
    test_suite='nose.collector',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    cmdclass={
        'install': PostInstallMessage,
    }
)
