Description of Package Modules
**********************************

Base SQL
==================================
Module containing the SQL used in the database queries.
Should the SQL need to be changed, this is the place to
do it. This module is located at webb_utils.base_sql.

Sites
==================================
List of sites and site groups. This sites may be changed
if a new site is added to the WEBB project. This module is
located at webb_utils.sites.

Retrieve Data
==================================
Module containing classes for creating objects to
effect data retrieval from an Oracle database. This
module is located at webb_utils.retrieve_data.

.. autoclass:: webb_utils.retrieve_data.RetrieveData
	:members: get_well_datums, get_well_uvs, get_carbon_data, get_data_with_alkalinity, get_well_check_values, get_piezo_sites, get_site_info, _create_dataframe
	
Upload Data
==================================
Module functions and classes to effect the upload
of new data into the data from CSV files provided
by a laboratory. This module is located in
webb_utils.upload_data.

.. autofunction:: webb_utils.upload_data.string_to_datetime

.. autofunction:: webb_utils.upload_data.str_to_date

.. autofunction:: webb_utils.upload_data.clean_string_elements

.. autoclass:: webb_utils.upload_data.UploadData
	:members:
	
DB Utils
==================================
Module containing utilites for database access.

.. autofunction:: webb_utils.db_utils.create_db_filter_str

.. autoclass:: webb_utils.db_utils.AlchemDB
	:members: create_session
	
DB Mappings
==================================
Subpackage containing SQLAlchemy mappings to Oracle tables
and columns pertinent to uploads

Table Mappings
----------------------------------

The webb_utils.db_mapping.db_table_mapping contains mappings to tables 
and table columns for the SQLAlchemy ORM. Any changes to the tables in 
the databases (e.g. new column, removed column, new foreign key etc.) 
will need to be reflected as well. Full documentation for using 
SQLAlchemy object-relational configuration can be found at:
http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html.

.. automodule:: webb_utils.db_mappings.db_table_mapping
	:members:

Upload Columns
----------------------------------

The webb_utils_db_mapping.upload_columns module contains tuples containing
the pertinent data columns in a CSV file to be loaded into the database. 
The columns in the CSV file have the sample ordering as the column names
in the tuples or errors will ensue.

.. automodule:: webb_utils.db_mappings.upload_columns
	:members: