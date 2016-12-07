#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import DEBUG
from logging import getLogger
from logging import Formatter
from logging import INFO
from logging import StreamHandler
from typing import Callable
from typing import List

from scapy.all import ARP

from . import handlers
from .utils import DEFAULT_MAC

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class NekomataLogger(object):
    """Send random messages to logger."""

    def __init__(self, handler: str, generator: Callable[[str], str],
                 senders: List, **options):
        self._handler = StreamHandler()
        try:
            self._handler = getattr(handlers, handler)(**options)
        except AttributeError as ex:
            logger.error("Handler '{}' not found.".format(handler))
            raise ex
        except TypeError as ex:
            logger.error("Incorrect option(s) for '{}'.".format(handler))
            raise ex
        formatter = Formatter("%(message)s")
        self._handler.setLevel(INFO)
        self._handler.setFormatter(formatter)
        self._logger = getLogger(handler)
        self._logger.setLevel(INFO)
        self._logger.addHandler(self._handler)
        self._generator = generator
        if not senders or DEFAULT_MAC in senders:
            self._senders = list()
        else:
            self._senders = senders

    def send(self, param: str="") -> str:
        """Send a message using logger."""
        message = self.generate_message(param)
        self._logger.info(message)
        return message

    def generate_message(self, param: str="") -> str:
        """Generate a random message."""
        return self._generator(param)


class NekomataArpLogger(NekomataLogger):
    """Receive ARP packet and send message."""

    def __call__(self, p) -> None:
        """Called as `prn` in `scapy.all.sniff`."""
        if p[ARP].op == 1 and p[ARP].psrc == "0.0.0.0":
            logger.info("Recieved ARP packet from: {}".format(p[ARP].hwsrc))
            if not self._senders or p[ARP].hwsrc in self._senders:
                msg = self.send(p[ARP].hwsrc)
                logger.info("Sent a message '{}'".format(msg))
