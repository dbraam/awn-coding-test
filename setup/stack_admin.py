#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import sys
import boto3
import json

"""Administers the AWS CloudFormation stack needed for the publish / subscribe
exercise. This includes administering an SNS topic to publish to and 2 SQS
queues subscribed to the topic.
"""

parser = argparse.ArgumentParser(
  description='Administer AWS CloudFormation stack.')
subparsers = parser.add_subparsers()
create_parser = subparsers.add_parser('create', help='create the stack')
create_parser.set_defaults(action='create')
create_parser.add_argument('--name', default='AWNCodingTest',
  help='the name of the stack to create (default: %(default)s)')
create_parser.add_argument('--topic', default='random-integers',
  help='the topic to publish to (default: %(default)s)')
create_parser.add_argument('--queue1', default='SumQueue',
  help='the first queue subscribed to the topic (default: %(default)s)')
create_parser.add_argument('--queue2', default='MedianQueue',
  help='the second queue subscribed to the topic (default: %(default)s)')
delete_parser = subparsers.add_parser('delete', help='delete the stack')
delete_parser.set_defaults(action='delete')
delete_parser.add_argument('--name', default='AWNCodingTest',
  help='the name of the stack to delete (default: %(default)s)')

cloudformation = boto3.resource('cloudformation')
client = boto3.client('cloudformation')

def read_json_template_from_file():
  with open('./aws_stack.json', 'rB') as template_file:
    template_string = template_file.read()
  template = json.loads(template_string)
  return template

def set_topic_name(json_template, topic_name):
  topic = json_template['Resources']['MySNSTopic']
  topic['Properties']['TopicName'] = topic_name

def set_queue_names(json_template, queue_1_name, queue_2_name):
  queue_1 = json_template['Resources']['MyQueue1']
  queue_1['Properties']['QueueName'] = queue_1_name
  queue_2 = json_template['Resources']['MyQueue2']
  queue_2['Properties']['QueueName'] = queue_2_name

def create_stack(opts):
  print 'Creating stack {0}, topic {1}, queues {2}, {3}'.format(opts['name'],
    opts['topic'], opts['queue1'], opts['queue2'])

  template = read_json_template_from_file()
  set_topic_name(template, opts['topic'])
  set_queue_names(template, opts['queue1'], opts['queue2'])
  template_string = json.dumps(template)

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
    Capabilities=['CAPABILITY_IAM'],
    OnFailure='DELETE',
  )
  print 'Waiting for stack creation to complete...'
  waiter = client.get_waiter('stack_create_complete')
  waiter.wait(StackName=opts['name'])
  print 'Stack created.'

def delete_stack(opts):
  client.delete_stack(StackName=opts['name'])
  print 'Waiting for stack deletion to complete...'
  waiter = client.get_waiter('stack_delete_complete')
  waiter.wait(StackName=opts['name'])
  print 'Stack deleted.'

def main():
  opts = vars(parser.parse_args())
  if opts['action'] == 'create':
    create_stack(opts)
  elif opts['action'] == 'delete':
    delete_stack(opts)
  else:
    print 'No action specified.'
    exit(1)

if __name__ == '__main__':
  main()
