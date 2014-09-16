'''
Created on Sep 9, 2014

@author: ayan
'''
from datetime import datetime
import pandas as pd
from pandas.io.parsers import read_csv
from db_utils import AlchemDB
from db_mappings.db_table_mapping import (Anion, Cation, Carbon, CarbonGas, DVResults, Field, FluxChamber, GageHtMeas,
                                          GageHtRp, IsotopeStrontium, IsotopeWater, Mercury, Nutrient)
from db_mappings.upload_columns import (ANION_COLUMNS, BULLEN_CATION_COLUMNS, CARBON_COLUMNS, CARBON_GAS_COLUMNS, CATION_COLUMNS,
                                        DV_RESULTS_COLUMNS, FIELD_COLUMNS, FLUX_CHAMBER_COLUMNS, GAGE_HT_MEAS_COLUMNS, GAGE_HT_RP_COLUMNS,
                                        ISOTOPE_STRONTIUM_COLUMNS, ISOTOPE_WATER_COLUMNS, MERCURY_COLUMNS, NUTRIENT_COLUMNS)


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
    
    mg_per_liter = 'mg/L'
    ug_per_liter = 'ug/L'
    meq_per_liter = 'meq/L'
    microsiemens_per_cm = 'uS/cm'
    no_unit = 'No Unit'
    o18_unit = 'delta O18/O16'
    d_unit = 'delta D/H'
    
    def __init__(self, schema, password, db_name):
        self.acdb = AlchemDB(schema, password, db_name)
        self.engine = self.acdb.engine
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
        final_df_no_nans = final_df.where((pd.notnull(final_df)), None)
        return final_df_no_nans
    
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
        row_list = []
        for df_record in df_records:
            record_number = int(df_record['record_number'])
            analyzing_lab = df_record['analyzing_lab']
            cl = df_record['Cl']
            no3 = df_record['NO3']
            so4 = df_record['SO4']
            flagcl = df_record['flagCl']
            flagno3 = df_record['flagNO3']
            flagso4 = df_record['flagSO4']
            alkalinity_source = df_record['alkalinity_source']
            alkalinity = df_record['alkalinity']
            if cl:
                cl_unit = self.mg_per_liter
            else:
                cl_unit = None
            if no3:
                no3_unit = self.ug_per_liter
            else:
                no3_unit = None
            if so4:
                so4_unit = self.mg_per_liter
            else:
                so4_unit = None
            if alkalinity:
                alk_unit = self.meq_per_liter
            else:
                alk_unit = None   
            anion_row = Anion(
                              record_number=record_number,
                              analyzing_lab=analyzing_lab,
                              cl=cl,
                              no3=no3,
                              so4=so4,
                              flagcl=flagcl,
                              flagno3=flagno3,
                              flagso4=flagso4,
                              alkalinity_source=alkalinity_source,
                              alkalinity=alkalinity,
                              cl_unit=cl_unit,
                              no3_unit=no3_unit,
                              so4_unit=so4_unit,
                              alk_unit=alk_unit
                              )
            row_list.append(anion_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} anion records'.format(len(row_list))
        return message
    
    def load_bullen_cation_data(self, csv_pathname):
        columns = BULLEN_CATION_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = int(row['record_number'])
            analyzing_lab = row['analyzing_lab']
            na = row['Na']
            mg = row['Mg']
            si = row['Si']
            k = row['K']
            ca = row['Ca']
            mn = row['Mn']
            fe = row['Fe']
            sr = row['Sr']
            flagna = row['flagNa']
            flagmg = row['flagMg']
            flagsi = row['flagSi']
            flagk = row['flagK']
            flagca = row['flagCa']
            flagmn = row['flagMn']
            flagfe = row['flagFe']
            flagsr = row['flagSr']
            if na:
                na_unit = self.mg_per_liter
            else:
                na_unit = None
            if k:
                k_unit = self.mg_per_liter
            else:
                k_unit = None
            if mg:
                mg_unit = self.mg_per_liter
            else:
                mg_unit = None
            if si:
                si_unit = self.mg_per_liter
            else:
                si_unit = None
            if ca:
                ca_unit = self.mg_per_liter
            else:
                ca_unit = None
            if mn:
                mn_unit = self.mg_per_liter
            else:
                mn_unit = None
            if fe:
                fe_unit = self.mg_per_liter
            else:
                fe_unit = None
            if sr:
                sr_unit = self.mg_per_liter
            else:
                sr_unit = None
            cation_row = Cation(
                                record_number=record_number,
                                analyzing_lab=analyzing_lab,
                                na=na,
                                mg=mg,
                                si=si,
                                k=k,
                                ca=ca,
                                mn=mn,
                                fe=fe,
                                sr=sr,
                                flagna=flagna,
                                flagmg=flagmg,
                                flagsi=flagsi,
                                flagk=flagk,
                                flagca=flagca,
                                flagmn=flagmn,
                                flagfe=flagfe,
                                flagsr=flagsr,
                                ca_unit=ca_unit,
                                mg_unit=mg_unit,
                                na_unit=na_unit,
                                k_unit=k_unit,
                                fe_unit=fe_unit,
                                mn_unit=mn_unit,
                                si_unit=si_unit,
                                sr_unit=sr_unit
                                )
            row_list.append(cation_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} bullen cation records'.format(len(row_list))
        return message
    
    def load_carbon_data(self, csv_pathname):
        columns = CARBON_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            tic = row['TIC']
            toc = row['TOC']
            uva_254 = row['UVA_254']
            uva_280 = row['UVA_280']
            flagtic = row['flagTIC']
            flagtoc = row['flagTOC']
            flaguva_254 = row['flagUVA_254']
            flaguva_280 = row['flagUVA_280']
            carbon_row = Carbon(
                                record_number=record_number,
                                analyzing_lab=analyzing_lab,
                                tic=tic,
                                toc=toc,
                                uva_254=uva_254,
                                uva_280=uva_280,
                                flagtic=flagtic,
                                flagtoc=flagtoc,
                                flaguva_254=flaguva_254,
                                flaguva_280=flaguva_280
                                )
            row_list.append(carbon_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} carbon records'.format(len(row_list))
        return message
    
    def load_carbon_gas_data(self, csv_pathname):
        columns = CARBON_GAS_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = int(row['record_number'])
            analyzing_lab = row['analyzing_lab']
            ch4 = row['ch4']
            co2 = row['co2']
            flagch4 = row['flagch4']
            flagco2 = row['flagco2']
            carbon_gas_row = CarbonGas(
                                       record_number=record_number,
                                       analyzing_lab=analyzing_lab,
                                       ch4=ch4,
                                       co2=co2,
                                       flagch4=flagch4,
                                       flagco2=flagco2
                                       )
            row_list.append(carbon_gas_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} carbon gas records'.format(len(row_list))
        return message
    
    def load_cation_data(self, csv_pathname):
        columns = CATION_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []        
        for row in df_records:
            record_number = int(row['record_number'])
            analyzing_lab = row['analyzing_lab']
            ca = row['Ca']
            mg = row['Mg']
            na = row['Na']
            k = row['K']
            fe = row['Fe']
            mn = row['Mn']
            flagca = row['flagCa']
            flagmg = row['flagMg']
            flagna = row['flagNa']
            flagk = row['flagK']
            flagfe = row['flagFe']
            flagmn = row['flagMn']
            if ca:
                ca_unit = self.mg_per_liter
            else:
                ca_unit = None
            if mg:
                mg_unit = self.mg_per_liter
            else:
                mg_unit = None
            if na:
                na_unit = self.mg_per_liter
            else:
                na_unit = None
            if k:
                k_unit = self.mg_per_liter
            else:
                k_unit = None
            if fe:
                fe_unit = self.mg_per_liter
            else:
                fe_unit = None
            if mn:
                mn_unit = self.mg_per_liter
            else:
                mn_unit = None
            cation_row = Cation(
                                record_number=record_number,
                                analyzing_lab=analyzing_lab,
                                ca=ca,
                                mg=mg,
                                na=na,
                                k=k,
                                fe=fe,
                                mn=mn,
                                flagca=flagca,
                                flagmg=flagmg,
                                flagna=flagna,
                                flagk=flagk,
                                flagfe=flagfe,
                                flagmn=flagmn,
                                ca_unit=ca_unit,
                                mg_unit=mg_unit,
                                na_unit=na_unit,
                                k_unit=k_unit,
                                fe_unit=fe_unit,
                                mn_unit=mn_unit
                                )
            row_list.append(cation_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} cation records'.format(len(row_list))
        return message
    
    def load_dv_results_data(self, csv_pathname):
        columns = DV_RESULTS_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            parameter_code = row['parameter_code']
            result_date = row['result_date']
            result_value = row['result_value']
            dv_flag = row['dv_flag']
            dv_results_row = DVResults(
                                       station_no=station_no,
                                       parameter_code=parameter_code,
                                       result_date=result_date,
                                       result_value=result_value,
                                       dv_flag=dv_flag
                                       )
            row_list.append(dv_results_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} DV result records'.format(len(row_list))
        return message
    
    def load_field_data(self, csv_pathname):
        columns = FIELD_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = int(row['record_number'])
            gage_height = row['gage_height']
            fldcond = row['fldcond']
            fldph = row['fldph']
            wtemp = row['wtemp']
            atemp = row['atemp']
            o2 = row['o2']
            weather = row['weather']
            sulfide = row['sulfide']
            redox = row['redox']
            particulates = row['particulates']
            if fldcond:
                fldcond_unit = self.microsiemens_per_cm
            else:
                fldcond_unit = None
            field_row = Field(
                              record_number=record_number,
                              gage_height=gage_height,
                              fldcond=fldcond,
                              fldph=fldph,
                              wtemp=wtemp,
                              atemp=atemp,
                              o2=o2,
                              weather=weather,
                              sulfide=sulfide,
                              redox=redox,
                              particulates=particulates,
                              fldcond_unit=fldcond_unit
                              )
            row_list.append(field_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} field result records'.format(len(row_list))
        return message
    
    def load_flux_chamber_data(self, csv_pathname):
        columns = FLUX_CHAMBER_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            meas_date = row['meas_date']
            meas_minute = row['meas_minute']
            co2_light = row['co2_light']
            co2_dark = row['co2_dark']
            remark = row['remark']
            fc_row = FluxChamber(
                                 station_no=station_no,
                                 meas_date=meas_date,
                                 meas_minute=meas_minute,
                                 co2_light=co2_light,
                                 co2_dark=co2_dark,
                                 remark=remark
                                 )
            row_list.append(fc_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} flux chamber records'.format(len(row_list))
        return message
    
    def load_gage_ht_meas_data(self, csv_pathname):
        columns = GAGE_HT_MEAS_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            meas_date = row['meas_date']
            ht_above_rp = row['ht_above_rp']
            local_ws_elev = row['local_ws_elev']
            ngvd_ws_elev = row['ngvd_ws_elev']
            data_source = row['data_source']
            ghm_row = GageHtMeas(
                                 station_no=station_no,
                                 meas_date=meas_date,
                                 ht_above_rp=ht_above_rp,
                                 local_ws_elev=local_ws_elev,
                                 ngvd_ws_elev=ngvd_ws_elev,
                                 data_source=data_source
                                 )
            row_list.append(ghm_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} gage height measurement records'.format(len(row_list))
        return message
    
    def load_gage_ht_rp_data(self, csv_pathname):
        columns = GAGE_HT_RP_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            rp_id = row['rp_id']
            rp_date = row['rp_date']
            rp_valid = row['rp_valid']
            local_rp_elev = row['local_rp_elev']
            ngvd_rp_elev = row['ngvd_rp_elev']
            ghr_row = GageHtRp(
                               station_no=station_no,
                               rp_id=rp_id,
                               rp_date=rp_date,
                               rp_valid=rp_valid,
                               local_rp_elev=local_rp_elev,
                               ngvd_rp_elev=ngvd_rp_elev,
                               )
            row_list.append(ghr_row)
        self.session.add_all(ghr_row)
        self.session.commit()
        message = 'Loaded {0} gage height RP records'.format(len(row_list))
        return message
    
    def load_strontium_isotope_data(self, csv_pathname):
        columns = ISOTOPE_STRONTIUM_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            sr87_sr86 = row['Sr_87#Sr_86']
            sr87 = row['Sr_87']
            flag_sr87_sr86 = row['flagSr_87#Sr_86']
            flag_sr87 = row['flagSr_87']
            if sr87_sr86:
                sr87_sr86_unit = self.no_unit
            else:
                sr87_sr86_unit = None
            iso_sr_row = IsotopeStrontium(
                                          record_number=record_number,
                                          analyzing_lab=analyzing_lab,
                                          sr87_sr86=sr87_sr86,
                                          sr87=sr87,
                                          flag_sr87_sr86,
                                          flag_sr87=flag_sr87,
                                          sr87_sr86_unit=sr87_sr86_unit
                                          )
            row_list.append(iso_sr_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} strontium isotope records'.format(len(row_list))
        return message
    
    def load_water_isotope_data(self, csv_pathname):
        columns = ISOTOPE_WATER_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            d = row['d']
            o_18 = row['O_18']
            flag_d = row['flagD']
            flag_o18 = row['flagO_18']
            h_3 = row['H_3']
            sd_h_3 = row['SD_H_3']
            flag_h3 = row['flagH_3']
            lab_id = row['lab_id']
            if d:
                d_unit = self.d_unit
            else:
                d_unit = None
            if o_18:
                o18_unit = self.o18_unit
            else:
                o18_unit = None
            iso_water_row = IsotopeWater(
                                         record_number=record_number,
                                         analyzing_lab=analyzing_lab,
                                         d=d,
                                         o_18=o_18,
                                         flag_d=flag_d,
                                         flag_o18=flag_o18,
                                         h_3=h_3,
                                         sd_h_3=sd_h_3,
                                         flag_h3=flag_h3,
                                         lab_id=lab_id,
                                         d_unit=d_unit,
                                         o18_unit=o18_unit
                                         )
            row_list.append(iso_water_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} water isotope records'.format(len(row_list))
        return message
    
    def load_mercury_data(self, csv_pathname):
        columns = MERCURY_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            analysis_date = row['analysis_date']
            results_id = row['results_id']
            bottle_id = row['bottle_id']
            parameter = row['parameter']
            ddl = row['ddl']
            d_flag = row['d_flag']
            value = row['value']
            units = row['units']
            qa_flags = row['qa_flags']
            field_id = row['field_id']
            lab_comment = row['lab_comment']
            mercury_row = Mercury(
                                  record_number=record_number,
                                  analyzing_lab=analyzing_lab,
                                  analysis_date=analysis_date,
                                  results_id=results_id,
                                  bottle_id=bottle_id,
                                  parameter=parameter,
                                  ddl=ddl,
                                  d_flag=d_flag,
                                  value=value,
                                  units=units,
                                  qa_flags=qa_flags,
                                  field_id=field_id,
                                  lab_comment=lab_comment
                                  )
            row_list.append(mercury_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} mercury records'.format(len(row_list))
        return message
    
    def load_nutrient_data(self, csv_pathname):
        columns = NUTRIENT_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            filter_type = row['filter_type']
            analyzing_lab = row['analyzing_lab']
            sio2 = row['SiO2']
            if sio2:
                sio2_unit = self.mg_per_liter
            else:
                sio2_unit = None
            no3 = row['NO3']
            if no3:
                no3_unit = self.ug_per_liter
            else:
                no3_unit = None
            nh4 = row['NH4']
            if nh4:
                nh4_unit = self.ug_per_liter
            else:
                nh4_unit = None
            nh4orgn = row['NH4orgN']
            n = row['N']
            if n:
                n_unit = self.ug_per_liter
            else:
                n_unit = None
            po4 = row['PO4']
            if po4:
                po4_unit = self.mg_per_liter
            else:
                po4_unit = None
            p = row['P']
            if p:
                p_unit = self.ug_per_liter
            else:
                p_unit = None
            flagsio2 = row['flagSiO2']
            flagno3 = row['flagNO3']
            flagnh4 = row['flagNH4']
            flagnh4orgn = row['flagNH4orgN']
            flagn = row['flagN']
            flagpo4 = row['flagPO4']
            flagp = row['flagP']
            nutrient_row = Nutrient(
                                    record_number=record_number,
                                    filter_type=filter_type,
                                    analyzing_lab=analyzing_lab,
                                    sio2 = sio2,
                                    no3=no3,
                                    nh4=nh4,
                                    nh4orgn=nh4orgn,
                                    n=n,
                                    po4=po4,
                                    p=p,
                                    flagsio2=flagsio2,
                                    flagno3=flagno3,
                                    flagnh4=flagnh4,
                                    flagnh4orgn=flagnh4orgn,
                                    flagn=flagn,
                                    flagpo4=flagpo4,
                                    flagp=flagp,
                                    sio2_unit=sio2_unit,
                                    no3_unit=no3_unit,
                                    n_unit=n_unit,
                                    p_unit=p_unit,
                                    po4_unit=po4_unit,
                                    nh4_unit=nh4_unit
                                    )     
            row_list.append(nutrient_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = 'Loaded {0} nutrient records'.format(len(row_list))
        return message