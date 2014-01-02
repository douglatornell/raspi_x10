"""
RaspberryPi X10 Home Automation

Copyright 2013 Doug Latornell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from setuptools import setup
import __version__


python_classifiers = [
    'Programming Language :: Python :: {0}'.format(py_version)
    for py_version in ['3', '3.2', '3.3']]
other_classifiers = [
    'Development Status :: ' + __version__.dev_status,
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: Implementation :: CPython',
    'Operating System :: POSIX :: Linux',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'Natural Language :: English',
    'Topic :: Home Automation',
]

with open('README.rst', 'rt') as f:
    long_description = f.read()
install_requires = [
    # see requirements.txt for versions most recently used in development
    'pyramid==1.5a3',
    'pyramid_mako',
]
tests_require = [
    'coverage',
    'pytest',
    'tox',
]

setup(
    name='raspi_x10',
    version=__version__.number + __version__.release,
    description='Raspberry Pi X10 Home Automation',
    long_description=long_description,
    author='Doug Latornell',
    author_email='djl@douglatornell.ca',
    url='https://bitbucket.org/douglatornell/raspi_x10',
    license='Apache License, Version 2.0',
    classifiers=python_classifiers + other_classifiers,
    platforms=['Linux'],
    packages=['raspi_x10'],
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points="""\
    [paste.app_factory]
    web_remote = raspi_x10.web_remote:main
    """,
)
