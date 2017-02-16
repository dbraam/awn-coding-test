#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import unittest
from abc import ABCMeta
from abc import abstractmethod

"""Unit tests for the common_subscriber module.
"""


class CommonSubscriberTests(unittest.TestCase):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _get_opts(self):
        return {}

    @abstractmethod
    def _get_default_queue(self):
        return ''

    def test_num_available_opts(self):
        opts = self._get_opts()
        self.assertTrue(len(opts) == 3)

    def test_opt_names(self):
        opts = self._get_opts()
        valid_opts = ('queue', 'topic', 'window')
        self.assertTrue(valid_opts == tuple(sorted(opts.keys())))

    def test_default_topic(self):
        self._verify_opt('topic', 'random-integers')

    def test_default_window(self):
        self._verify_opt('window', 5)

    def test_default_queue(self):
        self._verify_opt('queue', self._get_default_queue())

    def _verify_opt(self, key, value):
        opts = self._get_opts()
        self.assertTrue(opts[key] == value)
