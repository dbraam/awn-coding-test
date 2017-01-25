#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

from common_subscriber import CommonSubscriber

"""Simple subscriher which listens for messages published to a redis server
on a given channvel.

This subscriber sums all of the integer messages it receives over a specified
period of time (the window size) on the configured channel and outputs the
result after each window.
"""

class Subscriber1(CommonSubscriber):
  _sum = 0

  def _output_result_and_reset(self):
    print 'Sum of integers received in last {0} seconds: '.format(
      self._opts['window_size_seconds']) + str(self._sum)
    self._sum = 0

  def _handle_message(self, message):
    self._sum += int(message['data'])    

def main():
  subscriber = Subscriber1()
  subscriber.run()

if __name__ == '__main__':
  main()
