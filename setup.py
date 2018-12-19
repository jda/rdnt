#!/usr/bin/env python

from setuptools import setup

setup(
    name="rdnt",
    packages=["rdnt"],
    entry_points={"console_scripts": ["rdnt = rdnt.__main__:main"]},
)
