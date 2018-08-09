#!/usr/bin/env python3
# A very simple load tester
# Copyright 2018 Google
# Sebastian Weigand tdg@google.com

import poke
import os
import signal
import time
import argparse
from multiprocessing import Pool
from functools import partial

parser = argparse.ArgumentParser(
    description='A simple load tester!', epilog='A Sab handy-dandy script.')

parser.add_argument(
    'url', 
    nargs=1, 
    type=str, 
    help='The URL you wish to test.'
)

parser.add_argument(
    '--fulltext',
    action='store_true',
    default=False,
    help=
    'print the full text of HTTP response, instead of just the code (this will print a lot of text).'
)

parser.add_argument(
    '-i',
    '--iterations',
    type=int,
    nargs='?',
    default=20,
    help='The number of iterations to run [20].'
)

parser.add_argument(
    '-c',
    '--chunks',
    type=int,
    nargs='?',
    default=os.cpu_count(),
    help='The number of simultaneous processes to invoke [cpu_count].'
)

args = parser.parse_args()

args.url[0] = args.url[0].rstrip('/')
if not args.url[0].startswith('http://'):
    args.url[0] = 'http://' + args.url[0]


def init_worker():
    '''
    We establish an init_worker so that we can intercept signals,
    and kill the concurrent subprocesses:
    '''
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def concurrent_test(url, iterations, chunks, fulltext):
    '''
    A simple function which wraps the call, generates the collection
    of URLs to test, and feeds the appropriate pool.
    '''

    print('Getting "{}", {} times, {} calls at a time...'.format(
        url, iterations, chunks))
    
    try:
        pool = Pool(chunks, init_worker)

        # We need to pass in a keyword argument to the map, so use a partial:
        mapfunc = partial(poke.poke, full_text=args.fulltext)
        pool.map(mapfunc, (url for i in range(iterations)))
    
    except KeyboardInterrupt:
        print('\n  [Abort requested] - Roger that!')
        pool.terminate()
        pool.join()
    
    else:
        pool.close()
        pool.join()


concurrent_test(args.url[0], args.iterations, args.chunks, args.fulltext)
