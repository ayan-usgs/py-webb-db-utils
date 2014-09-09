'''
Created on Sep 9, 2014

@author: ayan
'''
from datetime import datetime
from pandas.io.parsers import read_csv 
from db_utils import AlchemDB
from db_mappings.db_table_mapping import anion
from db_mappings.upload_columns import ANION_COLUMNS


def string_to_datetime(series, date_col, time_col):
    date_str = series[date_col]
    time_str = series[time_col]
    datetime_str = '{date} {time}'.format(date=date_str, time=time_str)
    try:
        datetime_obj = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    except ValueError:
        datetime_obj = datetime_str
    return datetime_obj


def clean_string_elements(element):
    try:
        int_str = element.decode('utf-8-sig')
        unicode_str = int_str.encode('utf-8')
    except AttributeError:
        unicode_str = element
    return unicode_str


class UploadData(object):
    
    def __init__(self, schema, password, db_name):
        self.acdb = AlchemDB(schema, password, db_name)
        self.session = self.acdb.create_session()

    def _dataframe_from_csv(self, csv_pathname, columns, sep='\t', engine='python', 
                            header=None, parse_dates=False, date_parser=None, date_col=None, time_col=None):
        raw_df = read_csv(filepath_or_buffer=csv_pathname, sep=sep, index_col=None, engine=engine, header=header, 
                          names=columns, parse_dates=parse_dates, date_parser=date_parser)
        if date_col and time_col:
            raw_df['datetime'] = raw_df.apply(string_to_datetime, axis=1, date_col=date_col, time_col=time_col)
            raw_df_str_clean = raw_df.applymap(clean_string_elements)
            df_columns = ['datetime'] + [column_name for column_name in columns if column_name not in (date_col, time_col)]
            final_df = raw_df_str_clean[df_columns]
        else:
            final_df = raw_df
        
        return final_df
    
    def _dataframe_to_records(self, dataframe):
        df_records = dataframe.to_dict('records')
        return df_records
        
    def close_session(self):
        
        self.session.close()
        
        return 'Session closed'
    
    def load_anion_data(self, csv_pathname):
        columns = ANION_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        