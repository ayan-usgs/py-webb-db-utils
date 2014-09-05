'''
Created on Sep 4, 2014

@author: ayan
'''
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from ..retrieve_data import RetrieveData


class TestRetrieveData(unittest.TestCase):
    
    def setUp(self):
        self.t1 = ('I have 10 apples.', 459.12)
        self.t2 = ('I have 20 oranges.', 843.12)
        self.test_data = [self.t1, self.t2]
        self.pwd = 'fake_pwd'
        self.schema = 'fake_schema'
        self.fake_db = 'fake.db'
        
    def test_create_dataframe(self):
        rd_test = RetrieveData(self.schema, self.pwd, self.fake_db)
        df_test = rd_test._create_dataframe(data=self.test_data, columns=('some_string', 'some_number'))
        expected_df = pd.DataFrame(self.test_data, columns=('some_string', 'some_number'))
        df_equals = assert_frame_equal(df_test, expected_df)
        self.assertIsNone(df_equals)