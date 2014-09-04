'''
Created on Sep 4, 2014

@author: ayan
'''
import unittest
from ..db_utils import create_db_filter_str


class TestCreateDBFilterStr(unittest.TestCase):

    def setUp(self):
        self.test_tuple = ('apple', 'pear', 'watermelon')
        self.test_list = ['durian', 'mango', 'honeydew']
        
    def test_db_filter_str_with_tuple(self):
        db_filter_str = create_db_filter_str(self.test_tuple)
        expected = "'apple','pear','watermelon'"
        self.assertEqual(db_filter_str, expected)
        
    def test_db_filter_str_with_list(self):
        db_filter_str = create_db_filter_str(self.test_list)
        expected = "'durian','mango','honeydew'"
        self.assertEqual(db_filter_str, expected)