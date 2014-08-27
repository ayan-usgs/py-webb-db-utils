'''
Created on Aug 27, 2014

@author: ayan
'''
import pandas as pd
from db_utils import AlchemDB
from base_sql import WELL_DATUMS


class RetrieveData(object):
    
    def __init__(self, schema, password, db_name):
        self.acdb = AlchemDB(schema=schema, password, db_name)
        self.session = self.acdb.create_session()
        
    def get_well_datums(self):
        pass