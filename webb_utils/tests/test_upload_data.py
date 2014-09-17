'''
Created on Sep 9, 2014

@author: ayan
'''
import unittest
from datetime import datetime
from ..upload_data import string_to_datetime, pad_string, str_to_date


@unittest.skip("This test still needs work.")
class TestStringToDatetime(unittest.TestCase):
    
    def setUp(self):
        self.date_str = '07/28/08 18:00:00'
  
    def test_string_to_datetime(self):
        result_datetime = string_to_datetime(self.date_str)
        expected_datetime = datetime(2008, 7, 28, 18, 0, 0)
        self.assertEqual(result_datetime, expected_datetime)
        
        
class TestPadString(unittest.TestCase):
    
    def setUp(self):
        self.string = '63'
        self.int = 63
        self.long_string = '58904212'
        
    def test_pad_string_with_string(self):
        padded_str = pad_string(self.string, 5, '0')
        expected = '00063'
        self.assertEqual(padded_str, expected)
        
    def test_pad_string_with_number(self):
        padded_str = pad_string(self.int, 5, '0')
        expected = '00063'
        self.assertEqual(padded_str, expected)
        
    def test_pad_string_with_long_string(self):
        padded_str = pad_string(self.long_string, 5, '0')
        expected = self.long_string
        self.assertEqual(padded_str, expected)
        

class TestConvertStringToDate(unittest.TestCase):
    
    def setUp(self):
        self.test_date_str = '09/15/14'
        
    def test_str_to_date(self):
        date_obj = str_to_date(self.test_date_str)
        expected_date = datetime(2014, 9, 15).date()
        self.assertEqual(date_obj, expected_date)