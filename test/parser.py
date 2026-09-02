#!/usr/bin/env python

"""Python server parser selection tests."""

import os
import sys
import urllib.request

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)
netron = __import__("source")


def _test_parser_metadata():
    address = netron.serve(__file__, address=("localhost", 0), parser="tf")
    try:
        with urllib.request.urlopen(
            f"http://{address[0]}:{address[1]}", timeout=5
        ) as response:
            content = response.read().decode("utf-8")
        assert '<meta name="parser" content="tf">' in content
    finally:
        netron.stop(address)


def _test_invalid_parser():
    try:
        netron.serve(__file__, address=("localhost", 0), parser="../tf")
    except ValueError as error:
        assert str(error) == "Invalid parser '../tf'."
    else:
        raise AssertionError("Invalid parser was accepted.")


_test_parser_metadata()
_test_invalid_parser()
