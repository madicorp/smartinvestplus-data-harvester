#!/usr/bin/env python
import pip
from setuptools import setup, find_packages

# If in install_requires, the wheel is not downloaded and there is an error on macos
pip.main(['install', 'cryptography'])
setup(name='smartinvestplus_data_spider',
      version='0.1.0',
      description='Smartinvestplus data spider',
      author='ekougs',
      author_email='ekougs@gmail.com',
      url='',
      long_description='README.adoc',
      packages=find_packages(),
      install_requires=['scrapy==1.1.1', 'pymongo']
      )
