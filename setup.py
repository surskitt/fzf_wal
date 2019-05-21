#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

#  requirements = []
with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="\"Shane Donohoe",
    author_email='shane@donohoe.cc',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="pywal theme selector using fzf",
    install_requires=requirements,
    entry_points={
        "console_scripts": ['fzf-wal = fzf_wal.fzf_wal:main']
    },
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fzf_wal',
    name='fzf_wal',
    packages=find_packages(include=['fzf_wal']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/shanedabes/fzf_wal',
    version='0.1.2',
    zip_safe=False,
)
