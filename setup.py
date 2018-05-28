#!/usr/bin/env python
"""Defines the Bouce Python package."""

from distutils.core import setup


def get_requirements():
    """Returns a list of required packages for Bounce installation."""
    return [
        line.split()[0] for line in open('requirements.txt', 'r').readlines()
        if not line.startswith('#')
    ]


setup(
    name='bounce',
    version='0.1',
    description=('Backend for Bounce - bringing people with '
                 'common interests together'),
    author='UBC Launch Pad',
    license='MIT',
    author_email='team@ubclaunchpad.com',
    install_requires=get_requirements(),
    packages=['server', 'cli'],
    entry_points={'console_scripts': ['bounce=cli:cli']},
)
