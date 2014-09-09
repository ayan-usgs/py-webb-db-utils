'''
Created on Sep 9, 2014

@author: ayan
'''

ANION_COLUMNS = (
                 'record_number', 'analyzing_lab', 'Cl', 'NO3', 'SO4', 
                 'flagCl', 'flagNO3', 'flagSO4', 'alkalinity_source', 'alkalinity'
                 )


BULLEN_CATION_COLUMNS = (
                         'record_number', 'analyzing_lab', 'Na', 'Mg', 'Si', 'K', 'Ca', 'Mn', 'Fe', 'Sr',
                          'flagNa','flagMg','flagSi','flagK','flagCa','flagMn','flagFe','flagSr'
                         )


CARBON_COLUMNS = (
                  'record_number','analyzing_lab','TIC','TOC','UVA_254','UVA_280',
                  'flagTIC','flagTOC','flagUVA_254','flagUVA_280'
                  )


CARBON_GAS_COLUMNS = (
                      'record_number','analyzing_lab','ch4','co2','flagch4','flagco2'
                      )


CATION_COLUMNS = (
                  'record_number','analyzing_lab','Ca','Mg','Na','K','Fe','Mn',
                  'flagCa','flagMg','flagNa','flagK','flagFe','flagMn'
                  )


DV_RESULTS_COLUMNS = (
                      'station_no', 'parameter_code', 'result_date', 'result_value', 'dv_flag'
                      )


FIELD_COLUMNS = (
                 
                 )