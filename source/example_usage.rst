Example Usage
**********************************
Illustration of using this package to retrieve and upload data 
through a Python interactive console.

Data Retrieval
==================================

Data Retrieval Example
----------------------------------

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

Data Entry Example
----------------------------------

This example demonstrates the use this package to load
data from a CSV into the database. The files for this demonstration
can be found in the example_upload_files directory of this project.

A salient feature to not about the upload files, is that the
order of the columns mirrors the order of the columns specified
in webb_utils.db_mappings.upload_columns. This is important as
it is necessary for this package to parse the CSV file and then 
load the data into the correct database table columns.

Let's say that there is a new sample that needs to be added
to the database. The CSV for this is called "sample_load.csv"
and for demonstration purposes, say this file is 
currently located at 'C:/Users/anna/Documents/sample_load.csv'.
Loading this data via a Python interactive console would proceed as follows:

>>> from webb_utils.upload_data import UploadData
>>> SCHEMA_NAME = 'my_schema'
>>> PASSWORD = 'my_password'
>>> DB_NAME = 'db.name.blah'
>>> ud = UploadData(SCHEMA_NAME, PASSWORD, DB_NAME) # this creates a database session
>>> # load and commit the sample data into the database
>>> sample_upload = ud.load_sample_data('C:/Users/anna/Documents/sample_load.csv')

In addition, loading that sample data, there is also strontium
isotope data that needs to be loaded for the sample. The data file
from the lab is 'anion_load.csv' and that this file has been placed at
'C:/Users/anna/Documents/strontium_load.csv'. This anion data can be loaded
as follows:

>>> # load and commit the anion data into the database
>>> anion_load = ud.load_strontium_isotope_data('C:/Users/anna/Documents/strontium_load.csv') 

If those are the only two things we want to load,
the database session needs to be ended. This can be
done as follows:

>>> ud.close_session()

Data Load Ordering
----------------------------------

The order in which loads are performed is critical to the success
of a particular load. The database has a number of referential and
uniqueness constraints that may cause problems if data is loaded
out of other. In the data load example, the sample data was loaded before
the strontium isotope data because the strontium data references the
sample record number. Hence, loading the strontium data first would have
yield an Oracle error saying that a database constraint had been violated.

Recommended Data Load Order
++++++++++++++++++++++++++++++++++

This is a recommended data load order. Not all steps may apply to 
all loading activities. If something does not apply, skip to the
next item. For example, there may not be a new site to add to the
database, so sample data would be loaded first.

1. Site
2. Sample
3. RP Desc
4. Other (e.g. anion, cation, UV, etc.)

