'''
Created on Sep 9, 2014

@author: ayan
'''
from datetime import datetime
import pandas as pd
from pandas.io.parsers import read_csv
from db_utils import AlchemDB
from db_mappings.db_table_mapping import (Anion, Cation, Carbon, CarbonGas, DVResults, Field, FluxChamber, GageHtMeas,
                                          GageHtRp, IsotopeStrontium, IsotopeWater, Mercury, Nutrient, Parameters, QMeas,
                                          RareCation, RawCation, RPDesc, Sample, SampleGroup, Site, TestSite, UVResults,
                                          WellHeadMeas, WellHeadMp, WwwSites)
from db_mappings.upload_columns import (ANION_COLUMNS, BULLEN_CATION_COLUMNS, CARBON_COLUMNS, CARBON_GAS_COLUMNS, CATION_COLUMNS,
                                        DV_RESULTS_COLUMNS, FIELD_COLUMNS, FLUX_CHAMBER_COLUMNS, GAGE_HT_MEAS_COLUMNS, GAGE_HT_RP_COLUMNS,
                                        ISOTOPE_STRONTIUM_COLUMNS, ISOTOPE_WATER_COLUMNS, MERCURY_COLUMNS, NUTRIENT_COLUMNS, PARAMETERS_COLUMNS,
                                        QMEAS_COLUMNS, RARE_CATION_COLUMNS, RAW_CATION_COLUMNS, RP_DESC_COLUMNS, SAMPLE_COLUMNS,
                                        SAMPLE_GROUP_COLUMNS, SITE_COLUMNS, SOIL_PROFILE_COLUMNS, TEST_SITE_COLUMNS, UV_RESULTS_COLUMNS,
                                        WELL_HEAD_MEAS_COLUMNS, WELL_HEAD_MP_COLUMNS, WSLH_ANION_COLUMNS, WSLH_CATION_COLUMNS, WWW_SITES_COLUMNS)


def string_to_datetime(series, date_col, time_col):
    date_str = series[date_col]
    time_str = series[time_col]
    datetime_str = '{date} {time}'.format(date=date_str, time=time_str)
    try:
        datetime_obj = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    except ValueError:
        datetime_obj = datetime_str
    return datetime_obj


def str_to_date(date_str, time_format='%m/%d/%y'):
    datetime_obj = datetime.strptime(date_str, time_format)
    return datetime_obj.date()


def pad_string(string, total_length=5, padding_element='0'):
    force_string = str(string)
    length_to_pad = 5 - len(force_string)
    if length_to_pad > 0:
        padding_str = padding_element * length_to_pad
        final_str = '{0}{1}'.format(padding_str, force_string)
    else:
        final_str = force_string
    return final_str


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
    return_message = 'Loaded {0} {1} records'
    
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
        print(df_records)
        row_list = []
        for df_record in df_records:
            record_number = df_record['record_number']
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
        message = self.return_message.format(len(row_list), 'anion')
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
                                sr_unit=sr_unit,
                                s_unit=None
                                )
            row_list.append(cation_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'bullen cation')
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
        message = self.return_message.format(len(row_list), 'carbon')
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
        message = self.return_message.format(len(row_list), 'carbon gas')
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
        message = self.return_message.format(len(row_list), 'cation')
        return message
    
    def load_dv_results_data(self, csv_pathname):
        columns = DV_RESULTS_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            parameter_code = pad_string(row['parameter_code'])
            result_date = str_to_date(row['result_date'])
            result_value = row['result_value']
            dv_flag = row['dv_flag']
            if dv_flag:
                dv_flag_val = dv_flag
            else:
                dv_flag_val = ' '
            dv_results_row = DVResults(
                                       station_no=station_no,
                                       parameter_code=parameter_code,
                                       result_date=result_date,
                                       result_value=result_value,
                                       dv_flag=dv_flag_val
                                       )
            row_list.append(dv_results_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'DV result')
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
        message = self.return_message.format(len(row_list), 'field result')
        return message
    
    def load_flux_chamber_data(self, csv_pathname):
        columns = FLUX_CHAMBER_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            meas_date = str_to_date(row['meas_date'])
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
        message = self.return_message.format(len(row_list), 'flux chamber')
        return message
    
    def load_gage_ht_meas_data(self, csv_pathname, date_col, time_col):
        columns = GAGE_HT_MEAS_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns, date_col=date_col, time_col=time_col)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            meas_date = row['datetime']
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
        message = self.return_message.format(len(row_list), 'gage_height_measurement')
        return message
    
    def load_gage_ht_rp_data(self, csv_pathname):
        columns = GAGE_HT_RP_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            rp_id = row['rp_id']
            rp_date = str_to_date(row['rp_date'])
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
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'gage height RP')
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
                                          flag_sr87_sr86=flag_sr87_sr86,
                                          flag_sr87=flag_sr87,
                                          sr87_sr86_unit=sr87_sr86_unit
                                          )
            row_list.append(iso_sr_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'strontium isotope')
        return message
    
    def load_water_isotope_data(self, csv_pathname):
        columns = ISOTOPE_WATER_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            d = row['D']
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
        message = self.return_message.format(len(row_list), 'water isotope')
        return message
    
    def load_mercury_data(self, csv_pathname):
        columns = MERCURY_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            analysis_date = str_to_date(row['analysis_date'])
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
        message = self.return_message.format(len(row_list), 'mercury')
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
        message = self.return_message.format(len(row_list), 'nutrient')
        return message
    
    def load_parameters(self, csv_pathname):
        columns = PARAMETERS_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            parameter_code = pad_string(row['parameter_code'])
            parameter_short_name = row['parameter_short_name']
            parameter_code_name = row['parameter_code_name']
            parameter_name = row['parameter_name']
            constituent_name = row['constituent_name']
            cas_num = row['cas_num']
            report_units = row['report_units']
            record_source = row['record_source']
            parameter_row = Parameters(
                                       parameter_code=parameter_code,
                                       parameter_short_name=parameter_short_name,
                                       parameter_code_name=parameter_code_name,
                                       parameter_name=parameter_name,
                                       constituent_name=constituent_name,
                                       cas_num=cas_num,
                                       report_units=report_units,
                                       record_source=record_source
                                       )
            row_list.append(parameter_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'parameter')
        return message
    
    def load_qmeas_data(self, csv_pathname):
        columns = QMEAS_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            meas_no = row['meas_no']
            meas_dt = str_to_date(row['meas_dt'])
            made_by = row['made_by']
            width = row['width']
            area = row['area']
            velocity = row['velocity']
            gage_ht = row['gage_ht']
            discharge = row['discharge']
            shift_adj = row['shift_adj']
            pct_diff = row['pct_diff']
            nu_sect = row['nu_sect']
            ght_change = row['ght_change']
            meas_time = row['meas_time']
            meas_rated = row['meas_rated']
            control_cond = row['control_cond']
            station_no = row['station_no']
            qmeas_row = QMeas(
                              meas_no=meas_no,
                              meas_dt=meas_dt,
                              made_by=made_by,
                              width=width,
                              area=area,
                              velocity=velocity,
                              gage_ht=gage_ht,
                              discharge=discharge,
                              shift_adj=shift_adj,
                              pct_diff=pct_diff,
                              nu_sect=nu_sect,
                              ght_change=ght_change,
                              meas_time=meas_time,
                              meas_rated=meas_rated,
                              control_cond=control_cond,
                              station_no=station_no
                              )
            row_list.append(qmeas_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'QMEAS')
        return message
    
    def load_rare_cation_data(self, csv_pathname):
        columns = RARE_CATION_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            li = row['Li']
            b = row['B']
            al = row['Al']
            rb = row['Rb']
            sr = row['Sr']
            ba = row['Ba']
            pb = row['Pb']
            u = row['U']
            flagli = row['flagLi']
            flagb = row['flagB']
            flagal = row['flagAl']
            flagrb = row['flagRb']
            flagsr = row['flagSr']
            flagba = row['flagBa']
            flagpb = row['flagPb']
            flagu = row['flagU']
            rare_cation_row = RareCation(
                                         record_number=record_number,
                                         analyzing_lab=analyzing_lab,
                                         li=li,
                                         b=b,
                                         al=al,
                                         rb=rb,
                                         sr=sr,
                                         ba=ba,
                                         pb=pb,
                                         u=u,
                                         flagli=flagli,
                                         flagb=flagb,
                                         flagal=flagal,
                                         flagrb=flagrb,
                                         flagsr=flagsr,
                                         flagba=flagba,
                                         flagpb=flagpb,
                                         flagu=flagu
                                         )
            row_list.append(rare_cation_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'rare cation')
        return message
    
    def load_raw_cation_data(self, csv_pathname):
        columns = RAW_CATION_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            flagraw_k = row['flagraw_K']
            raw_k = row['raw_K']
            flagraw_ca = row['flagraw_Ca']
            raw_ca = row['raw_Ca']
            flagraw_mg = row['flagraw_Mg']
            raw_mg = row['raw_Mg']
            flagraw_s = row['flagraw_S']
            raw_s = row['raw_S']
            flagraw_mn = row['flagraw_Mn']
            raw_mn = row['raw_Mn']
            flagraw_fe = row['flagraw_Fe']
            raw_fe = row['raw_Fe']
            flagraw_na = row['flagraw_Na']
            raw_na = row['raw_Na']
            raw_cation_row = RawCation(
                                       record_number=record_number,
                                       analyzing_lab=analyzing_lab,
                                       flagraw_k=flagraw_k,
                                       raw_k=raw_k,
                                       flagraw_ca=flagraw_ca,
                                       raw_ca=raw_ca,
                                       flagraw_mg=flagraw_mg,
                                       raw_mg=raw_mg,
                                       flagraw_s = flagraw_s,
                                       raw_s=raw_s,
                                       flagraw_mn=flagraw_mn,
                                       raw_mn=raw_mn,
                                       flagraw_fe=flagraw_fe,
                                       raw_fe=raw_fe,
                                       flagraw_na=flagraw_na,
                                       raw_na=raw_na
                                       )
            row_list.append(raw_cation_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'raw cation')
        return message
    
    def load_rp_desc_data(self, csv_pathname):
        columns = RP_DESC_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            rp_id = row['rp_id']
            rp_desc = row['rp_desc']
            rp_desc_row = RPDesc(
                                 station_no=station_no,
                                 rp_id=rp_id,
                                 rp_desc=rp_desc
                                 )
            row_list.append(rp_desc_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'RP description')
        return message
    
    def load_sample_data(self, csv_pathname, date_col, time_col):
        columns = SAMPLE_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns, date_col=date_col, time_col=time_col)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            depth = row['depth']
            sample_date = row['datetime']
            taken_by = row['taken_by']
            sampling_method = row['sampling_method']
            sample_medium = row['sample_medium']
            sample_type = row['sample_type']
            sample_sequence = row['sample_sequence']
            record_number = row['record_number']
            field_id = row['field_id']
            composite_end_date = row['composite_end_date']
            sample_row = Sample(
                                station_no=station_no,
                                depth=depth,
                                sample_date=sample_date,
                                taken_by=taken_by,
                                sampling_method=sampling_method,
                                sample_medium=sample_medium,
                                sample_type=sample_type,
                                sample_sequence=sample_sequence,
                                record_number=record_number,
                                field_id=field_id,
                                composite_end_date=composite_end_date
                                )
            row_list.append(sample_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'sample')
        return message
            
    def load_sample_group_data(self, csv_pathname):
        columns = SAMPLE_GROUP_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            group_type = row['group_type']
            group_date = row['group_date']
            group_sort = row['group_sort']
            record_number = row['record_number']
            sample_grp_row = SampleGroup(
                                         group_type=group_type,
                                         group_date=group_date,
                                         group_sort=group_sort,
                                         record_number=record_number
                                         )        
            row_list.append(sample_grp_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'sample group')
        return message
    
    def load_site_data(self, csv_pathname):
        columns = SITE_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            depth = row['depth']
            station_name = row['station_name']
            short_name = row['short_name']
            latitude = row['latitude']
            longitude = row['longitude']
            nest = row['nest']
            site_type_cd = row['site_type_cd']
            site_group_cd = row['site_group_cd']
            aquifer = row['aquifer']
            county_code = row['county_code']
            county_name = row['county_name']
            hyd_unit = row['hyd_unit']
            distance = row['distance']
            elevation = row['elevation']
            length = row['length']
            nwis_station_no = row['nwis_station_no']
            dec_latitude = row['dec_latitude']
            dec_longitude = row['dec_longitude']
            site_row = Site(
                            station_no=station_no,
                            depth=depth,
                            station_name=station_name,
                            short_name=short_name,
                            latitude=latitude,
                            longitude=longitude,
                            nest=nest,
                            site_type_cd=site_type_cd,
                            site_group_cd=site_group_cd,
                            aquifer=aquifer,
                            county_code=county_code,
                            county_name=county_name,
                            hyd_unit=hyd_unit,
                            distance=distance,
                            elevation=elevation,
                            length=length,
                            nwis_station_no=nwis_station_no,
                            dec_latitude=dec_latitude,
                            dec_longitude=dec_longitude
                            )
            row_list.append(site_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'site')
        return message
    
    def load_soil_profile_data(self, csv_pathname, date_col, time_col):
        columns = SOIL_PROFILE_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns, date_col=date_col, time_col=time_col)
        df_records = self._dataframe_to_records(df)
        print(df_records)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            depth = row['depth']
            sample_date = row['datetime']
            taken_by = row['taken_by']
            if taken_by:
                taken_by_val = taken_by
            else:
                taken_by_val = 'jes'
            sampling_method = row['sampling_method']
            if sampling_method:
                sampling_method_val = sampling_method
            else:
                sampling_method_val = '9999'
            sample_medium = row['sample_medium']
            if sample_medium:
                sample_medium_val = sample_medium
            else:
                sample_medium_val = '0'
            sample_type = row['sample_type']
            if sample_type:
                sample_type_val = sample_type
            else:
                sample_type_val = '9'
            sample_sequence = row['sample_sequence']
            if sample_sequence:
                sample_seq_val = sample_sequence
            else:
                sample_seq_val = 1
            record_number = row['record_number']
            soil_profile_row = Sample(
                                      station_no=station_no,
                                      depth=depth,
                                      sample_date=sample_date,
                                      taken_by=taken_by_val,
                                      sampling_method=sampling_method_val,
                                      sample_medium=sample_medium_val,
                                      sample_type=sample_type_val,
                                      sample_sequence=sample_seq_val,
                                      record_number=record_number
                                      )
            row_list.append(soil_profile_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'soil profile sample')
        return message
    
    def load_test_site_data(self, csv_pathname):
        columns = TEST_SITE_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            nwis_station_no = row['nwis_station_no']
            depth = row['depth']
            station_name = row['station_name']
            short_name = row['short_name']
            nest_name = row['nest_name']
            latitude = row['latitude']
            longitude = row['longitude']
            x_wtm = row['x_wtm']
            y_wtm = row['y_wtm']
            site_type_cd = row['site_type_cd']
            site_group_cd = row['site_group_cd']
            aquifer = row['aquifer']
            county_code = row['county_code']
            county_name = row['county_name']
            hyd_unit = row['hyd_unit']
            distance = row['distance']
            elevation = row['elevation']
            length = row['length']
            test_site_row = TestSite(
                                     station_no=station_no,
                                     nwis_station_no=nwis_station_no,
                                     depth=depth,
                                     station_name=station_name,
                                     short_name=short_name,
                                     nest_name=nest_name,
                                     latitude=latitude,
                                     longitude=longitude,
                                     x_wtm=x_wtm,
                                     y_wtm=y_wtm,
                                     site_type_cd=site_type_cd,
                                     site_group_cd=site_group_cd,
                                     aquifer=aquifer,
                                     county_code=county_code,
                                     county_name=county_name,
                                     hyd_unit=hyd_unit,
                                     distance=distance,
                                     elevation=elevation,
                                     length=length
                                     )
            row_list.append(test_site_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'test site')
        return message
    
    def load_uv_results_data(self, csv_pathname):
        columns = UV_RESULTS_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            parameter_code = row['parameter_code']
            result_datetime = row['result_datetime']
            edited_value = row['edited_value']
            computed_value = row['computed_value']
            uv_result_row = UVResults(
                                      station_no=station_no,
                                      parameter_code=parameter_code,
                                      result_datetime=result_datetime,
                                      edited_value=edited_value,
                                      computed_value=computed_value
                                      )
            row_list.append(uv_result_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'UV result')
        return message
    
    def load_wellhead_measurement_data(self, csv_pathname):
        columns = WELL_HEAD_MEAS_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            depth = row['depth']
            meas_date = row['meas_date']
            depth_to_ws = row['depth_to_ws']
            ws_elev = row['ws_elev']
            ngvd_ws_elev = row['ngvd_ws_elev']
            wellhead_meas_row = WellHeadMeas(
                                             station_no=station_no,
                                             depth=depth,
                                             meas_date=meas_date,
                                             depth_to_ws=depth_to_ws,
                                             ws_elev=ws_elev,
                                             ngvd_ws_elev=ngvd_ws_elev
                                             )
            row_list.append(wellhead_meas_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'wellhead measurement')
        return message
    
    def load_wellhead_mp_data(self, csv_pathname):
        columns = WELL_HEAD_MP_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station_no = row['station_no']
            mp_date = row['mp_date']
            mp_valid = row['mp_valid']
            mp_desc = row['mp_desc']
            local_mp_elev = row['local_mp_elev']
            ngvd_mp_elev = row['ngvd_mp_elev']
            wellhead_mp_row = WellHeadMp(
                                         station_no=station_no,
                                         mp_date=mp_date,
                                         mp_valid=mp_valid,
                                         mp_desc=mp_desc,
                                         local_mp_elev=local_mp_elev,
                                         ngvd_mp_elev=ngvd_mp_elev
                                         )
            row_list.append(wellhead_mp_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'wellhead mp result')
        return message
    
    def load_wslh_anion_data(self, csv_pathname):
        columns = WSLH_ANION_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            flagcl = row['flagCl']
            cl = row['Cl']
            if cl:
                cl_unit = self.mg_per_liter
            else:
                cl_unit = None
            flagno3 = row['flagNO3']
            no3 = row['NO3']
            if no3:
                no3_unit = self.ug_per_liter
            else:
                no3_unit = None
            flagso4 = row['flagSO4']
            so4 = row['SO4']
            if so4:
                so4_unit = self.mg_per_liter
            else:
                so4_unit = None
            whls_anion_row = Anion(
                                   record_number=record_number,
                                   analyzing_lab=analyzing_lab,
                                   flagcl=flagcl,
                                   cl=cl,
                                   flagno3=flagno3,
                                   no3=no3,
                                   flagso4=flagso4,
                                   so4=so4,
                                   cl_unit=cl_unit,
                                   no3_unit=no3_unit,
                                   so4_unit=so4_unit
                                   )
            row_list.append(whls_anion_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'WHLS anion')
        return message
    
    def load_whls_cation_data(self, csv_pathname):
        columns = WSLH_CATION_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            record_number = row['record_number']
            analyzing_lab = row['analyzing_lab']
            ca = row['Ca']
            if ca:
                ca_unit = self.mg_per_liter
            else:
                ca_unit = None
            mg = row['Mg']
            if mg:
                mg_unit = self.mg_per_liter
            else:
                mg_unit = None
            na = row['Na']
            if na:
                na_unit = self.mg_per_liter
            else:
                na_unit = None
            k = row['K']
            if k:
                k_unit = self.mg_per_liter
            else:
                k_unit = None
            fe = row['Fe']
            if fe:
                fe_unit = self.mg_per_liter
            else:
                fe_unit = None
            mn = row['Mn']
            if mn:
                mn_unit = self.mg_per_liter
            else:
                mn_unit = None
            flagca = row['flagCa']
            flagmg = row['flagMg']
            flagna = row['flagNa']
            flagk = row['flagK']
            flagfe = row['flagFe']
            flagmn = row['flagMn']
            wslh_cation_row = Cation(
                                     record_number=record_number,
                                     analyzing_lab=analyzing_lab,
                                     ca=ca,
                                     ca_unit=ca_unit,
                                     mg=mg,
                                     mg_unit=mg_unit,
                                     na=na,
                                     na_unit=na_unit,
                                     k=k,
                                     k_unit=k_unit,
                                     fe=fe,
                                     fe_unit=fe_unit,
                                     mn=mn,
                                     mn_unit=mn_unit,
                                     flagca=flagca,
                                     flagmg=flagmg,
                                     flagna=flagna,
                                     flagk=flagk,
                                     flagfe=flagfe,
                                     flagmn=flagmn
                                     )
            row_list.append(wslh_cation_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'WSLH cation')
        return message  
    
    def load_www_sites_data(self, csv_pathname):
        columns = WWW_SITES_COLUMNS
        df = self._dataframe_from_csv(csv_pathname, columns=columns)
        df_records = self._dataframe_to_records(df)
        row_list = []
        for row in df_records:
            station = row['station']
            name = row['name']
            short_name = row['short_name']
            latitude = row['latitude']
            longitude = row['longitude']
            elevation = row['elevation']
            depth = row['depth']
            state = row['state']
            county = row['county']
            watershed = row['watershed']
            www_sites_row = WwwSites(
                                     station=station,
                                     name=name,
                                     short_name=short_name,
                                     latitude=latitude,
                                     longitude=longitude,
                                     elevation=elevation,
                                     depth=depth,
                                     state=state,
                                     county=county,
                                     watershed=watershed
                                     )
            row_list.append(www_sites_row)
        self.session.add_all(row_list)
        self.session.commit()
        message = self.return_message.format(len(row_list), 'WWW sites')
        return message