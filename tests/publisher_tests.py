#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import unittest
from components import publisher

"""Unit tests for the publisher module.
"""


class PublisherTests(unittest.TestCase):
    def test_num_available_opts(self):
        opts = vars(publisher.parser.parse_args([]))
        self.assertTrue(len(opts) == 4)

    def test_opt_names(self):
        opts = vars(publisher.parser.parse_args([]))
        valid_opts = ('frequency', 'max', 'min', 'topic')
        self.assertTrue(valid_opts == tuple(sorted(opts.keys())))

    def test_default_topic(self):
        self._verify_opt('topic', 'random-integers')

    def test_default_min(self):
        self._verify_opt('min', 0)

    def test_default_max(self):
        self._verify_opt('max', 1000)

    def test_default_frequency(self):
        self._verify_opt('frequency', 20)

    def _verify_opt(self, key, value):
        opts = vars(publisher.parser.parse_args([]))
        self.assertTrue(opts[key] == value)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PublisherTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
