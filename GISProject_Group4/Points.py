# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 12:08:14 2020

@author: 39351
"""
import pandas as pd
import geopandas as gpd
import contextily as ctx
from geopandas import GeoDataFrame as gdf
from shapely.geometry import MultiPoint, Point
import plosCalc


collected = pd.read_csv(r"C:\Users\arlia\Documents\Politecnico di Milano\Semester 1\Geographic Information Systems\Project\GISProject_Group4\GISProject_Group4\GISProject_Data\Collected Data.csv") #skiprows=1)
print(collected)

collected.plot(x='long_1_Coordinates', y='lat_1_Coordinates', style='o', legend=False)

position = pd.DataFrame(collected, columns = ['long_1_Coordinates', 'lat_1_Coordinates'])

position_gdf = gpd.GeoDataFrame(position, geometry=gpd.points_from_xy(position['long_1_Coordinates'], position['lat_1_Coordinates']), crs=3857)

position_gdf.plot()
position_gdf.to_file(r'position.shp')


def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis() 
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))


ax = gpd.read_file(r'position.shp').to_crs(epsg=3857)
ax = ax.plot(figsize = (20, 20), alpha = 0.5, marker = 'o', color = 'red', edgecolor = 'k')

add_basemap(ax, zoom = 13)


#Create a column for the PLOS in the dataframe
#collected['PLOS'] = plosCalc(collected.Vm,collected.Nt, collected.Sr, collected.Wv, collected.W1, collected.ppk, collected.Wbuf, collected.fb, collected.WaA, collected.fsw)
