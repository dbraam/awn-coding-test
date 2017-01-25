#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import unittest
from ..components import publisher

"""Unit tests for the publisher module.
"""

class PublisherTests(unittest.TestCase):

  def test_parse_command_line_default_channel(self):
    opts = publisher.parse_command_line(['./publisher.py'])
    self.assertTrue('default-channel' == opts['channel'])

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(PublisherTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
