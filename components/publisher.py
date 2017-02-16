#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import random
import time

import boto3

"""Simple publisher which publishes random integers to an AWS SNS topic.
"""

parser = argparse.ArgumentParser(description='Publish random integers.')
parser.add_argument('--topic', default='random-integers',
        help='the topic to publish to (default: %(default)s)')
parser.add_argument('--min', default=0, type=int,
        help='minimum value of the sandbox integers (default: %(default)s)')
parser.add_argument('--max', default=1000, type=int,
        help='maximum value of the sandbox integers (default: %(default)s)')
parser.add_argument('--frequency', default=20, type=int,
        help='number of messages to generate per second (default: %(default)s)')


def main():
    opts = vars(parser.parse_args())
    print 'publishing on topic: ' + opts['topic']
    client = boto3.client('sns')
    topic = client.create_topic(Name=opts['topic'])

    while True:
        client.publish(TargetArn=topic['TopicArn'], Message=str(
            random.randint(opts['min'], opts['max'])))
        time.sleep(1.0 / opts['frequency'])


if __name__ == '__main__':
    main()
