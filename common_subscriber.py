#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import redis
import datetime

"""Simple subscriher which listens for messages published to a redis server
on a given channvel.

TODO: More detail here...
"""

WINDOW_SIZE = 5		# seconds

class CommonSubscriber:
  """Common (abstract) base class for both subscribers."""

  start_time = None

  def message_handler(self, message):
    if self.start_time is None:
      self.start_time = datetime.datetime.now()
    else:
      now = datetime.datetime.now()
      delta = now - self.start_time
      if delta.total_seconds() >= WINDOW_SIZE:
        self.output_result_and_reset()
        self.start_time = now
  
    self.handle_message(message) 

  # abstract
  def output_result_and_reset(self):
    pass

  # abstract
  def handle_message(self, message):
    pass

  def parse_command_line(self):
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

    d = {}
    d['hostname'] = hostname
    d['port'] = port
    d['channel'] = channel

    return d

  def run(self):
    opts = self.parse_command_line()
    r = redis.StrictRedis(host=opts['hostname'], port=opts['port'], db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe(**{opts['channel']: self.message_handler})

    for message in p.listen():
      pass

