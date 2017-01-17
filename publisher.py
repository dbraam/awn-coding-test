#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import redis
import time
import random

"""Simple publisher which publishes random integers to a redis server.

TODO: More detail here...
"""

def main():
  script_name = sys.argv[0]
  args = sys.argv[1:]

  usage = 'usage: ' + script_name + ' [--channel channel]'

  channel = 'default-channel'
  hostname = 'localhost'
  port = 6379
  min_int = 0
  max_int = 1000

  if args:
    if args[0] == '-?':
      print usage
      sys.exit(1)
    elif args[0] == '--channel':
      del args[0]
      channel = args[0]
    else:
      print 'invalid option: ' + args[0]
      print usage

  print 'publishing on channel: ' + channel

  r = redis.StrictRedis(host=hostname, port=port, db=0)

  while True:
    r.publish(channel, random.randint(min_int, max_int))
    time.sleep(0.05)

if __name__ == '__main__':
  main()
