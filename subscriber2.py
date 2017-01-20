#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import redis
import datetime
import numpy

"""Simple subscriher which listens for messages published to a redis server
on a given channvel.

TODO: More detail here...
"""

WINDOW_SIZE = 5		# seconds

def median(lst):
    return numpy.median(numpy.array(lst))

entries_in_window = []
start_time = None

def message_handler(message):
  global start_time
  global entries_in_window

  if start_time is None:
    start_time = datetime.datetime.now()
  else:
    now = datetime.datetime.now()
    delta = now - start_time
    if delta.total_seconds() >= WINDOW_SIZE:
      print 'Median of integers received in last 5 seconds:',
      print str(int(median(entries_in_window)))
      entries_in_window = []
      start_time = now
  
  entries_in_window.append(int(message['data']))

def main():
  script_name = sys.argv[0]
  args = sys.argv[1:]

  usage = 'usage: ' + script_name + ' [--channel channel]'

  channel = ''
  hostname = 'localhost'
  port = 6379

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

  if len(channel) == 0:
    channel = 'default-channel'

  print 'subscribing on channel: ' + channel

  r = redis.StrictRedis(host=hostname, port=port, db=0)
  p = r.pubsub(ignore_subscribe_messages=True)
  p.subscribe(**{channel: message_handler})

  for message in p.listen():
    pass

if __name__ == '__main__':
  main()
