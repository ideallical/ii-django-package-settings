#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from io import open

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])

    return {package: filepaths}


version = get_version('ii_django_package_settings')

setup(
    name='ii_django_package_settings',
    version=version,
    description='ideallical django package settings',
    url='https://github.com/ideallical/ii-django-package-settings',
    download_url=('https://github.com/ideallical/ii-django-package-settings/'
                  'archive/{}.tar.gz'.format(version)),
    author='ideallical',
    author_email='info@ideallical.com',
    keywords=['django', 'package', 'settings'],
    license='BSD',
    install_requires=[],
    packages=get_packages('ii_django_package_settings'),
    package_data=get_package_data('ii_django_package_settings'),
    zip_safe=False
)
