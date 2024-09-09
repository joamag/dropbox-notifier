#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

setuptools.setup(
    name="dropbox-notifier",
    version="0.2.10",
    author="João Magalhães",
    author_email="joamag@gmail.com",
    description="Dropbox Notifier",
    license="Apache License, Version 2.0",
    keywords="dropbox notifier api",
    url="http://dropbox-notifier.joao.me",
    zip_safe=False,
    packages=[
        "dropbox_notifier",
        "dropbox_notifier.controllers",
        "dropbox_notifier.models",
    ],
    package_dir={"": os.path.normpath("src")},
    package_data={"dropbox_notifier": ["templates/*.tpl", "templates/email/*.tpl"]},
    install_requires=["appier", "appier-extras"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
