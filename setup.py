#!/usr/bin/env python

import os

from setuptools import find_packages
from setuptools import setup

NAME =               'icypher'
VERSION =            '0.1.4'
AUTHOR =             'Lev E. Givon'
AUTHOR_EMAIL =       'lev@columbia.edu'
URL =                'https://github.com/lebedov/icypher/'
DESCRIPTION =        'Cypher access to Neo4J via IPython'
LONG_DESCRIPTION =   DESCRIPTION
DOWNLOAD_URL =       URL
LICENSE =            'BSD'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Framework :: IPython',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development',
    'Topic :: Database',
    'Topic :: Database :: Front-Ends']
PACKAGES =           find_packages()

if __name__ == "__main__":
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    setup(
        name = NAME,
        version = VERSION,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        license = LICENSE,
        classifiers = CLASSIFIERS,
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        url = URL,
        packages = PACKAGES,
        install_requires = ['ipython>=1.0',
                            'py2neo>=2.0',
                            'httpstream==1.3.0'])
