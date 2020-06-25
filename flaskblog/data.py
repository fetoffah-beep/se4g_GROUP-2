import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString
from bokeh.io import curdoc
from bokeh.layouts import gridplot, column, row
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.models import CDSView, ColumnDataSource, HoverTool, Select, CustomJS, IndexFilter
from bokeh.models import BoxSelectTool, BoxZoomTool, LassoSelectTool
from bokeh.transform import factor_cmap, factor_mark
from dataedit import importdf, importgdf, dftype

gdf = importgdf()
df = importdf()
dftype = dftype()


# original source
psource = ColumnDataSource(p_df)

source = ColumnDataSource(data=dict(x=[], y=[]))

# filtered
#view = CDSView(source=psource, filters=[IndexFilter([0,1])

# saving output html file
output_file(r"C:\Users\arlia\Documents\Python Scripts\SEGeo\flaskblog\templates\map.html")

# defining basemap
tile_provider = get_provider(CARTODBPOSITRON)

# managing the map feature
p = figure(title= 'Observerd Data', plot_width=400, plot_height=400, 
           x_range=(1020414, 1024954), y_range=(5698497, 5700000), 
           x_axis_type="mercator", y_axis_type="mercator", 
           tools='pan, wheel_zoom, box_select, box_zoom, lasso_select, reset')
p.add_tile(tile_provider)

# y_range=(5692309, 5698497)
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
myhover.tooltips = [('Data Type', '@Data_Type'), ('Value', '@Values'), ('X, Y', '@Longitude_Coordinates, @Latitude_Coordinates')]
p.add_tools(myhover)

# ploting different marker for each data type
datatype = gdf['Data_Type'].unique()
MARKERS = ['hex', 'circle_x', 'triangle', 'diamond', 'inverted_triangle', 'asterisk', 'x']

# Create scatter plot
p.scatter('x', 'y', source=psource, legend_field="Data_Type", fill_alpha=0.4, 
              size=12, marker=factor_mark('Data_Type', MARKERS, datatype),
              color=factor_cmap('Data_Type', 'Category10_3', datatype))



p2 = figure(plot_width=400, plot_height=400, x_range=(0, 1), y_range=(0, 1),
            tools="", title="Watch Here")
p2.circle('x', 'y', source=source, alpha=0.6)

psource.selected.js_on_change('indices', CustomJS(args=dict(psource=psource, source=source), code="""
        var inds = cb_obj.indices;
        var d1 = psource.data;
        var d2 = source.data;
        d2['x'] = []
        d2['y'] = []
        for (var i = 0; i < inds.length; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
        }
        source.change.emit();
    """)
)
'''
layout = row(p, p2)

show(layout)
'''

'''
p_filtered = figure(plot_height=300, plot_width=300)
p_filtered.circle(x="x", y="y", size=10, hover_color="red", source=source, view=view)

show(gridplot([[p, p_filtered]]))
'''


'''
layout = row(p)

show(layout)
'''



### Use later

'''
s2 = ColumnDataSource(data=dict(x=[], y=[]))
p2 = figure(plot_width=400, plot_height=400, x_range=(0, 1), y_range=(0, 1),
            tools="", title="Watch Here")
p2.circle('x', 'y', source=s2, alpha=0.6)


psource.selected.js_on_change('indices', CustomJS(args=dict(psource=psource, s2=s2), code="""
        var inds = cb_obj.indices;
        var d1 = psource.data;
        var d2 = s2.data;
        d2['x'] = []
        d2['y'] = []
        for (var i = 0; i < inds.length; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
        }
        s2.change.emit();
    """)
)
'''



#p.legend.click_policy = 'hide'

select = Select(title="Option:", value="Buffer", options=list(p_df['Data_Type'].unique()))
'''
callback = select.CustomJS(args=dict(select=select), code="""
            f = select.value
""")
'''
select.js_on_change('value', CustomJS(args=dict(select=select), code="""
            f = select.value
"""))

 
show(column(p, select))


