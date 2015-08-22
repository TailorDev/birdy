#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip.req import parse_requirements
from setuptools import setup, find_packages

install_reqs = parse_requirements('requirements.txt')
requirements = [str(ir.req) for ir in install_reqs]

setup(
    name='birdy',
    version=__import__('birdy').__version__,
    packages=find_packages(),
    author="Camille Loiseau",
    author_email='loiseauc48@gmail.com',
    description="A biological formats compilation tool",
    long_description=open('README.md').read(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        ],
    scripts=['scripts/birdy']
)
