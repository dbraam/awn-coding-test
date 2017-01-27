#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import numpy
from common_subscriber import CommonSubscriber

"""Simple subscriher which listens for messages published to a redis server
on a given channvel.

This subscriber calculates the median of all of the integer messages it receives
over a specified period of time (the window size) on the configured channel and
outputs the result after each window.
"""

def median(lst):
  return numpy.median(numpy.array(lst))

class MedianSubscriber(CommonSubscriber):
  _entries_in_window = []

  def _output_result_and_reset(self):
    print 'Median of integers received in last {0} seconds:'.format(
      self._opts['window']),
    print str(int(median(self._entries_in_window)))
    self._entries_in_window = []

  def _handle_message(self, message):
    self._entries_in_window.append(int(message['data']))

  def _get_usage_description(self):
    return 'Subscriber that calculates the median of the integers received ' \
         + 'during each window.'

def main():
  subscriber = MedianSubscriber()
  subscriber.run()

if __name__ == '__main__':
  main()
