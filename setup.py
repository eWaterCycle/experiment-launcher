#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'nbformat', 'requests', 'connexion', 'gunicorn', 'decorator', 'simplepam']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Stefan Verhoeven",
    author_email='s.verhoeven@esciencecenter.nl',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Webservice to generate and launch a Jupyter notebook",
    entry_points={
        'console_scripts': [
            'ewatercycle_experiment_launcher=ewatercycle_experiment_launcher.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ewatercycle_experiment_launcher',
    name='ewatercycle_experiment_launcher',
    packages=find_packages(include=['ewatercycle_experiment_launcher']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ewatercycle/ewatercycle_experiment_launcher',
    version='0.1.0',
    zip_safe=False,
    package_data={
      'ewatercycle_experiment_launcher': ['api.yaml'],
    },
)
