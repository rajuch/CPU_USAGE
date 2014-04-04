#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Test suites for record usage functionality.

@created: 04-Apr-2014
@author: Anshu Kumar, <anshu.choubey@imaginea.com>
'''

# pylint: disable=C0103,R0904

import unittest
import app.record_usage as RU


class TestPeekableQueue(unittest.TestCase):
    """PeekableQueue data-structure Tests"""
    # Variables for Queue length.
    Q_EMPTY = 0
    Q_FULL = 5
    # Test data list length.
    TEST_DATA_LENGTH = 5

    def setUp(self):
        self.ru_obj = RU.PeekableQueue(self.Q_FULL)
        self.test_data = range(self.TEST_DATA_LENGTH)

    def test_enqueue(self):
        """PeekableQueue.enqueue"""
        for item in self.test_data:
            self.ru_obj.enqueue(item)
        # Queue with enqueue operation till full size.
        self.assertEqual(self.ru_obj.items, self.test_data)
        self.ru_obj.enqueue(10)  # random number.
        extra_element_test_data = self.test_data + [10]  # random number.
        # Queue with enqueue operation after full size.
        self.assertNotEqual(self.ru_obj.items, extra_element_test_data)
        self.assertEqual(self.ru_obj.items, extra_element_test_data[1:])

    def test_dequeue(self):
        """PeekableQueue.dequeue"""
        # Empty Queue
        self.assertIsNone(self.ru_obj.dequeue())
        for item in self.test_data:
            self.ru_obj.enqueue(item)
        for item in self.test_data:
            # Dequeue operation from a full queue.
            self.assertIs(self.ru_obj.dequeue(), item)
        return

    def test_get_avg(self):
        """PeekableQueue.get_avg"""
        # Empty Queue
        self.assertRaises(ZeroDivisionError, self.ru_obj.get_avg)
        self.ru_obj.enqueue(1)  # random number.
        self.assertEqual(self.ru_obj.get_avg(), 1.0)
        self.ru_obj.enqueue(2.5)  # random number.
        self.assertEqual(self.ru_obj.get_avg(), 1.75)
        self.ru_obj.enqueue(3.5)  # random number.
        self.assertEqual(self.ru_obj.get_avg(), 2.33)
        self.assertEqual(self.ru_obj.get_avg(3), 2.333)

    def test_is_full(self):
        """PeekableQueue.is_full"""
        # Empty.
        self.assertFalse(self.ru_obj.is_full())
        for item in xrange(self.Q_FULL - 1):
            self.ru_obj.enqueue(item)
        # Queue with less than max capacity.
        self.assertFalse(self.ru_obj.is_full())
        self.ru_obj.enqueue(10)  # random number.
        # Queue with max capacity.
        self.assertTrue(self.ru_obj.is_full())
        self.ru_obj.enqueue(15)  # random number.
        # Queue with an attempt to cross the max capacity.
        self.assertTrue(self.ru_obj.is_full())

    def test_size(self):
        """PeekableQueue.size"""
        # Empty Queue.
        self.assertEqual(self.ru_obj.size(), self.Q_EMPTY)
        for index, item in enumerate(self.test_data):
            self.ru_obj.enqueue(item)
            # Enqueued queue.
            self.assertEqual(self.ru_obj.size(), index + 1)
        # Full Queue.
        self.assertEqual(self.ru_obj.size(), self.Q_FULL)
        count = len(self.test_data)
        while count:
            self.ru_obj.dequeue()
            count -= 1
            # Dequeued queue.
            self.assertEqual(self.ru_obj.size(), count)


class TestRecordUsage(unittest.TestCase):
    """Record Usage Tests"""


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(
        loader.loadTestsFromNames((
            'test_record_usage.TestPeekableQueue',
            'test_record_usage.TestRecordUsage')))

    class CustomResult(unittest.TextTestResult):
        """TextTestResult class to use short description of methods."""
        getDescription = lambda self, test: test.shortDescription() or \
            super(CustomResult, self).getDescription(test)

    unittest.TextTestRunner(verbosity=2, resultclass=CustomResult).run(suite)
