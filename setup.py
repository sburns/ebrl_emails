#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Scott Burns <scott.s.burns@gmail.com>'
__license__ = 'BSD 3-Clause'

import os
import ebrl

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if __name__ == '__main__':

    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')
    
    setup(name='ebrl',
        maintainer='Scott Burns',
        maintainer_email='scott.s.burns@gmail.com',
        description="""ebrl: education and brain research lab tools""",
        license='BSD (3-clause)',
        url='http://github.com/sburns/ebrl_emails',
        version=ebrl.__version__,
        download_url='http://github.com/sburns/ebrl_emails',
        packages=['ebrl'],
        requires=[],
        platforms='any',
        classifiers=(
                'Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved',
                'Topic :: Software Development',
                'Topic :: Scientific/Engineering',
                'Operating System :: Microsoft :: Windows',
                'Operating System :: POSIX',
                'Operating System :: Unix',
                'Operating System :: MacOS',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.7',)
        )
