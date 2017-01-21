#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import redis
import time
import random

"""Simple publisher which publishes random integers to a redis server.
"""

def parse_command_line():
  script_name = sys.argv[0]
  args = sys.argv[1:]

  usage = 'usage: ' + script_name + ' [--channel channel]'

  opts = {'channel' : 'default-channel',
          'hostname' : 'localhost',
          'port' : 6379,
          'min_int' : 0,
          'max_int' : 1000,
          'messages_per_second' : 20}

  if args:
    if args[0] == '-?':
      print usage
      sys.exit(1)
    elif args[0] == '--channel':
      del args[0]
      opts['channel'] = args[0]
    else:
      print 'invalid option: ' + args[0]
      print usage

  print 'publishing on channel: ' + opts['channel']

  return opts

def main():
  opts = parse_command_line()
  r = redis.StrictRedis(host=opts['hostname'], port=opts['port'], db=0)

  while True:
    r.publish(opts['channel'], random.randint(opts['min_int'], opts['max_int']))
    time.sleep(1.0 / opts['messages_per_second'])

if __name__ == '__main__':
  main()
