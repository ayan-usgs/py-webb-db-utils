'''
Created on Aug 27, 2014

@author: ayan

.. module:: retrieve_data
    :platform: Unix, Windows, MacOS
    :synopsis: Tools for retrieveing data from an Oracle database.

'''


import pandas as pd
from db_utils import AlchemDB, create_db_filter_str
from base_sql import WELL_DATUMS, WELL_UVS, WITH_DATA, DATA_WITH_UV, WELL_CK_VALUES, PIEZO_SITES, SITE_INFO
from sites import UV_SITES, WELL_CHECK_VALUE_SITES, SITE_GROUPS


class RetrieveData(object):
    
    """
    Retrieve data object to execute and retrieve the results
    of six database queries deemed important to the USGS WEBB
    project.
    
    :param str schema: schema user name
    :param str password: schema user password
    :param str db_name: database name
    :param bool excel_indexes: whether an exported excel file should have Pandas dataframe indexes; default is false
    """
    
    def __init__(self, schema, password, db_name, excel_indexes=False):
        self.acdb = AlchemDB(schema, password, db_name)
        self.session = self.acdb.create_session()
        self.uv_sites = UV_SITES
        self.grps = SITE_GROUPS
        self.well_ck_vals_sites = WELL_CHECK_VALUE_SITES
        self.exind = excel_indexes
    
    def _create_dataframe(self, data, columns):
        """
        Internal method to create a pandas dataframe.
        
        :param data: raw query results
        :type data: list of tuples
        :param columns: dataframe column names
        :type columns: list of strings
        :return: dataframe of query results
        :rtype: pandas.DataFrame
        """
        try:
            df = pd.DataFrame(data, columns=columns)
        except ValueError:
            df = pd.DataFrame(data)
        return df
           
    def close_session(self):
        """
        Close an open Oracle session.
        
        :return: session closed message
        :rtype: string
        """
        
        self.session.close()
        
        return 'Session closed.'
        
    def get_well_datums(self, excel_export_path=None):
        """
        Get well datums. Returns Pandas dataframe, optional excel export.
        
        :param excel_export_path: path for MS Excel 2007 output (e.g. C:/tmp/my_export.xlsx; default None)
        :type excel_export_path: string or None
        :return: query result
        :rtype: pandas.DataFrame
        """
        columns = ['depth', 'short_name', 'station_no', 'local_mp_elev', 'ngvd_mp_elev']
        query_base = self.session.query(*columns)
        result_set = query_base.from_statement(WELL_DATUMS).all()
        df = self._create_dataframe(data=result_set, columns=tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_well_uvs(self, start_date, end_date, sites=None, excel_export_path=None):
        """
        Get well UV data. Returns Pandas dataframe, optional excel export.
        Returns query results for all sites if none are specified.
        
        :param str start_date: start date for database query of form '01-JAN-2005'
        :param str end_date: end date for database query of form '01-JAN-2006'
        :param sites: filter for sites
        :type sites: iterable of strings
        :param excel_export_path: path for MS Excel 2007 output (e.g. C:/tmp/my_export.xlsx; default None)
        :type excel_export_path: string or None
        :return: query result
        :rtype: pandas.DataFrame
        """
        if sites is None:
            selected_sites = create_db_filter_str(self.uv_sites)
        else:
            selected_sites = create_db_filter_str(sites)
        columns = ['result_datetime', 'depth_above_sensor']
        display_columns = ('result_datetime', 'depth_above_sensor (m)')
        query_base = self.session.query(*columns)
        sql_statement = str(WELL_UVS).format(sites=selected_sites)
        result_set = query_base.from_statement(sql_statement).params(EndUVDate=end_date, StartUVDate=start_date).all()
        df = self._create_dataframe(data=result_set, columns=display_columns)
        if excel_export_path:
            df.to_excel(excel_export_path, columns=display_columns, index=self.exind)
        return df
    
    def get_carbon_data(self, start_date, end_date, groups=None, excel_export_path=None):
        """
        Get carbon data. Returns Pandas dataframe, optional excel export.
        Returns results for all site groups if none is specified.
        
        :param str start_date: start date for database query of form '01-JAN-2005'
        :param str end_date: end date for database query of form '01-JAN-2006'
        :param groups: filter for site groups
        :type groups: iterable of strings
        :param excel_export_path: path for MS Excel 2007 output (e.g. C:/tmp/my_export.xlsx; default None)
        :type excel_export_path: string or None
        :return: query result
        :rtype: pandas.DataFrame
        """
        if groups is None:
            selected_grps = create_db_filter_str(self.grps)
        else:
            selected_grps = create_db_filter_str(groups)
        columns = ['station_no', 'short_name', 'record_number', 'sample_date', 'wtemp']
        query_base = self.session.query(*columns)
        sql_statement = str(WITH_DATA).format(groups=selected_grps)
        result_set = query_base.from_statement(sql_statement).params(StartDate=start_date, EndDate=end_date).all()
        df = self._create_dataframe(result_set, columns=tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_data_with_alkalinity(self, start_date, end_date, groups=None, excel_export_path=None):
        """
        Get data with alkalinity. Returns Pandas dataframe, optional excel export.
        Returns results for all site groups if none is specified.
         
        :param str start_date: start date for database query of form '01-JAN-2005'
        :param str end_date: end date for database query of form '01-JAN-2006'
        :param groups: filter for site groups
        :type groups: iterable of strings
        :param excel_export_path: path for MS Excel 2007 output (e.g. C:/tmp/my_export.xlsx; default None)
        :type excel_export_path: string or None
        :return: query result
        :rtype: pandas.DataFrame
        """
        if groups is None:
            selected_grps = create_db_filter_str(self.grps)
        else:
            selected_grps = create_db_filter_str(groups)
        columns = ['station_no', 'short_name', 'sample_date', 'record_number', 'alkalinity']
        query_base = self.session.query(*columns)
        sql_statement = str(DATA_WITH_UV).format(groups=selected_grps)
        result_set = query_base.from_statement(sql_statement).params(StartDate=start_date, EndDate=end_date).all()
        df = self._create_dataframe(result_set, tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_well_check_values(self, start_date, end_date, sites=None, excel_export_path=None):
        """
        Get well check values. Returns Pandas dataframe, optional excel export.
        Returns query results for all sites if none are specified.
        
        :param str start_date: start date for database query of form '01-JAN-2005'
        :param str end_date: end date for database query of form '01-JAN-2006'
        :param sites: filter for sites
        :type sites: iterable of strings
        :param excel_export_path: path for MS Excel 2007 output (e.g. C:/tmp/my_export.xlsx; default None)
        :type excel_export_path: string or None
        :return: query result
        :rtype: pandas.DataFrame
        """
        if sites is None:
            selected_sites = create_db_filter_str(self.well_ck_vals_sites)
        else:
            selected_sites = create_db_filter_str(sites)
        columns = ['short_name', 'meas_date', 'ngvd_ws_elev', 'ws_elev', 'depth_to_ws', 'local_mp_elev', 'ngvd_mp_elev', 'station_no']
        display_columns = ('short_name', 'meas_date', 'ngvd_ws_elev (m)', 'ws_elev', 'depth_to_ws', 'local_mp_elev', 'ngvd_mp_elev', 'station_no')
        query_base = self.session.query(*columns)
        sql_statement = str(WELL_CK_VALUES).format(sites=selected_sites)
        result_set = query_base.from_statement(sql_statement).params(EndDT=end_date, StartDT=start_date).all()
        df = self._create_dataframe(result_set, display_columns)
        if excel_export_path:
            df.to_excel(excel_export_path, columns=display_columns, index=self.exind)
        return df
    
    def get_piezo_sites(self, start_date, end_date, groups=None, excel_export_path=None):
        """
        Get total organic carbon and total inorganic carbon.
        Returns Pandas dataframe, optional excel export.
        Returns results for all site groups if none is specified.
        
        :param str start_date: start date for database query of form '01-JAN-2005'
        :param str end_date: end date for database query of form '01-JAN-2006'
        :param groups: filter for site groups
        :type groups: iterable of strings
        :param excel_export_path: path for MS Excel 2007 output (e.g. C:/tmp/my_export.xlsx; default None)
        :type excel_export_path: string or None
        :return: dataframe
        :rtype: pandas.DataFrame
        """
        if groups is None:
            selected_grps = create_db_filter_str(self.grps)
        else:
            selected_grps = create_db_filter_str(groups)
        columns = ['station_no', 'station_name', 'sample_date', 'record_number', 'tic', 'toc']
        query_base = self.session.query(*columns)
        sql_statement = str(PIEZO_SITES).format(groups=selected_grps)
        result_set = query_base.from_statement(sql_statement).params(StartDate=start_date, EndDate=end_date).all()
        df = self._create_dataframe(result_set, tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df
    
    def get_site_info(self, excel_export_path=None):
        """
        Get site information (lat, lon, NWIS Station number, etc).
        Returns Pandas dataframe, optional excel export.
        
        :param excel_export_path: path for MS Excel 2007 output (e.g. C:/tmp/my_export.xlsx; default None)
        :type excel_export_path: string or None
        :return: query result
        :rtype: pandas.DataFrame
        """
        columns = ['station_no', 'station_name', 'short_name', 'depth', 'latitude', 'longitude', 'dec_latitude', 'dec_longitude', 'nwis_station_no']
        query_base = self.session.query(*columns)
        sql_statement = SITE_INFO
        result_set = query_base.from_statement(sql_statement).all()
        df = self._create_dataframe(result_set, tuple(columns))
        if excel_export_path:
            df.to_excel(excel_export_path, columns=tuple(columns), index=self.exind)
        return df