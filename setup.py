#!/usr/bin/env python3

from setuptools import setup

setup(
    name='emailbot',
    version='0.1.0',
    description='A notifier bot for Euphoria.',
    author='Rishov Sarkar',
    url='https://github.com/ArkaneMoose/emailbot',
    license='MIT',
    packages=['emailbot'],
    package_dir={'emailbot': 'src'},
    install_requires=['eupy >=1.2, <2.0'],
    dependency_links=['git+https://github.com/ArkaneMoose/EuPy.git@9caf35d0d7370efbdba16c4903891c6e97526200#egg=eupy-1.2'],
    entry_points={
        'console_scripts': [
            'emailbot = emailbot.__main__:main'
        ]
    }
)
