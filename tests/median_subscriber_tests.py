#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import unittest
import common_subscriber_tests
from components import median_subscriber

"""Unit tests for the median_subscriber module.
"""


class MedianSubscriberTests(common_subscriber_tests.CommonSubscriberTests):
    def _get_opts(self):
        return median_subscriber.MedianSubscriber()._opts

    def _get_default_queue(self):
        return 'MedianQueue'


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MedianSubscriberTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
