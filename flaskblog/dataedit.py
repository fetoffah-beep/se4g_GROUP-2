import pandas as pd
import geopandas as gpd
import numpy as np


# csv file from epicollect5
raw_data = pd.read_csv(r"C:\Users\arlia\Documents\Python Scripts\form-1__plos.csv")

# renaming the data
col_rename = {'ec5_uuid': 'Epicollect5_ID',
              'created_at': 'Date_Created',
              'uploaded_at': 'Date_Uploaded',
              'title': 'Title',
              'lat_1_Coordinates': 'Latitude_Coordinates', 
              'long_1_Coordinates': 'Longitude_Coordinates', 
              'accuracy_1_Coordinates': 'Accuracy', 
              'UTM_Northing_1_Coordinates': 'UTM_Northing', 
              'UTM_Easting_1_Coordinates': 'UTM_Easting', 
              'UTM_Zone_1_Coordinates': 'UTM_Zone', 
              '2_Data_Type': 'Data_Type', 
              '3_Value': 'Values', 
              '4_Take_a_note_if_hel': 'Notes', 
              '5_Take_a_picture_if_': 'Pictures'}
data = raw_data.rename(columns=col_rename)

# deleting nan value from data
data = data.dropna(subset=['Latitude_Coordinates', 'Longitude_Coordinates', 'Accuracy', 'UTM_Northing', 'UTM_Easting'])

# converting data to geodataframe and set the crs
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(np.array(data['UTM_Easting']), np.array(data['UTM_Northing'])))
gdf.crs = 'EPSG:32632'
gdf = gdf.to_crs('EPSG:3857')

df = pd.DataFrame(gdf)

#EPSG:32632
#EPSG:3857
#EPSG:4326

def getPointCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y

# make a copy of geodata for plotting also defining source data to plot
gdf['x'] = gdf.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
gdf['y'] = gdf.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)
cols = ['geometry', 'Epicollect5_ID', 'Date_Created', 'Date_Uploaded', 'Title', 'Accuracy', 'UTM_Zone', 'Notes', 'Pictures'] 
df = pd.DataFrame(gdf)
df = df.drop(cols, axis=1).copy()

def importgdf():
    return gdf

def importdf():
    return df

# separate each data type to different dataframe

def dftype():
    df_type = []
    for i in range(len(df['Data_Type'].unique())):
        df_type.append(pd.DataFrame(df.loc[df['Data_Type'].isin([df['Data_Type'].unique()[i]])]))

    df_curbramps = df_type[0].reset_index(drop=True)
    df_lighting = df_type[1].reset_index(drop=True)
    df_sidewalk = df_type[2].reset_index(drop=True)
    df_parking = df_type[3].reset_index(drop=True)
    df_buffer = df_type[4].reset_index(drop=True)
    df_bikenshoulder = df_type[5].reset_index(drop=True)
    df_numberoflanes = df_type[6].reset_index(drop=True)

    return df_type
