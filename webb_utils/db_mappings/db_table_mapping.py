'''
Created on Sep 9, 2014

@author: ayan
'''
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Anion(Base):
    
    __table__ = 'ANION'
    
    record_number = Column(Float, asdecimal=False, primary_key=True, nullable=False, ForeignKey(u'sample.record_number'))
    analyzing_lab = Column(String, primary_key=True, ForeignKey(u'lab.analyzing_lab'), nullable=False)
    cl = Column(Float, asdecimal=False)
    no3 = Column(Float, asdecimal=False)
    so4 = Column(Float, asdecimal=False)
    flagcl = Column(String)
    flagno3 = Column(String)
    flagso4 = Column(String)
    alkalinity_source = Column(String)
    alkalinity = Column(Float)
    

class Cation(Base):
    
    __table__ = 'CATION'
    
    record_number = Column(Float, asdecimal=False, nullable=False, ForeignKey(u'sample.record_number'))
    analyzing_lab = Column(String, primary_key=True, ForeignKey(u'lab.analyzing_lab'), nullable=False)
    na = Column(Float, asdecimal=False)
    mg = Column(Float, asdecimal=False)
    