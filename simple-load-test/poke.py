#!/usr/bin/env python3
# Load tester library
# Copyright 2018 Google
# Sebastian Weigand tdg@google.com

from requests import get
from requests.exceptions import ConnectionError
from http.client import RemoteDisconnected
from urllib3.exceptions import ProtocolError
import sys


def poke(url, full_text=False):
    ''' 
    Poke takes a URL, GETs it, and returns the status code.
    If full_text is True, it will return the body of the request as a string.

    It needs to be in a separate file to that pool.map() works properly.
    '''

    try:
        if full_text:
            print(get(url).text)

        else:
            print(get(url).status_code)

    except (RemoteDisconnected, ProtocolError, ConnectionError):
        sys.stderr.write('  HTTP Error: Connection prematurely terminated.\n')