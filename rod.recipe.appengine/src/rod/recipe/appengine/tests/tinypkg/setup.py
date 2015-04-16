"""Setup script."""

import os
from setuptools import setup, find_packages


setup (
    name='tinypkg',
    version='0.1.0',
    author="Someone Else",
    description="For testing purposes only.",
    long_description="",
    license="Apache License 2.0",
    keywords="dummy",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        ],
    url='',
    py_modules = ['tinymodule'],
    install_requires=['setuptools'],
    zip_safe=False,
    )
