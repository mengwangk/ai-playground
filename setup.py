#!/usr/bin/env python

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import unittest
version = '0.1.0'

def myInvestor_toolkit_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('myInvestor-toolkit', pattern='*_test.py')
    return test_suite

setup(name='myInvestor-toolkit',
      version=version,
      description='Toolkit library for investment',
      author='Koh Meng Wang',
      packages=find_packages(),
      url='https://mengwangk.github.io/',
      install_requires=['pytest', 'pylint', 'yahoofinancials', 'pandas', 'ta', 'backtrader', 'pyalgotrade'],
      test_suite='setup.myInvestor_toolkit_test_suite'
      )