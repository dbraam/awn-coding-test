#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

from common_subscriber import CommonSubscriber

"""Simple subscriber which listens for messages published to an AWS SQS queue
subscribed to an AWS SNS topic.

This subscriber sums all of the integer messages it receives over a specified
period of time (the window size) on the configured channel and outputs the
result after each window.
"""


class SumSubscriber(CommonSubscriber):

    def __init__(self):
        super(SumSubscriber, self).__init__()
        self._sum = 0

    def _output_result_and_reset(self):
        print 'Sum of integers received in last {0} seconds: '.format(
            self._opts['window']) + str(self._sum)
        self._sum = 0

    def _handle_message(self, body):
        self._sum += int(body['Message'])

    def _get_usage_description(self):
        return 'Subscriber that sums the integers received during each window.'

    def _get_default_queue(self):
        return 'SumQueue'


def main():
    subscriber = SumSubscriber()
    subscriber.run()


if __name__ == '__main__':
    main()
