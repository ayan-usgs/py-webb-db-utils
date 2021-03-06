'''
Created on Sep 9, 2014

@author: ayan
'''

#: Expected anion columns and ordering.
ANION_COLUMNS = (
                 'record_number', 'analyzing_lab', 'Cl', 'NO3', 'SO4', 
                 'flagCl', 'flagNO3', 'flagSO4', 'alkalinity_source', 'alkalinity'
                 )


#: Expected bullen columns and ordering.
BULLEN_CATION_COLUMNS = (
                         'record_number', 'analyzing_lab', 'Na', 'Mg', 'Si', 'K', 'Ca', 'Mn', 'Fe', 'Sr',
                          'flagNa','flagMg','flagSi','flagK','flagCa','flagMn','flagFe','flagSr'
                         )


#: Expected carbon columns and ordering.
CARBON_COLUMNS = (
                  'record_number','analyzing_lab','TIC','TOC','UVA_254','UVA_280',
                  'flagTIC','flagTOC','flagUVA_254','flagUVA_280'
                  )


#: Expected carbon gas columns and ordering.
CARBON_GAS_COLUMNS = (
                      'record_number','analyzing_lab','ch4','co2','flagch4','flagco2'
                      )


#: Expected cation columns and ordering.
CATION_COLUMNS = (
                  'record_number','analyzing_lab','Ca','Mg','Na','K','Fe','Mn',
                  'flagCa','flagMg','flagNa','flagK','flagFe','flagMn'
                  )


#: Expected DV result columns and ordering.
DV_RESULTS_COLUMNS = (
                      'station_no', 'parameter_code', 'result_date', 'result_value', 'dv_flag'
                      )

#: Expected field columns and ordering.
FIELD_COLUMNS = (
                 'record_number', 'gage_height', 'fldcond', 'fldph', 'wtemp', 
                 'atemp', 'o2', 'weather', 'sulfide', 'redox', 'particulates'
                 )


#: Expected flux chamber columns and ordering.
FLUX_CHAMBER_COLUMNS = (
                        'station_no', 'meas_date', 'meas_minute', 'co2_light', 'co2_dark', 'remark'
                        )


# meas_time added to support a separate time column from a lab export
#: Expected gage height measurement columns and ordering.
GAGE_HT_MEAS_COLUMNS = (
                        'station_no', 'meas_date', 'meas_time', 'ht_above_rp', 'local_ws_elev', 'ngvd_ws_elev', 'data_source',
                        )


#: Expected gage height rp columns and ordering.
GAGE_HT_RP_COLUMNS = (
                      'station_no', 'rp_id', 'rp_date', 'rp_valid', 'local_rp_elev', 'ngvd_rp_elev'
                      )


#: Expected strontium isotope columns and ordering.
ISOTOPE_STRONTIUM_COLUMNS = (
                             'record_number', 'analyzing_lab', 'Sr_87#Sr_86', 'Sr_87', 'flagSr_87#Sr_86', 'flagSr_87'
                             )


#: Expected water isotope columns and ordering.
ISOTOPE_WATER_COLUMNS = (
                         'record_number', 'analyzing_lab', 'D', 'O_18', 'flagD', 'flagO_18', 'H_3', 'SD_H_3', 'flagH_3', 'lab_id'
                         )


#: Expected mercury columns and ordering.
MERCURY_COLUMNS = (
                   'record_number', 'analyzing_lab', 'analysis_date', 'results_id', 'bottle_id',
                   'parameter', 'ddl', 'd_flag', 'value', 'units', 'qa_flags', 'field_id', 'lab_comment'
                   )

#: Expected nutrient columns and ordering.
NUTRIENT_COLUMNS = (
                    'record_number', 'filter_type', 'analyzing_lab', 'SiO2','NO3','NH4',
                    'NH4orgN','N','PO4','P','flagSiO2','flagNO3','flagNH4','flagNH4orgN',
                    'flagN','flagPO4','flagP' 
                    )

#: Expected parameter columns and ordering.
PARAMETERS_COLUMNS = (
                      'parameter_code','parameter_short_name','parameter_code_name','parameter_name',
                      'constituent_name','cas_num','report_units','record_source'
                      )


#: Expected qmeas columns and ordering.
QMEAS_COLUMNS = (
                 'meas_no', 'meas_dt', 'made_by', 'width', 'area', 'velocity', 'gage_ht', 'discharge', 'shift_adj',
                 'pct_diff', 'nu_sect', 'ght_change', 'meas_time', 'meas_rated', 'control_cond', 'station_no'
                 )


#: Expected rare cation columns and ordering.
RARE_CATION_COLUMNS = (
                       'record_number', 'analyzing_lab', 'Li', 'B', 'Al', 'Rb', 'Sr', 'Ba', 'Pb', 'U', 
                       'flagLi', 'flagB', 'flagAl', 'flagRb', 'flagSr', 'flagBa', 'flagPb', 'flagU'
                       )


#: Expected raw cation columns and ordering.
RAW_CATION_COLUMNS = (
                      'record_number','analyzing_lab','flagraw_K','raw_K','flagraw_Ca','raw_Ca',
                      'flagraw_Mg','raw_Mg','flagraw_S', 'raw_S', 'flagraw_Mn', 'raw_Mn', 
                      'flagraw_Fe', 'raw_Fe','flagraw_Na', 'raw_Na'
                      )

#: Expected RP description columns and ordering.
RP_DESC_COLUMNS = (
                   'station_no', 'rp_id', 'rp_desc'
                   )


#: Expected sample columns and ordering.
SAMPLE_COLUMNS = (
                  'station_no','depth','sample_date', 'sample_time','taken_by','sampling_method','sample_medium',
                  'sample_type','sample_sequence','record_number','field_id','composite_end_date'
                  )


#: Expected sample group columns and ordering.
SAMPLE_GROUP_COLUMNS = (
                        'group_type', 'group_date', 'group_sort', 'record_number'
                        )


#: Expected site columns and ordering.
SITE_COLUMNS = (
                'station_no', 'depth', 'station_name', 'short_name', 'latitude', 'longitude', 'nest',
                'site_type_cd', 'site_group_cd', 'aquifer', 'county_code', 'county_name', 'hyd_unit',
                'distance', 'elevation', 'length', 'nwis_station_no', 'dec_latitude', 'dec_longitude'
                )


# constants are specified in this control file
#: Expected soil profile columns and ordering.
SOIL_PROFILE_COLUMNS = (
                        'station_no', 'depth', 'sample_date', 'sample_time', 'taken_by', 'sampling_method', 
                        'sample_medium', 'sample_type', 'sample_sequence', 'record_number'
                        )


#: Expected test site columns and ordering.
TEST_SITE_COLUMNS = (
                     'station_no', 'nwis_station_no', 'depth', 'station_name', 'short_name', 'nest_name', 'latitude', 'longitude',
                     'x_wtm', 'y_wtm', 'site_type_cd', 'site_group_cd', 'aquifer', 'county_code', 'county_name', 'hyd_unit',
                     'distance', 'elevation', 'length'
                     )


#: Expected UV result columns and ordering.
UV_RESULTS_COLUMNS = (
                      'station_no', 'parameter_code', 'result_date', 'result_time', 'edited_value', 'computed_value'
                      )

#: Expected well head measurement columns and ordering.
WELL_HEAD_MEAS_COLUMNS = (
                          'station_no', 'depth', 'meas_date', 'depth_to_ws', 'ws_elev', 'ngvd_ws_elev'
                          )


#: Expected well head mp columns and ordering.
WELL_HEAD_MP_COLUMNS = (
                        'station_no', 'mp_date', 'mp_valid', 'mp_desc', 'local_mp_elev', 'ngvd_mp_elev'
                        )


#: Expected WI State Hygiene Lab anion result columns and ordering.
WSLH_ANION_COLUMNS = (
                      'record_number', 'analyzing_lab', 'flagCl', 'Cl', 'flagNO3', 'NO3', 'flagSO4', 'SO4'
                      )


#: Expected WI State Hygiene Lab cation result columns and ordering.
WSLH_CATION_COLUMNS = (
                       'record_number', 'analyzing_lab', 'Ca', 'Mg', 'Na', 'K', 'Fe', 'Mn', 
                       'flagCa', 'flagMg', 'flagNa', 'flagK', 'flagFe', 'flagMn'
                       )

#: Expected WWW site result columns and ordering.
WWW_SITES_COLUMNS = (
                     'station', 'name', 'short_name', 'latitude', 'longitude', 'elevation', 'depth', 'state', 'county', 'watershed'
                     )