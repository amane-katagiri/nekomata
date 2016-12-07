#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from logging import DEBUG
from logging import getLogger
from logging import StreamHandler

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


def get_mac_address_as_decimal(param: str) -> str:
    try:
        num = int(param.replace(":", ""), base=16)
    except Exception:
        num = 0
    return str(num)
