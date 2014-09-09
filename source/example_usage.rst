Example Usage
**********************************
Illustration of using this package to retrieve data through
a Python interactive console.

Data Retrieval
==================================
This example is providing assuming that one is in the 
py-webb-db-utils has been installed as a package. These 
examples show MS Excel 2007 exports being placed at 
C:/Users/joe/downloads/, but can be any appropriate directory.

>>> from webb_utils.retrieve_data import RetrieveData
>>> SCHEMA_NAME = 'my_schema'
>>> PASSWORD = 'my_password'
>>> DB_NAME = 'db.name.blah'
>>> START_DATE = '01-OCT-2006'
>>> END_DATE = '30-SEP-2007'
>>> rd = RetrieveData(SCHEMA_NAME, PASSWORD, DB_NAME)
>>> # get well datums
>>> gwd = rd.get_well_datums(excel_export_path='C:/Users/joe/downloads/well_datums.xlsx') 
>>> # get well uv
>>> gwu = rd.get_well_uvs(START_DATE, END_DATE, 
	excel_export_path='C:/Users/joe/downloads/well_uvs.xlsx')
>>> # get carbon data
>>> gcd = rd.get_carbon_data(START_DATE, END_DATE, 
	excel_export_path='C:/Users/joe/downloads/carbon_data.xlsx')
>>> # get alkalinity
>>> gda = rd.get_data_with_alkalinity(START_DATE, END_DATE, 
	excel_export_path='C:/Users/joe/downloads/data_alk.xlsx')
>>> # get check values
>>> gwcv = rd.get_well_check_values(START_DATE, END_DATE, 
	excel_export_path='C:/Users/joe/downloads/check_values.xlsx')
>>> # get piezo sites
>>> gps = rd.get_piezo_sites(START_DATE, END_DATE, 
	excel_export_path='C:/Users/joe/downloads/piezo_sites.xlsx')
>>> # get site information
>>> sites = rd.get_site_info(excel_export_path='C:/Users/joe/downloads/site_info.xlsx')
>>> # close the session
>>> rd.close_session()

Data Entry
==================================