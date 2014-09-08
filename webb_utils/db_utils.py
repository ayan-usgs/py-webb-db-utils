'''
Created on Aug 27, 2014

@author: ayan
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_db_filter_str(param_list):
    """
    Create an Oracle safe string from a Python iterable.
    
    :param param_list: list of strings
    :return: Oracle safe string
    :rtype: string
    """
    quoted_list = ["'{0}'".format(param) for param in param_list]
    filter_str = ','.join(quoted_list)
    return filter_str


class AlchemDB(object): 
    """
    Create an Oracle session.
    
    :param str schema: schema user name
    :param str password: schema user password
    :param str db_name: database name
    """
    
    def __init__(self, schema, password, db_name):
        
        self.connect = 'oracle+cx_oracle://%s:%s@%s' % (schema, password, db_name)
        self.engine = create_engine(self.connect)
               
    def create_session(self):
        """
        Create an Oracle session
        
        :return: Oracle database session
        :rtype: sqlalchemy.orm.session.Session
        """
        
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        session = Session()
        
        return session