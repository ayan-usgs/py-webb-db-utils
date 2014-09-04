'''
Created on Aug 27, 2014

@author: ayan
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_db_filter_str(param_list):
    quoted_list = ["'{0}'".format(param) for param in param_list]
    filter_str = ','.join(quoted_list)
    return filter_str


class AlchemDB(object): 
    
    def __init__(self, schema, password, db_name):
        
        self.connect = 'oracle+cx_oracle://%s:%s@%s' % (schema, password, db_name)
        self.engine = create_engine(self.connect)
               
    def create_session(self):
        
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        session = Session()
        
        return session