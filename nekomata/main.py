#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import DEBUG
from logging import getLogger
from logging import StreamHandler

from scapy.all import sniff
import toml

from . import functions
from .logger import NekomataArpLogger
from .utils import DEFAULT_MAC
from .utils import gen_xeger

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


def serve(config):
    """Main Service."""
    message_senders = list()
    for k, v in config.items():
        if "log_format_text" in v:
            generator = gen_xeger(v["log_format_text"])
        elif "log_format_file" in v:
            generator = gen_xeger(open(v["log_format_file"]).read())
        elif "log_format_func" in v:
            try:
                generator = getattr(functions, v["log_format_func"])
            except AttributeError as ex:
                logger.error("Function '{}' not found.".format(handler))
                raise ex
            except TypeError as ex:
                logger.error("Function '{}' is invalid.".format(handler))
                raise ex
        else:
            generator = str

        v["senders"] = v.get("senders", list())
        if k != DEFAULT_MAC:
            v["senders"].append(k)

        m = NekomataArpLogger(v.get("handler", "StreamHandler"), generator,
                              v["senders"], **(v.get("option", dict())))
        message_senders.append(m)
    sniff(prn=lambda x: (lambda y: None)([f(x) for f in message_senders]),
          filter="arp", store=0)


def main():
    """Entry point."""
    import argparse
    import doctest
    doctest.testmod()

    parser = argparse.ArgumentParser(description="A simple ARP packet logger.")
    parser.add_argument("-e", type=str, nargs=1, default="",
                        help="regex of message (literal)")
    parser.add_argument("-f", type=str, nargs=1, default="",
                        help="regex of message (text file)")
    parser.add_argument("-g", type=str, nargs=1, default="",
                        help="regex of message (Python function)")
    parser.add_argument("-l", type=str, nargs=1, default="",
                        help="")
    parser.add_argument("--config", type=str, nargs=1, default="",
                        help="path to config file")
    parser.add_argument("mac_address", type=str, nargs="*",
                        help="MAC addresses Nekomata will react")
    args = parser.parse_args()

    if args.config:
        config = toml.load(args.config[0])
    else:
        config = {DEFAULT_MAC: dict()}

    if args.l:
        config[DEFAULT_MAC]["logger"] = args.l[0]

    if args.e:
        config[DEFAULT_MAC]["log_format_text"] = args.e[0]
    elif args.f:
        config[DEFAULT_MAC]["log_format_file"] = args.f[0]
    elif args.g:
        config[DEFAULT_MAC]["log_format_func"] = args.g[0]

    if args.mac_address:
        config[DEFAULT_MAC]["senders"] = args.mac_address

    serve(config)

if __name__ == "__main__":
    main()
