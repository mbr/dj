#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='dj',
    version='0.1dev',
    description='Downloads tracks from all over the net.',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='http://github.com/mbr/dj',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['click', 'requests', 'six', 'mutagen'],
    entry_points={
        'console_scripts': [
            'dj = dj.cli:main',
        ],
    }
)
