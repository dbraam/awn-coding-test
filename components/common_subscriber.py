#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import sys
import json
import boto3
import datetime

"""Common base class for subscrihers which listen for messages published to an
AWS SQS queue which is subscribed to an AWS SNS topic.
"""

class CommonSubscriber:
  """Common (abstract) base class for both subscribers."""

  _opts = {}
  _start_time = None

  def _message_handler(self, message):
    if self._start_time is None:
      self._start_time = datetime.datetime.now()
    else:
      now = datetime.datetime.now()
      delta = now - self._start_time
      if delta.total_seconds() >= self._opts['window']:
        self._output_result_and_reset()
        self._start_time = now

    body = json.loads(message.body)  
    self._handle_message(body)
    message.delete()

  # abstract
  def _output_result_and_reset(self):
    pass

  # abstract
  def _handle_message(self, body):
    pass

  # abstract
  def _get_usage_description(self):
    pass

  # abstract
  def _get_default_queue(self):
    pass

  def __init__(self):
    parser = argparse.ArgumentParser(description=self._get_usage_description())
    parser.add_argument('--topic', default='random-integers',
      help='the topic to subscribe to (default: %(default)s)')
    parser.add_argument('--queue', default=self._get_default_queue(),
      help='the queue to receive messages from (default: %(default)s)')
    parser.add_argument('--window', default = 5, type=int,
      help='window size in seconds to accumulate data (default: %(default)s)')

    self._opts = vars(parser.parse_args())

  def run(self):
    print 'subscribing to topic {0} using queue {1}'.format(
      self._opts['topic'], self._opts['queue'])
    sqs = boto3.resource('sqs')
    queue = sqs.create_queue(QueueName=self._opts['queue'])
    queue.purge()
    while True:
      messages = queue.receive_messages()
      for message in messages:
        self._message_handler(message)

