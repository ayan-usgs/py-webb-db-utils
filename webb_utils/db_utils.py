'''
Created on Aug 27, 2014

@author: ayan
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AlchemDB(object): 
    
    def __init__(self, schema, password, db_name):
        
        self.connect = 'oracle+cx_oracle://%s:%s@%s' % (schema, password, db_name)
        self.engine = create_engine(self.connect)
               
    def create_session(self):
        
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        session = Session()
        
        return session