#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import sys
import redis
import time
import random

"""Simple publisher which publishes random integers to a redis server.
"""

parser = argparse.ArgumentParser(description='Publish random integers.')
parser.add_argument('--channel', default='default-channel',
  help='the channel to publish to (default: %(default)s)')
parser.add_argument('--hostname', default='localhost',
  help='the hostname of the redis server (default: %(default)s)')
parser.add_argument('--port', default=6379, type=int,
  help='the port number of the redis server (default: %(default)s)')
parser.add_argument('--min', default = 0, type=int,
  help='minimum value of the sandbox integers (default: %(default)s)')
parser.add_argument('--max', default = 1000, type=int,
  help='maximum value of the sandbox integers (default: %(default)s)')
parser.add_argument('--frequency', default = 20, type=int,
  help='number of messages to generate per second (default: %(default)s)')

def main():
  opts = vars(parser.parse_args())
  print 'publishing on channel: ' + opts['channel']
  r = redis.StrictRedis(host=opts['hostname'], port=opts['port'], db=0)

  while True:
    r.publish(opts['channel'], random.randint(opts['min'], opts['max']))
    time.sleep(1.0 / opts['frequency'])

if __name__ == '__main__':
  main()
