#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def parse_requirements(requirements, ignore=('setuptools',)):
    """Read dependencies from requirements file (with version numbers if any)
    Note: this implementation does not support requirements files with extra
    requirements
    """
    with open(requirements) as f:
        packages = set()
        for line in f:
            line = line.strip()
            if line.startswith(('#', '-r', '--')):
                continue
            if '#egg=' in line:
                line = line.split('#egg=')[1]
            pkg = line.strip()
            if pkg not in ignore:
                packages.add(pkg)
    return packages


setup(
    name='birdy',
    version=__import__('birdy').__version__,
    packages=find_packages(),
    author="Camille Loiseau",
    author_email='loiseauc48@gmail.com',
    description="A biological formats compilation tool",
    long_description=open('README.md').read(),
    install_requires=parse_requirements('requirements.txt'),
    tests_require=parse_requirements('requirements-dev.txt'),
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
