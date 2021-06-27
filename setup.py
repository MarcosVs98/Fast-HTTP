"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""
import os
import re
import sys

from codecs import open
from setuptools import setup
from setuptools.command.test import test as TestCommand

BASE = os.path.abspath(os.path.dirname(__file__))

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist bdist_wheel')
	os.system('twine upload dist/*')
	sys.exit()

packages = ['fasthttp', 'tests']

requires = [
	"requests==2.22.0",
	"colorama==0.4.3",
	"aiohttp==3.7.4.post0",
	"urllib3==1.25.11",
	"dataclasses==0.8" ,
]

test_requirements = []

about = {}
with open(os.path.join(BASE, 'fasthttp', '__version__.py'), 'r', 'utf-8') as f:
	exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
	readme = f.read()

setup(
	name=about['__title__'],
	version=about['__version__'],
	description=about['__description__'],
	long_description=readme,
	long_description_content_type='text/markdown',
	author=about['__author__'],
	author_email=about['__author_email__'],
	url=about['__url__'],
	packages=packages,
	include_package_data=True,
	python_requires=">=3.6",
	install_requires=requires,
	license=about['__license__'],
	tests_require=test_requirements,
)

# end-of-file