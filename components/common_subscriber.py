#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
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
      if delta.total_seconds() >= self._opts['window']:
        self._output_result_and_reset()
        self._start_time = now
  
    self._handle_message(message) 

  # abstract
  def _output_result_and_reset(self):
    pass

  # abstract
  def _handle_message(self, message):
    pass

  # abstract
  def _get_usage_description(self):
    pass

  def __init__(self):
    parser = argparse.ArgumentParser(description=self._get_usage_description())
    parser.add_argument('--channel', default='default-channel',
      help='the channel to subscribe to (default: %(default)s)')
    parser.add_argument('--hostname', default='localhost',
      help='the hostname of the redis server (default: %(default)s)')
    parser.add_argument('--port', default=6379, type=int,
      help='the port number of the redis server (default: %(default)s)')
    parser.add_argument('--window', default = 5, type=int,
      help='window size in seconds to accumulate data (default: %(default)s)')

    self._opts = vars(parser.parse_args())

  def run(self):
    r = redis.StrictRedis(host=self._opts['hostname'], port=self._opts['port'],
       db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    print 'subscribing to channel: ' + self._opts['channel']
    p.subscribe(**{self._opts['channel']: self.message_handler})

    for message in p.listen():
      pass
