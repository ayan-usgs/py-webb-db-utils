'''
Created on Sep 9, 2014

@author: ayan
'''
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from upload_columns import ANION_COLUMNS
from ..db_utils import AlchemDB


meta = MetaData()
Base = declarative_base()


anion = Table('ANION', meta, autoload=True)


class Anion(Base):
    
    __table__ = anion
    __mapper_args__ = {
                       'include_properties': list(ANION_COLUMNS)
                       }