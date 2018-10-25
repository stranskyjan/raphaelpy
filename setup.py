#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from raphaelpy import version

with open('README.md') as f:
	long_description = f.read()

setuptools.setup(
	name = 'raphaelpy',
	version = version,
	description = 'Library for creating SVG drawings using Python, inspired by RaphaëlJS',
	author = 'Jan Stransky',
	author_email = 'honzik.stransky@gmail.com',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/stranskyjan/raphaelpy',
	license = "LGPL",
	keywords = "Python SVG RaphaelJS Raphael",
	packages = ['raphaelpy'],
	classifiers = [
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent',
	],
)
