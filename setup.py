# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import setup, find_packages

from avashell import APP_NAME, __version__

setup(
    name=APP_NAME,
    version=__version__,
    description="A system tray application to run a Python script on start up.",
    # package_dir={'': ''},
    packages=find_packages(exclude=['**/tests/*']),
    include_package_data=True,

    zip_safe=False,

    entry_points={
        'gui_scripts': [
            'avashell = avashell.launcher:main',
        ],
    },

    author="Sampot",
    url="https://samkuo.me",

)