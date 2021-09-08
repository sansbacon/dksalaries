# dksalaries/setup.py
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Eric Truett
# Licensed under the MIT License


from setuptools import setup, find_packages

PACKAGE_NAME = "dksalaries"


def run():
    setup(name=PACKAGE_NAME,
          version="0.3",
          description="python library for getting/parsing DK salaries",
          author="Eric Truett",
          author_email="eric@erictruett.com",
          license="MIT",
          packages=find_packages(),
          package_data={'tests': ["data/*.json"]},
          entry_points={'console_scripts': ['salaries=scripts.getsalaries:run']},
          install_requires=[
            'requests',
            'requests_cache',
            'browser_cookie3',
            'attrs',
            'cattrs',
            'python-dateutil',
            'pytz',
            'nflnames',
            'rapidfuzz'
          ],
          zip_safe=False)


if __name__ == '__main__':
    run()
