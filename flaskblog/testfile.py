from random import random

import bokeh.io
from bokeh.io import output_notebook, show

from bokeh.layouts import row
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString
from bokeh.io import curdoc
from bokeh.layouts import gridplot, column
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.models import ColumnDataSource, HoverTool, Select, CustomJS
from bokeh.models import BoxSelectTool, BoxZoomTool, LassoSelectTool
from bokeh.transform import factor_cmap, factor_mark


from bokeh.resources import INLINE
bokeh.io.output_notebook(INLINE)

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

def getPointCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y

# make a copy of geodata for plotting also defining source data to plot
gdf['x'] = gdf.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
gdf['y'] = gdf.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)
p_df = gdf.drop('geometry', axis=1).copy()
psource = ColumnDataSource(p_df)

# saving output html file
output_file(r"C:\Users\arlia\Documents\Python Scripts\SEGeo\flaskblog\templates\tile.html")

# defining basemap
tile_provider = get_provider(CARTODBPOSITRON)

# managing the map feature
p = figure(title= 'Observed Data', plot_width=1000, plot_height=400, 
           x_range=(1020414, 1024954), y_range=(5692309, 5698497), 
           x_axis_type="mercator", y_axis_type="mercator", 
           tools='pan, wheel_zoom, box_select, box_zoom, lasso_select, reset')
p.add_tile(tile_provider)

# selection feature for the map
select_overlay = p.select_one(BoxSelectTool).overlay
select_overlay = p.select_one(BoxSelectTool).overlay
select_overlay.fill_color = "firebrick"
select_overlay.line_color = None
zoom_overlay = p.select_one(BoxZoomTool).overlay
zoom_overlay.line_color = "olive"
zoom_overlay.line_width = 8
zoom_overlay.line_dash = "solid"
zoom_overlay.fill_color = None
p.select_one(LassoSelectTool).overlay.line_dash = [10, 10]

# adding pop up message
myhover = HoverTool()
myhover.tooltips = [('Data_Type', '@{Data_Type}'),('X, Y', '@{Longitude_Coordinates}, @{Latitude_Coordinates}')]
p.add_tools(myhover)

# ploting different marker for each data type
datatype = gdf['Data_Type'].unique()
MARKERS = ['hex', 'circle_x', 'triangle', 'diamond', 'inverted_triangle', 'asterisk', 'x']

p.scatter('x', 'y', source=psource, legend_field="Data_Type", fill_alpha=0.4, 
              size=12, marker=factor_mark('Data_Type', MARKERS, datatype),
              color=factor_cmap('Data Type', 'Category10_3', datatype))


x = [list(gdf['x'])]
y = [list(gdf['y'])]
z = [list(gdf['Data_Type'])]

s1 = ColumnDataSource(data=dict(x=x, y=y))
p1 = figure(plot_width=400, plot_height=400, tools="lasso_select", title="Select Here")
p1.circle('x', 'y', source=s1, alpha=0.6)

s2 = ColumnDataSource(data=dict(x=[], y=[], z=[]))
p2 = figure(plot_width=400, plot_height=400, x_range=(0, 1), y_range=(0, 1),
            tools="", title="Watch Here")
p2.circle('x', 'y', source=s2, alpha=0.6)

columns = [TableColumn(field ="x",  title = "X axis"),
           TableColumn(field ="y",  title = "Y axis"),
           TableColumn(field ="z",  title = "Data Type")]

table = DataTable(source =s2, columns = columns, width =155, height = 380)


s1.selected.js_on_change('indices', CustomJS(args=dict(s1=s1, s2=s2, table=table), code="""
        var inds = cb_obj.indices;
        var d1 = s1.data;
        var d2 = s2.data;
        d2['x'] = []
        d2['y'] = []
        for (var i = 0; i < inds.length; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
        }
        s2.change.emit();
        table.change.emit();
    """)
)

layout = row(p1, p2, table)

show(layout)