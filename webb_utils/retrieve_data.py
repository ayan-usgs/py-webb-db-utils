'''
Created on Aug 27, 2014

@author: ayan
'''
import pandas as pd
from db_utils import AlchemDB
from base_sql import WELL_DATUMS, WELL_UVS, WITH_DATA, DATA_WITH_UV, WELL_CK_VALUES, PIEZO_SITES, SITE_INFO
from local_connect import SCHEMA, PWD, DB

class RetrieveData(object):
    
    def __init__(self, schema, password, db_name, excel_indexes=False):
        self.acdb = AlchemDB(schema, password, db_name)
        self.session = self.acdb.create_session()
        self.uv_sites = ("'North Mid bank well','North Mid streambed well','North Middle','Stevenson Headwaters','Stevenson bank well',"
                         "'Stevenson baro','Stevenson hw bank well','Stevenson hw streambed well','Stevenson streambed well','TS-30 bank well',"
                         "'TS-30 streambed well','Well A1-10WT','Well IS-K106','Well M-05.1','Well M-15.1','Well M-15.2','Well T1-10WT','Well T1-15WT',"
                         "'Well T1-70WT','Well T2-15WT','Well T2-90WT','Well T5-10WT','Well T5-20WT','Well T5-30WT','Well T5-60.80','Well T5-60WT','Well T5-95WT'")
        self.grps = ("'FC_C1','FC_LS','FC_US','FP_IS','FP_LB','FP_T1','FP_T2','FP_T3','FP_T4','FP_T5','G_LYS','HW_LS','HW_MS','HW_US','HYPO','INVERT',"
                     "'LAKE','MISC','PPT','P_LYS','SOILM','S_GAS','S_LYS','TENS','TRIBS'")
        self.well_ck_vals_sites = (
                                   "'North Mid bank well','North Mid streambed well','North Middle','Stevenson Headwaters','Stevenson bank well',"
                                   "'Stevenson baro','Stevenson hw bank well','Stevenson hw streambed well','Stevenson streambed well','TS-30 bank well',"
                                   "'TS-30 streambed well','Well A1-10WT','Well IS-K106','Well M-05.1','Well M-15.1','Well M-15.2','Well T1-10WT',"
                                   "'Well T1-15WT','Well T1-70WT','Well T2-15WT','Well T2-90WT','Well T5-10WT','Well T5-20WT','Well T5-30WT','Well T5-60.80'"
                                   )
        self.exind = excel_indexes
    
    def _create_dataframe(self, data, columns):
        try:
            df = pd.DataFrame(data, columns=columns)
        except ValueError:
            df = pd.DataFrame(data)
        return df
           
    def close_session(self):
        
        self.session.close()
        
        return 'Session closed.'
        
    def get_well_datums(self, excel_export_path=None):
        columns = ['depth', 'short_name', 'station_no', 'local_mp_elev', 'ngvd_mp_elev']
        query_base = self.session.query(*columns)
        result_set = query_base.from_statement(WELL_DATUMS).all()
        df = self._create_dataframe(data=result_set, columns=tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_well_uvs(self, start_date, end_date, sites=None, excel_export_path=None):
        if sites is None:
            selected_sites = self.uv_sites
        else:
            selected_sites = sites
        columns = ['depth_above_sensor', 'result_datetime']
        query_base = self.session.query(*columns)
        sql_statement = str(WELL_UVS).format(sites=selected_sites)
        result_set = query_base.from_statement(sql_statement).params(EndUVDate=end_date, StartUVDate=start_date).all()
        df = self._create_dataframe(data=result_set, columns=tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_carbon_data(self, start_date, end_date, groups=None, excel_export_path=None):
        if groups is None:
            selected_grps = self.grps
        else:
            selected_grps = groups
        columns = ['station_no', 'short_name', 'sample_date', 'wtemp']
        query_base = self.session.query(*columns)
        sql_statement = str(WITH_DATA).format(groups=selected_grps)
        result_set = query_base.from_statement(sql_statement).params(StartDate=start_date, EndDate=end_date).all()
        df = self._create_dataframe(result_set, columns=tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_data_with_uv(self, start_date, end_date, groups=None, excel_export_path=None):
        if groups is None:
            selected_grps = self.grps
        else:
            selected_grps = groups
        columns = ['station_no', 'short_name', 'sample_date', 'record_number', 'alkalinity']
        query_base = self.session.query(*columns)
        sql_statement = str(DATA_WITH_UV).format(groups=selected_grps)
        result_set = query_base.from_statement(sql_statement).params(StartDate=start_date, EndDate=end_date).all()
        df = self._create_dataframe(result_set, tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_well_check_values(self, start_date, end_date, sites=None, excel_export_path=None):
        if sites is None:
            selected_sites = self.well_ck_vals_sites
        else:
            selected_sites = sites
        columns = ['short_name', 'meas_date', 'ngvd_ws_elev', 'ws_elev', 'depth_to_ws', 'local_mp_elev', 'ngvd_mp_elev', 'station_no']
        query_base = self.session.query(*columns)
        sql_statement = str(WELL_CK_VALUES).format(sites=selected_sites)
        result_set = query_base.from_statement(sql_statement).params(EndDT=end_date, StartDT=start_date).all()
        df = self._create_dataframe(result_set, tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_piezo_sites(self, start_date, end_date, groups=None, excel_export_path=None):
        if groups is None:
            selected_grps = self.grps
        else:
            selected_grps = groups
        columns = ['station_no', 'station_name', 'sample_date', 'record_number', 'tic', 'toc']
        query_base = self.session.query(*columns)
        sql_statement = str(PIEZO_SITES).format(groups=selected_grps)
        result_set = query_base.from_statement(sql_statement).params(StartDate=start_date, EndDate=end_date).all()
        df = self._create_dataframe(result_set, tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_site_info(self, excel_export_path=None):
        columns = ['station_no', 'station_name', 'short_name', 'depth', 'latitude', 'longitude', 'dec_latitude', 'dec_longitude', 'nwis_station_no']
        query_base = self.session.query(*columns)
        sql_statement = SITE_INFO
        result_set = query_base.from_statement(sql_statement).all()
        df = self._create_dataframe(result_set, tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
        
    
if __name__ == '__main__':
    
    START_DATE = '01-OCT-2006'
    END_DATE = '30-SEP-2007'
    rd = RetrieveData(SCHEMA, PWD, DB)
    gwd = rd.get_well_datums(excel_export_path='C:\\Users\\ayan\\Desktop\\tmp\\well_datums.xlsx')
    print(gwd)
    gwu = rd.get_well_uvs(START_DATE, END_DATE, excel_export_path='C:\\Users\\ayan\\Desktop\\tmp\\well_uvs.xlsx')
    print(gwu)
    gcd = rd.get_carbon_data(START_DATE, END_DATE, excel_export_path='C:\\Users\\ayan\\Desktop\\tmp\\carbon_data.xlsx')
    print(gcd)
    gdu = rd.get_data_with_uv(START_DATE, END_DATE, excel_export_path='C:\\Users\\ayan\\Desktop\\tmp\\data_uv.xlsx')
    print(gdu)
    gwcv = rd.get_well_check_values(START_DATE, END_DATE, excel_export_path='C:\\Users\\ayan\\Desktop\\tmp\\check_values.xlsx')
    print(gwcv)
    gps = rd.get_piezo_sites(START_DATE, END_DATE, excel_export_path='C:\\Users\\ayan\\Desktop\\tmp\\piezo_sites.xlsx')
    print(gps)
    sites = rd.get_site_info(excel_export_path='C:\\Users\\ayan\\Desktop\\tmp\\site_info.xlsx')
    print(sites)
    rd.close_session()
    