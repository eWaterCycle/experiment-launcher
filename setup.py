#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

requirements = ['nbformat', 'requests', 'connexion[swagger-ui]', 'connexion', 'gunicorn', 'decorator',
                'simplepam', 'flask-cors', 'jsonschema==3.2.0']


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
        'Programming Language :: Python :: 3.8',
    ],
    description="Webservice to generate and launch a Jupyter notebook",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='ewatercycle_experiment_launcher',
    name='ewatercycle_experiment_launcher',
    packages=find_packages(),
    test_suite='tests',
    url='https://github.com/ewatercycle/ewatercycle_experiment_launcher',
    version='0.2.0',
    zip_safe=False,
    package_data={
      'ewatercycle_experiment_launcher': ['openapi.yaml'],
    },
)
