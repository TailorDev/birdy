#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages

import db_fetcher
 

setup(
    name='db_fetcher',
    version="0.1", # db_fetcher.__version__,
    packages=find_packages(),
    author="Camille Loiseau",
    description="Fetches files in biology databases",
    long_description=open('README.md').read(),
    entry_points = {
        'console_scripts': [
            'db-fetcher = db_fetcher.core:main',
        ],
    },

    # Active la prise en compte du fichier MANIFEST.in
    #include_package_data=True,
)