#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import sys
import boto3
import json

"""Creates the AWS CloudFormation stack needed for the publish / subscribe
exercise. This includes creating an SNS topic to publish to and 2 SQS queues
subscribed to the topic.
"""

parser = argparse.ArgumentParser(description='Setup AWS CloudFormation stack.')
parser.add_argument('--name', default='SNSToSQS',
  help='the name of the stack (default: %(default)s)')
parser.add_argument('--topic', default='random-integers',
  help='the topic to publish to (default: %(default)s)')
parser.add_argument('--queue1', default='SumQueue',
  help='the first queue subscribed to the topic (default: %(default)s)')
parser.add_argument('--queue2', default='MedianQueue',
  help='the second queue subscribed to the topic (default: %(default)s)')

def main():
  opts = vars(parser.parse_args())
  print 'Creating stack {0}, topic {1}, queues {2}, {3}'.format(opts['name'],
    opts['topic'], opts['queue1'], opts['queue2'])
  cloudformation = boto3.resource('cloudformation')
  with open('./aws_stack.json', 'rB') as template_file:
    template_string = template_file.read()
  template = json.loads(template_string)

  stack = cloudformation.create_stack(
    StackName=opts['name'],
    TemplateBody=template_string,
    Parameters=[
      {
        'ParameterKey': 'MyPublishUserPassword',
        'ParameterValue': 'x',
        'UsePreviousValue': True
      },
      {
        'ParameterKey': 'MyQueueUserPassword',
        'ParameterValue': 'x',
        'UsePreviousValue': True
      }
    ],
    Capabilities=['CAPABILITY_IAM']
  )
  print 'Stack created(?)'

if __name__ == '__main__':
  main()
