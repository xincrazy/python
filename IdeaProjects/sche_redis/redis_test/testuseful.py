__author__ = 'root'
import unittest
import useful

class testuseful(unittest.TestCase):

    def test_use(self):
        self.assertLess(useful.sum(1,3),5)