#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logging handler used in Nekomata."""

import json
from logging import DEBUG
from logging import getLogger
from logging import StreamHandler
from logging.handlers import HTTPHandler

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class SlackHandler(HTTPHandler):
    """Logging handler which sends records to your Slack team."""

    def __init__(self, token: str):
        super().__init__("hooks.slack.com", "/services/{}".format(token),
                         "POST", secure=True)

    def mapLogRecord(self, record):
        """Set POST parameters.

        POST payload: quote('payload={"text": "MESSAGE"}')
        """
        return {"payload": json.dumps({"text": self.format(record)})}
