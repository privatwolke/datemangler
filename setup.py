#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import sys, os

version = '0.2.2'

setup(name = 'datemangler',
	version = version,
	description = 'This script modifies the last four bits of an NTFS timestamp to hide information.',
	long_description = open('README.rst', 'r').read(),
	keywords = 'NTFS encryption meta stenography hidden AES',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: POSIX',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Topic :: Utilities'
	],
	author = 'Stephan Klein',
	url = 'https://github.com/privatwolke/datemangler',
	license = 'MIT',
	packages = ['datemangler'],
	install_requires = ['xattr', 'pycrypto'],
	package_dir = {
		'datemangler': 'datemangler'
	},
	zip_safe = True,
	entry_points = {
		'console_scripts': [
			'datemangler = datemangler.__main__:main'
		]
	}
)
