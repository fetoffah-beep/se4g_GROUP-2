# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 14:01:52 2020

@author: sahar
"""


from geoalchemy2 import Geometry
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/SE4G')
df=pd.read_csv(r'C:\Users\sahar\Documents\GitHub\se4g_GROUP-2\GISProject_Group4\GISProject_Data\Enhanced_PLOS.CSV')
df.to_sql('Enhanced_PLOS', engine, if_exists = 'replace', index=False)
df_sql= pd.read_sql_table('Enhanced_PLOS',engine)
