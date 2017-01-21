#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import redis
import datetime

"""Common base class for subscrihers which listen for messages published to a
redis server on a given channvel.
"""

WINDOW_SIZE = 5		# seconds

class CommonSubscriber:
  """Common (abstract) base class for both subscribers."""

  _start_time = None

  def message_handler(self, message):
    if self._start_time is None:
      self._start_time = datetime.datetime.now()
    else:
      now = datetime.datetime.now()
      delta = now - self._start_time
      if delta.total_seconds() >= WINDOW_SIZE:
        self._output_result_and_reset()
        self._start_time = now
  
    self._handle_message(message) 

  # abstract
  def _output_result_and_reset(self):
    pass

  # abstract
  def _handle_message(self, message):
    pass

  def run(self):
    opts = parse_command_line()
    r = redis.StrictRedis(host=opts['hostname'], port=opts['port'], db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe(**{opts['channel']: self.message_handler})

    for message in p.listen():
      pass

def parse_command_line():
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
