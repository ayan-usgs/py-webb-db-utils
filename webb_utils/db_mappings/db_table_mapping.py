'''
Created on Sep 9, 2014

@author: ayan
'''
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Float, Date, CHAR, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Anion(Base):
    
    __tablename__ = u'ANION'
    
    record_number = Column(Float, ForeignKey(u'sample.record_number'), primary_key=True, nullable=False)
    analyzing_lab = Column(String, ForeignKey(u'lab.analyzing_lab'), primary_key=True, nullable=False)
    cl = Column(Float)
    no3 = Column(Float)
    so4 = Column(Float)
    flagcl = Column(CHAR)
    flagno3 = Column(CHAR)
    flagso4 = Column(CHAR)
    alkalinity_source = Column(String)
    alkalinity = Column(Float)


class Cation(Base):
    
    __tablename__ = u'CATION'
    
    record_number = Column(Float, ForeignKey(u'sample.record_number'), primary_key=True, nullable=False)
    analyzing_lab = Column(String, ForeignKey(u'lab.analyzing_lab'), primary_key=True, nullable=False)
    na = Column(Float)
    mg = Column(Float)
    si = Column(Float)
    k = Column(Float)
    ca = Column(Float)
    mn = Column(Float)
    fe = Column(Float)
    sr = Column(Float)
    flagna = Column(CHAR)
    flagmg = Column(CHAR)
    flagsi = Column(CHAR)
    flagk = Column(CHAR)
    flagca = Column(CHAR)
    flagmn = Column(CHAR)
    flagfe = Column(CHAR)
    flagsr = Column(CHAR)
    
    
class Carbon(Base):
    
    __tablename__ = u'CARBON'
    
    record_number = Column(Float, ForeignKey(u'sample.record_number'), nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(u'lab.analyzing_lab'), nullable=False, primary_key=True)
    tic = Column(Float)
    toc = Column(Float)
    uva_254 = Column(Float)
    uva_280 = Column(Float)
    flagtic = Column(CHAR)
    flagtoc = Column(CHAR)
    flaguva_254 = Column(CHAR)
    flaguva_280 = Column(CHAR)
    
    
class CarbonGas(Base):
    
    __tablename__ = u'CARBON_GAS'
    
    record_number = Column(Float, ForeignKey(u'sample.record_number'), nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(u'lab.analyzing_lab'), nullable=False, primary_key=True)
    ch4 = Column(Float)
    co2 = Column(Float)
    flagch4 = Column(CHAR)
    flagco2 = Column(CHAR)
    

class DVResults(Base):
    
    __tablename__ = u'DV_RESULTS'
    
    station_no = Column(String, ForeignKey(u'site.station_no'), nullable=False, primary_key=True)
    parameter_code = Column(String, ForeignKey(u'parameters.parameter_code'), nullable=False, primary_key=True)
    result_date = Column(Date, nullable=False, primary_key=True)
    result_value = Column(Float)
    dv_flag = Column(CHAR, ForeignKey(u'dv_flag.flag'))
    
    
class Field(Base):
    
    __tablename__ = u'FIELD'
    
    record_number = Column(Float, ForeignKey(u'sample.record_number'), nullable=False, primary_key=True)
    gage_height = Column(Float)
    fldcond = Column(Float)
    fldph = Column(Float)
    wtemp = Column(Float)
    atemp = Column(Float)
    o2 = Column(Float)
    weather = Column(String)
    sulfide = Column(Float)
    redox = Column(Float)
    particulates = Column(Float)
    
    
class FluxChamber(Base):
    
    __tablename__ = u'FLUX_CHAMBER'
    
    station_no = Column(String, ForeignKey(u'site.station_no'), nullable=False, primary_key=True)
    meas_date = Column(Date, nullable=False, primary_key=True)
    meas_minute = Column(Float, nullable=False)
    co2_light = Column(Float)
    co2_dark = Column(Float)
    remark = Column(String)
    
    
class GageHtMeas(Base):
    
    __tablename__ = u'GAGE_HT_MEAS'
    
    station_no = Column(String, ForeignKey(u'site.station_no'), nullable=False, primary_key=True)
    meas_date = Column(Date, nullable=False, primary_key=True)
    ht_above_rp = Column(Float)
    local_ws_elev = Column(Float)
    ngvd_ws_elev = Column(Float)
    data_source = Column(String)
    
    
class GageHtRp(Base):
    
    __tablename__ = u'GAGE_HT_RP'
    __table_args__ = (
                      ForeignKeyConstraint(['station_no', 'rp_id'], ['rp_desc.station_no', 'rp_desc.rp_id']),
                      )
    
    station_no = Column(String, ForeignKey(u'site.station_no'), nullable=False, primary_key=True)
    rp_id = Column(String, nullable=False, primary_key=True)
    rp_date = Column(Date, nullable=False)
    rp_valid = Column(String, nullable=False)
    local_rp_elev = Column(Float)
    ngvd_rp_elev = Column(String)
    

class IsotopeStrontium(Base):
    
    __tablename__ = u'ISOTOPE_STRONTIUM'
    
    record_number = Column(Float, ForeignKey(u'sample.record_number'), nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(u'lab.analyzing_lab'), nullable=False)
    sr87_sr86 = Column('SR_87#SR_86', Float)
    sr87 = Column('sr_87', Float)
    flag_sr87_sr86 = Column('FLAGSR_87#SR_86', CHAR) # must be aliased in retrievals as SQLAlchemy default name is too long
    flag_sr87 = Column('flagsr_87', CHAR)


class IsotopeWater(Base):
    
    __tablename__ = u'ISOTOPE_WATER'
    
    record_number = Column(Float, ForeignKey(u'sample.record_number'), nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(u'lab.analyzing_lab'), nullable=False)
    d = Column(Float)
    o_18 = Column(Float)
    flag_d = Column('flagd', CHAR)
    flag_o18 = Column('flago_18', CHAR)
    h_3 = Column(Float)
    sd_h_3 = Column(Float)
    flag_h3 = Column('flagh_3', String)
    lab_id = Column(String)
    
    
class Mercury(Base):
    
    __tablename__ = u'MERCURY'
    
    record_number = Column(Float, ForeignKey(u'sample.record_number'), nullable=False, primary_key=True)
    analyzing_lab = Column(String, nullable=False, primary_key=True)
    analysis_date = Column(Date)
    results_id = Column(Float)
    bottle_id = Column(String)
    parameter = Column(String, nullable=False, primary_key=True)
    ddl = Column(Float)
    d_flag = Column(String)
    value = Column(Float)
    units = Column(String)
    qa_flags = Column(String)
    field_id = Column(Float)
    lab_comment = Column(String)
    

class Nutrient(Base):
    
    __tablename__ = u'NUTRIENT'
    
    record_number = Column(Float, ForeignKey(u'sample.record_number'), nullable=False, primary_key=True)
    filter_type = Column(String)
    analyzing_lab = Column(String, ForeignKey(u'lab.analyzing_lab'), nullable=False, primary_key=False)
    sio2 = Column(Float)
    no3 = Column(Float)
    nh4 = Column(Float)
    nh4orgn = Column(Float)
    n = Column(Float)
    po4 = Column(Float)
    p = Column(Float)
    flagsio2 = Column(String)
    flagno3 = Column(String)
    flagnh4 = Column(String)
    flagnh4orgn = Column(String)
    flagn = Column(String)
    flagpo4 = Column(String)
    flagp = Column(String)
    
    
class Parameters(Base):
    
    __tablename__ = u'PARAMETERS'
    
    parameter_code = Column(String, nullable=False, primary_key=True)
    parameter_short_name = Column(String)
    parameter_code_name = Column(String)
    parameter_name = Column(String, nullable=False)
    constituent_name = Column(String)
    cas_num = Column(String)
    report_units = Column(String)
    record_source = Column(String)
    
    
class QMeas(Base):
    
    __tablename__ = u'QMEAS'
    
    meas_no = Column(String)
    meas_dt = Column(Date, nullable=False, primary_key=False)
    made_by = Column(String)
    width = Column(Float)
    area = Column(Float)
    velocity = Column(Float)
    gage_ht = Column(Float)
    discharge = Column(Float)
    shift_adj = Column(Float)
    pct_diff = Column(Float)
    nu_sect = Column(Float)
    ght_change = Column(Float)
    meas_time = Column(Float)
    meas_rated = Column(String)
    control_cond = Column(String)
    station_no = Column(String, ForeignKey(u'site.station_no'), nullable=False, primary_key=True)
    
    
class RareCation(Base):
    
    __tablename__ = u'RARE_CATION'
    
    record_number = Column(Float, nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(u'lab.analyzing_lab'), nullable=False, primary_key=True)
    li = Column(Float)
    b = Column(Float)
    al = Column(Float)
    rb = Column(Float)
    sr = Column(Float)
    ba = Column(Float)
    pb = Column(Float)
    u = Column(Float)
    flagli = Column(String)
    flagb = Column(String)
    flagal = Column(String)
    flagrb = Column(String)
    flagsr = Column(String)
    flagba = Column(String)
    flagpb = Column(String)
    flagu = Column(String)
    
    
class RawCation(Base):
    
    __tablename__ = u'RAW_CATION'
    
    record_number = Column(Float)
    analyzing_lab = Column(String)
    flagraw_k = Column(CHAR)
    raw_k = Column(Float)
    flagraw_ca = Column(CHAR)
    raw_ca = Column(Float)
    flagraw_mg = Column(CHAR)
    raw_mg = Column(Float)
    flagraw_s = Column(CHAR)
    raw_s = Column(Float)
    flagraw_mn = Column(CHAR)
    raw_mn = Column(Float)
    flagraw_fe = Column(CHAR)
    raw_fe = Column(Float)
    flagraw_na = Column(CHAR)
    raw_na = Column(Float)
    
    
class RPDesc(Base):
    
    __tablename__ = u'RP_DESC'
    
    station_no = Column(String, nullable=False, primary_key=True)
    rp_id = Column(String, nullable=False, primary_key=True)
    rp_desc = Column(String)
    
    
class Sample(Base):
    
    __tablename__ = u'SAMPLE'
    
    station_no = Column(String, ForeignKey(u'site.station_no'), nullable=False, primary_key=True)
    depth = Column(Float, nullable=False, primary_key=True)
    sample_date = Column(DateTime, nullable=False, primary_key=True)
    taken_by = Column(String)
    sampling_method = Column(Float, ForeignKey(u'sample_method.sample_method_cd'), nullable=False)
    sample_type = Column(CHAR, ForeignKey(u'sample_type.sample_type_cd'), nullable=False)
    sample_sequence = Column(Float, nullable=False, primary_key=True)
    record_number = Column(Float, nullable=False)
    field_id = Column(String)
    composite_end_date = Column(Date)
    
    
class SampleGroup(Base):
    
    __tablename__ = u'SAMPLE_GROUP'
    
    group_type = Column(String, nullable=False)
    group_date = Column(String, nullable=False)
    group_sort = Column(Float, nullable=False)
    record_number = Column(Float, nullable=False, primary_key=True)
    
    
class Site(Base):
    
    __tablename__ = u'SITE'
    
    station_no = Column(String, nullable=False, primary_key=True)
    depth = Column(Float, nullable=False)
    station_name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    nest= Column(String, nullable=False)
    site_type_cd = Column(String, ForeignKey(u'site_type.site_type_cd'), nullable=False)
    site_group_cd = Column(String, ForeignKey(u'site_group.site_group_cd'), nullable=False)
    aquifer = Column(String)
    county_code = Column(Float, nullable=False)
    county_name = Column(String, nullable=False)
    hyd_unit = Column(CHAR, nullable=False)
    distance = Column(Float)
    elevation = Column(Float)
    length = Column(Float)
    nwis_station_no = Column(String)
    dec_latitude = Column(Numeric)
    dec_longitude = Column(Numeric)
    
    
class TestSite(Base):
    
    __tablename__ = u'TEST_SITE'
    
    station_no = Column(String, nullable=False)
    nwis_station_no = Column(String)
    depth = Column(Float, nullable=False)
    station_name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    nest_name = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    x_wtm = Column(Float)
    y_wtm = Column(Float)
    site_type_cd = Column(String)
    site_group_cd = Column(String)
    aquifer = Column(String)
    county_code = Column(Float, nullable=False)
    county_name = Column(String, nullable=False)
    hyd_unit = Column(CHAR, nullable=False)
    distance = Column(Float)
    elevation = Column(Float)
    length = Column(Float)
    
    
class UVResults(Base):
    
    __tablename__ = u'UV_RESULTS'
    
    station_no = Column(String, nullable=False, primary_key=True)
    parameter_code = Column(String, nullable=False, primary_key=True)
    result_datetime = Column(DateTime, nullable=False, primary_key=True)
    edited_value = Column(Float, nullable=False)
    computed_value = Column(Float)
    
    
class WellHeadMeas(Base):
    
    __tablename__ = u'WELL_HEAD_MEAS'
    
    station_no = Column(String, ForeignKey(u'site.station_no'), nullable=False, primary_key=True)
    depth = Column(Float, nullable=False, primary_key=True)
    meas_date = Column(Date, nullable=False, primary_key=True)
    depth_to_ws = Column(Float)
    ws_elev = Column(Float)
    ngvd_ws_elev = Column(Float)
    
    
class WellHeadMp(Base):
    
    __tablename__ = u'WELL_HEAD_MP'
    
    station_no = Column(String, ForeignKey(u'site.station_no'), nullable=False, primary_key=True)
    mp_date = Column(Date, nullable=False, primary_key=True)
    mp_valid = Column(String, nullable=False)
    mp_desc = Column(String)
    local_mp_elev = Column(Float)
    ngvd_mp_elev = Column(Float)
    
    
class WwwSites(Base):
    
    __tablename__ = u'WWW_SITES'
    
    station = Column(String)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    latitude = Column(CHAR, nullable=False)
    longitude = Column(CHAR, nullable=False)
    elevation = Column(Float)
    depth = Column(Float)
    state = Column(CHAR, nullable=False)
    county = Column(String, nullable=False)
    watershed = Column(String, nullable=False)