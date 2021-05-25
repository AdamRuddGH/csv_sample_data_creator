#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Adam Rudd",
    author_email='adam@adamrudd.net',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Generate CSVs with sample data based on datatypes you specify. Useful for SQL tests where you have not been given actual data",
    entry_points={
        'console_scripts': [
            'csv_sample_data_creator=csv_sample_data_creator.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='csv_sample_data_creator',
    name='csv_sample_data_creator',
    packages=find_packages(include=['csv_sample_data_creator', 'csv_sample_data_creator.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/adamruddGH/csv_sample_data_creator',
    version='0.1.0',
    zip_safe=False,
)
