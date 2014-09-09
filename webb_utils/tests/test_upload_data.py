'''
Created on Sep 9, 2014

@author: ayan
'''
import unittest
from datetime import datetime
from ..upload_data import _string_to_datetime


class TestStringToDatetime(unittest.TestCase):
    
    def setUp(self):
        self.date_str = '07/28/08 18:00:00'
        
    def test_string_to_datetime(self):
        result_datetime = _string_to_datetime(self.date_str)
        expected_datetime = datetime(2008, 7, 28, 18, 0, 0)
        self.assertEqual(result_datetime, expected_datetime)
        
        