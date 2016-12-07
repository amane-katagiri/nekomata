#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logging handler used in Nekomata."""

from logging import DEBUG
from logging import getLogger
from logging import StreamHandler

from twitter import OAuth
from twitter import Twitter

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class TwitterHandler(StreamHandler):
    """Logging handler which sends records to your Slack team."""

    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_secret):
        self._t = Twitter(auth=OAuth(access_token, access_secret,
                                     consumer_key, consumer_secret))
        super().__init__()

    def emit(self, record):
        self._t.statuses.update(status=self.format(record))
