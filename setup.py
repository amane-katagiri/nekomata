#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup file for Distutils."""

from logging import DEBUG
from logging import getLogger
from logging import StreamHandler

import nekomata

from setuptools import find_packages
from setuptools import setup

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

setup(name="Nekomata",
      version=nekomata.__version__,
      description="A simple ARP packet logger.",
      author="Amane Katagiri",
      author_email="amane@ama.ne.jp",
      url="https://amane-katagiri.github.io/nekomata",
      install_requires=[
          "nekomata",
          "scapy-python3",
          "rstr",
          "toml",
          "twitter",
      ],
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      nekomata = nekomata.main:main
      """)
