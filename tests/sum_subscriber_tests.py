#!/usr/bin/python
# Copyright 2017 Doug Braam
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import unittest
from . import common_subscriber_tests
from components import sum_subscriber

"""Unit tests for the sum_subscriber module.
"""


class SumSubscriberTests(common_subscriber_tests.CommonSubscriberTests):
    def _get_opts(self):
        return sum_subscriber.SumSubscriber()._opts

    def _get_default_queue(self):
        return 'SumQueue'


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SumSubscriberTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
