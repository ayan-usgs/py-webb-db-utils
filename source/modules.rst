Description of Package Modules
**********************************

Base SQL
==================================
Module containing the SQL used in the database queries.
Should the SQL need to be changed, this is the place to
do it.

Sites
==================================
List of sites and site groups. This sites may be changed
if a new site is added to the WEBB project.

Retrieve Data
==================================
Module containing classes for creating objects to
effect data retrieval from an Oracle database.

.. autoclass:: webb_utils.retrieve_data.RetrieveData
	:members: get_well_datums, get_well_uvs, get_carbon_data, get_data_with_alkalinity, get_well_check_values, get_piezo_sites, get_site_info, _create_dataframe
	
DB Utils
==================================
Module containing utilites for database access.

.. autofunction:: webb_utils.db_utils.create_db_filter_str

.. autoclass:: webb_utils.db_utils.AlchemDB
	:members: create_session