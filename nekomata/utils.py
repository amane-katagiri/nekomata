#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import DEBUG
from logging import getLogger
from logging import StreamHandler
from typing import Callable

import rstr

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

DEFAULT_MAC = "00:00:00:00:00:00"


def gen_xeger(regex: str) -> Callable[[str], str]:
    """Generate random string generator."""
    def f(x):
        return rstr.xeger(regex)
    return f
