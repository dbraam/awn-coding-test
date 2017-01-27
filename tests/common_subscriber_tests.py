#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import unittest
from ..components import common_subscriber

"""Unit tests for the common_subscriber module.
"""

class CommonSubscriberTests(unittest.TestCase):

  # abstract method
  def _get_opts(self):
    pass

  def test_num_available_opts(self):
    opts = self._get_opts()
    self.assertTrue(len(opts) == 4)

  def test_opt_names(self):
    opts = self._get_opts()
    valid_opts = ('channel', 'hostname', 'port', 'window')
    self.assertTrue(valid_opts == tuple(sorted(opts.keys())))

  def test_default_channel(self):
    self._verify_opt('channel', 'default-channel')

  def test_default_hostname(self):
    self._verify_opt('hostname', 'localhost')

  def test_default_port(self):
    self._verify_opt('port', 6379)

  def test_default_window(self):
    self._verify_opt('window', 5)

  def _verify_opt(self, key, value):
    opts = self._get_opts()
    self.assertTrue(opts[key] == value)
