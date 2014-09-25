'''
Created on Sep 9, 2014

@author: ayan
'''
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from datetime import datetime
from ..upload_data import string_to_datetime, pad_string, str_to_date


class TestStringToDatetime(unittest.TestCase):
    
    def setUp(self):
        self.date_str = '07/28/08 18:00:00'
        self.t1 = ('07/28/08', '18:00:00')
        self.t2 = ('07/29/09', '03:50:00')
        self.columns = ('date', 'time')
        
    def test_string_to_datetime(self):
        df = pd.DataFrame([self.t1, self.t2], columns=self.columns)
        df['datetime'] = df.apply(string_to_datetime, axis=1, date_col='date', time_col='time')
        datetime_1 = datetime(2008, 7, 28, 18, 0, 0)
        datetime_2 = datetime(2009, 7, 29, 3, 50, 0)
        expected_row_1 = self.t1 + (datetime_1,)
        expected_row_2 = self.t2 + (datetime_2,)
        expected_dataframe = pd.DataFrame([expected_row_1, expected_row_2], columns=('date', 'time', 'datetime'))
        df_equals = assert_frame_equal(df, expected_dataframe)
        self.assertIsNone(df_equals)
        
        
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