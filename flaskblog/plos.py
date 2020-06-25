import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON, get_provider


gdf = gpd.read_file(r"C:\Users\arlia\Documents\Python Scripts\SEGeo\GISProject_Group4\GISProject_Data\Enhanced_PLOS.shp")

tile_provider = get_provider(CARTODBPOSITRON)
plot = figure(title= 'Collected Data', plot_width=500, plot_height=500, 
           x_range=(1020414, 1024954), y_range=(5698497, 5700000), 
           x_axis_type="mercator", y_axis_type="mercator")
