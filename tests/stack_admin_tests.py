#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import unittest
from ..setup import stack_admin

"""Unit tests for the stack_admin module.
"""


class StackAdminTests(unittest.TestCase):
    def test_num_available_create_opts(self):
        opts = vars(stack_admin.parser.parse_args(['create']))
        self.assertTrue(len(opts) == 5)

    def test_num_available_delete_opts(self):
        opts = vars(stack_admin.parser.parse_args(['delete']))
        self.assertTrue(len(opts) == 2)

    def test_create_opt_names(self):
        opts = vars(stack_admin.parser.parse_args(['create']))
        valid_opts = ('action', 'name', 'queue1', 'queue2', 'topic')
        self.assertTrue(valid_opts == tuple(sorted(opts.keys())))

    def test_delete_opt_names(self):
        opts = vars(stack_admin.parser.parse_args(['delete']))
        valid_opts = ('action', 'name')
        self.assertTrue(valid_opts == tuple(sorted(opts.keys())))

    def test_create_default_topic(self):
        self._verify_create_opt('topic', 'random-integers')

    def test_create_default_queue1(self):
        self._verify_create_opt('queue1', 'SumQueue')

    def test_create_default_queue2(self):
        self._verify_create_opt('queue2', 'MedianQueue')

    def test_create_default_name(self):
        self._verify_create_opt('name', 'AWNCodingTest')

    def test_delete_default_name(self):
        self._verify_delete_opt('name', 'AWNCodingTest')

    def _verify_create_opt(self, key, value):
        opts = vars(stack_admin.parser.parse_args(['create']))
        self.assertTrue(opts[key] == value)

    def _verify_delete_opt(self, key, value):
        opts = vars(stack_admin.parser.parse_args(['delete']))
        self.assertTrue(opts[key] == value)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(StackAdminTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
