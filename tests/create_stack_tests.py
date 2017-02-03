#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import unittest
from ..components import create_stack

"""Unit tests for the create_stack module.
"""

class CreateStackTests(unittest.TestCase):

  def test_num_available_opts(self):
    opts = vars(create_stack.parser.parse_args([]))
    self.assertTrue(len(opts) == 4)

  def test_opt_names(self):
    opts = vars(create_stack.parser.parse_args([]))
    valid_opts = ('name', 'queue1', 'queue2', 'topic')
    self.assertTrue(valid_opts == tuple(sorted(opts.keys())))

  def test_default_topic(self):
    self._verify_opt('topic', 'random-integers')

  def test_default_name(self):
    self._verify_opt('name', 'SNSToSQS')

  def test_default_queue2(self):
    self._verify_opt('queue2', 'MedianQueue')

  def _verify_opt(self, key, value):
    opts = vars(create_stack.parser.parse_args([]))
    self.assertTrue(opts[key] == value)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(CreateStackTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
