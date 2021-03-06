'''
Created on Sep 9, 2014

@author: ayan
'''
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Float, Date, CHAR, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SampleMethod(Base):
    """
    ORM mapping to the SAMPLE_METHOD table.
    """
    
    __tablename__ = u'SAMPLE_METHOD'
    
    sample_method_cd = Column(Integer, primary_key=True, nullable=False)
    

class SampleMedium(Base):
    """
    ORM mapping to the SAMPLE_MEDIUM table.
    """
    
    __tablename__ = u'SAMPLE_MEDIUM'
    
    sample_medium_cd = Column(String, primary_key=True, nullable=False)
    
    
class SampleType(Base):
    """
    ORM mapping to the SAMPLE_TYPE table.
    """
    
    __tablename__ = u'SAMPLE_TYPE'
    
    sample_type_cd = Column(CHAR, primary_key=True, nullable=False)
    
    
class SiteType(Base):
    """
    ORM mapping to the SITE_TYPE table.
    """
    
    __tablename__ = u'SITE_TYPE'
    
    site_type_cd = Column(CHAR, primary_key=True, nullable=False)
    
    
class SiteGroup(Base):
    """
    ORM mapping to the SITE_GROUP table.
    """
    
    __tablename__ = u'SITE_GROUP'
    
    site_group_cd = Column(String, primary_key=True, nullable=False)
    
    
class Site(Base):
    """
    ORM mapping to the SITE table.
    """    
    __tablename__ = u'SITE'
    
    station_no = Column(String, nullable=False, primary_key=True)
    depth = Column(Float, nullable=False)
    station_name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    nest = Column(String, nullable=False)
    site_type_cd = Column(String, ForeignKey(SiteType.site_type_cd), nullable=False)
    site_group_cd = Column(String, ForeignKey(SiteGroup.site_group_cd), nullable=False)
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


class Sample(Base):
    """
    ORM mapping to the SAMPLE table.
    """
    
    __tablename__ = u'SAMPLE'
    
    station_no = Column(String, ForeignKey(Site.station_no), nullable=False, primary_key=True)
    depth = Column(Float, nullable=False, primary_key=True)
    sample_date = Column(DateTime, nullable=False, primary_key=True)
    taken_by = Column(String)
    sampling_method = Column(Float, ForeignKey(SampleMethod.sample_method_cd), nullable=False)
    sample_medium = Column(String, ForeignKey(SampleMedium.sample_medium_cd), nullable=False)
    sample_type = Column(CHAR, ForeignKey(SampleType.sample_type_cd), nullable=False)
    sample_sequence = Column(Integer, nullable=False, primary_key=True)
    record_number = Column(Integer, nullable=False)
    field_id = Column(String)
    composite_end_date = Column(Date)
    

class Lab(Base):
    """
    ORM mapping to the LAB table.
    """
    
    __tablename__ = u'LAB'
    
    analyzing_lab = Column(String, nullable=False, primary_key=True)


class Parameters(Base):
    """
    ORM mapping to the PARAMETERS table 
    """
    
    __tablename__ = u'PARAMETERS'
    
    parameter_code = Column(String, nullable=False, primary_key=True)
    parameter_short_name = Column(String)
    parameter_code_name = Column(String)
    parameter_name = Column(String, nullable=False)
    constituent_name = Column(String)
    cas_num = Column(String)
    report_units = Column(String)
    record_source = Column(String)
    
    
class RPDesc(Base):
    """
    ORM mapping to the RP_DESC_table.
    """
    
    __tablename__ = u'RP_DESC'
    
    station_no = Column(String, nullable=False, primary_key=True)
    rp_id = Column(String, nullable=False, primary_key=True)
    rp_desc = Column(String)
    

class Anion(Base):
    """
    ORM mapping to the ANION table.
    """
    
    __tablename__ = u'ANION'
    
    record_number = Column(Integer, ForeignKey(Sample.record_number), primary_key=True, nullable=False)
    analyzing_lab = Column(String, ForeignKey(Lab.analyzing_lab), primary_key=True, nullable=False)
    cl = Column(Float)
    no3 = Column(Float)
    so4 = Column(Float)
    flagcl = Column(CHAR)
    flagno3 = Column(CHAR)
    flagso4 = Column(CHAR)
    alkalinity_source = Column(String)
    alkalinity = Column(Float)
    cl_unit = Column(String)
    no3_unit = Column(String)
    so4_unit = Column(String)
    alk_unit = Column(String)


class Cation(Base):
    """
    ORM mapping to the CATION table.
    """
    
    __tablename__ = u'CATION'
    
    record_number = Column(Integer, ForeignKey(Sample.record_number), primary_key=True, nullable=False)
    analyzing_lab = Column(String, ForeignKey(Lab.analyzing_lab), primary_key=True, nullable=False)
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
    ca_unit = Column(String)
    mg_unit = Column(String)
    na_unit = Column(String)
    k_unit = Column(String)
    fe_unit = Column(String)
    mn_unit = Column(String)
    si_unit = Column(String)
    sr_unit = Column(String)
    s_unit = Column(String)
    
    
class Carbon(Base):
    """
    ORM mapping to the CARBON table.
    """
    
    __tablename__ = u'CARBON'
    
    record_number = Column(Integer, ForeignKey(Sample.record_number), nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(Lab.analyzing_lab), nullable=False, primary_key=True)
    tic = Column(Float)
    toc = Column(Float)
    uva_254 = Column(Float)
    uva_280 = Column(Float)
    flagtic = Column(CHAR)
    flagtoc = Column(CHAR)
    flaguva_254 = Column(CHAR)
    flaguva_280 = Column(CHAR)
    
    
class CarbonGas(Base):
    """
    ORM mapping to the CARBON_GAS table.
    """
    
    __tablename__ = u'CARBON_GAS'
    
    record_number = Column(Integer, ForeignKey(Sample.record_number), nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(Lab.analyzing_lab), nullable=False, primary_key=True)
    ch4 = Column(Float)
    co2 = Column(Float)
    flagch4 = Column(CHAR)
    flagco2 = Column(CHAR)
    
    
class DVFlag(Base):
    """
    ORM mapping to the DV_FLAG table.
    """
    
    __tablename__ = u'DV_FLAG'
    
    flag = Column(CHAR, primary_key=True, nullable=False)
    

class DVResults(Base):
    """
    ORM mapping to the DV_RESULTS table.
    """
    
    __tablename__ = u'DV_RESULTS'
    
    station_no = Column(String, ForeignKey(Site.station_no), nullable=False, primary_key=True)
    parameter_code = Column(String, ForeignKey(Parameters.parameter_code), nullable=False, primary_key=True)
    result_date = Column(Date, nullable=False, primary_key=True)
    result_value = Column(Float)
    dv_flag = Column(CHAR, ForeignKey(DVFlag.flag), nullable=True)
    
    
class Field(Base):
    """
    ORM mapping to the FIELD table.
    """
    
    __tablename__ = u'FIELD'
    
    record_number = Column(Integer, ForeignKey(Sample.record_number), nullable=False, primary_key=True)
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
    fldcond_unit = Column(String)
    
    
class FluxChamber(Base):
    """
    ORM mapping to the FLUX_CHAMBER table.
    """
    
    __tablename__ = u'FLUX_CHAMBER'
    
    station_no = Column(String, ForeignKey(Site.station_no), nullable=False, primary_key=True)
    meas_date = Column(Date, nullable=False, primary_key=True)
    meas_minute = Column(Float, nullable=False)
    co2_light = Column(Float)
    co2_dark = Column(Float)
    remark = Column(String)
    
    
class GageHtMeas(Base):
    """
    ORM mapping to the GAGE_HT_MEAS table.
    """
    
    __tablename__ = u'GAGE_HT_MEAS'
    
    station_no = Column(String, ForeignKey(Site.station_no), nullable=False, primary_key=True)
    meas_date = Column(DateTime, nullable=False, primary_key=True)
    ht_above_rp = Column(Float)
    local_ws_elev = Column(Float)
    ngvd_ws_elev = Column(Float)
    data_source = Column(String)
    
    
class GageHtRp(Base):
    """
    ORM mapping to the GAGE_HT_RP table.
    A composite foreign key relationship
    is explicitly define.
    """
    
    __tablename__ = u'GAGE_HT_RP'
    __table_args__ = (
                      ForeignKeyConstraint(['station_no', 'rp_id'], [RPDesc.station_no, RPDesc.rp_id]),
                      )
    
    station_no = Column(String, ForeignKey(Site.station_name), nullable=False, primary_key=True)
    rp_id = Column(String, nullable=False, primary_key=True)
    rp_date = Column(Date, nullable=False)
    rp_valid = Column(String, nullable=False)
    local_rp_elev = Column(Float)
    ngvd_rp_elev = Column(String)
    

class IsotopeStrontium(Base):
    """
    ORM mapping to the ISOTOPE_STRONTIUM table.
    """
    
    __tablename__ = u'ISOTOPE_STRONTIUM'
    
    record_number = Column(Integer, ForeignKey(Sample.record_number), nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(Lab.analyzing_lab), nullable=False)
    sr87_sr86 = Column('SR_87#SR_86', Float)
    sr87 = Column('sr_87', Float)
    flag_sr87_sr86 = Column('FLAGSR_87#SR_86', CHAR) # must be aliased in retrievals as SQLAlchemy default name is too long
    flag_sr87 = Column('flagsr_87', CHAR)
    sr87_sr86_unit = Column('SR_87#SR86_UNIT', String)

class IsotopeWater(Base):
    """
    ORM mapping to the ISOTOPE_WATER table.
    """
    
    __tablename__ = u'ISOTOPE_WATER'
    
    record_number = Column(Integer, ForeignKey(Sample.record_number), nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(Lab.analyzing_lab), nullable=False)
    d = Column(Float)
    o_18 = Column(Float)
    flag_d = Column('flagd', CHAR)
    flag_o18 = Column('flago_18', CHAR)
    h_3 = Column(Float)
    sd_h_3 = Column(Float)
    flag_h3 = Column('flagh_3', String)
    lab_id = Column(String)
    d_unit = Column(String)
    o18_unit = Column(String)
    
    
class Mercury(Base):
    """
    ORM mapping to the MERCURY table.
    """
    
    __tablename__ = u'MERCURY'
    
    record_number = Column(Integer, ForeignKey(Sample.record_number), nullable=False, primary_key=True)
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
    """
    ORM mapping to the NURIENT table.
    """
    __tablename__ = u'NUTRIENT'
    
    record_number = Column(Integer, ForeignKey(Sample.record_number), nullable=False, primary_key=True)
    filter_type = Column(String)
    analyzing_lab = Column(String, ForeignKey(Lab.analyzing_lab), nullable=False, primary_key=False)
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
    sio2_unit = Column(String)
    no3_unit = Column(String)
    n_unit = Column(String)
    p_unit = Column(String)
    po4_unit = Column(String)
    nh4_unit = Column(String)
    
    
class QMeas(Base):
    """
    ORM mapping to QMEAS table.
    """
    
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
    station_no = Column(String, ForeignKey(Site.station_no), nullable=False, primary_key=True)
    
    
class RareCation(Base):
    """
    ORM mapping to the RARE_CATION table.
    """
    
    __tablename__ = u'RARE_CATION'
    
    record_number = Column(Integer, nullable=False, primary_key=True)
    analyzing_lab = Column(String, ForeignKey(Lab.analyzing_lab), nullable=False, primary_key=True)
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
    """
    ORM mapping to the RAW_CATION table.
    """
    
    __tablename__ = u'RAW_CATION'
    
    record_number = Column(Integer, primary_key=True)
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
    
    
class SampleGroup(Base):
    """
    ORM mapping to the SAMPLE_GROUP table.
    """
    
    __tablename__ = u'SAMPLE_GROUP'
    
    group_type = Column(String, nullable=False)
    group_date = Column(String, nullable=False)
    group_sort = Column(Float, nullable=False)
    record_number = Column(Integer, nullable=False, primary_key=True)
    
    
class TestSite(Base):
    """
    ORM mapping to the TEST_SITE table.
    """
    
    __tablename__ = u'TEST_SITE'
    
    station_no = Column(String, nullable=False, primary_key=True)
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
    """
    ORM mapping to the UV_RESULTS table.
    """
    
    __tablename__ = u'UV_RESULTS'
    
    station_no = Column(String, nullable=False, primary_key=True)
    parameter_code = Column(String, nullable=False, primary_key=True)
    result_datetime = Column(DateTime, nullable=False, primary_key=True)
    edited_value = Column(Float, nullable=False)
    computed_value = Column(Float)
    
    
class WellHeadMeas(Base):
    """
    ORM mapping to the WELL_HEAD_MEAS table.
    This table contains a composite foreign
    key.
    """
    
    __tablename__ = u'WELL_HEAD_MEAS'
    __table_args__ = (
                      ForeignKeyConstraint(['station_no', 'depth'], [Site.station_no, Site.depth]),
                      )
    
    station_no = Column(String, nullable=False, primary_key=True)
    depth = Column(Float, nullable=False, primary_key=True)
    meas_date = Column(Date, nullable=False, primary_key=True)
    depth_to_ws = Column(Float)
    ws_elev = Column(Float)
    ngvd_ws_elev = Column(Float)
    
    
class WellHeadMp(Base):
    """
    ORM mapping to the WELL_HEAD_MP table.
    """
    
    __tablename__ = u'WELL_HEAD_MP'
    
    station_no = Column(String, ForeignKey(Site.station_no), nullable=False, primary_key=True)
    mp_date = Column(Date, nullable=False, primary_key=True)
    mp_valid = Column(String, nullable=False)
    mp_desc = Column(String)
    local_mp_elev = Column(Float)
    ngvd_mp_elev = Column(Float)
    
    
class WwwSites(Base):
    """
    ORM mapping to the WWW_SITES table.
    """
    
    __tablename__ = u'WWW_SITES'
    
    station = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    latitude = Column(CHAR, nullable=False)
    longitude = Column(CHAR, nullable=False)
    elevation = Column(Float)
    depth = Column(Float)
    state = Column(CHAR, nullable=False)
    county = Column(String, nullable=False)
    watershed = Column(String, nullable=False)