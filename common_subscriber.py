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

class CommonSubscriber:
  """Common (abstract) base class for both subscribers."""

  _opts = {}
  _start_time = None

  def message_handler(self, message):
    if self._start_time is None:
      self._start_time = datetime.datetime.now()
    else:
      now = datetime.datetime.now()
      delta = now - self._start_time
      if delta.total_seconds() >= self._opts['window_size_seconds']:
        self._output_result_and_reset()
        self._start_time = now
  
    self._handle_message(message) 

  # abstract
  def _output_result_and_reset(self):
    pass

  # abstract
  def _handle_message(self, message):
    pass

  def __init__(self):
    self._opts = parse_command_line()

  def run(self):
    r = redis.StrictRedis(host=self._opts['hostname'], port=self._opts['port'],
       db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    print 'subscribing on channel: ' + self._opts['channel']
    p.subscribe(**{self._opts['channel']: self.message_handler})

    for message in p.listen():
      pass

def parse_command_line():
  script_name = sys.argv[0]
  args = sys.argv[1:]

  usage = 'usage: ' + script_name + ' [--channel channel]'

  opts = {'channel' : 'default-channel',
          'hostname' : 'localhost',
          'port' : 6379,
          'window_size_seconds' : 5}

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

  return opts
