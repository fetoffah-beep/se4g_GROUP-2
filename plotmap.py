import pandas as pd
from math import pi
from bokeh.io import curdoc
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import column, row, layout, gridplot
from bokeh.models import ColumnDataSource, Select, HoverTool
from bokeh.models import DataTable, TableColumn
from bokeh.plotting import figure, output_file, show, save
from bokeh.transform import factor_cmap, factor_mark, cumsum
from flaskblog.dataedit import importdf, importgdf, dftype
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.palettes import Category20c

gdf = importgdf()
df = importdf()
dftype = dftype()

source = ColumnDataSource(df)
tile_provider = get_provider(CARTODBPOSITRON)

tools = 'pan, wheel_zoom, box_select, box_zoom, lasso_select, reset'
# Create plot and widget
plot = figure(title= 'Collected Data', plot_width=500, plot_height=500, 
           x_range=(1020414, 1024954), y_range=(5698497, 5700000), 
           x_axis_type="mercator", y_axis_type="mercator",
           tools=tools)

plot.add_tile(tile_provider)

# adding pop up message
myhover = HoverTool()
myhover.tooltips = [('Data Type', '@Data_Type'), ('Value', '@Values'), ('X, Y', '@Longitude_Coordinates, @Latitude_Coordinates')]
plot.add_tools(myhover)

datatype = df['Data_Type'].unique()
MARKERS = ['hex', 'circle_x', 'triangle', 'diamond', 'inverted_triangle', 'asterisk', 'x']

plot.scatter(x='x', y='y', source=source, legend_field="Data_Type", size=5, 
             marker=factor_mark('Data_Type', MARKERS, datatype), fill_alpha=0.4,
             color=factor_cmap('Data_Type', 'Category10_3', datatype))


# selection map
# data for selection map
source2 = ColumnDataSource(df)

plot2 = figure(title= 'Selection Map', plot_width=500, plot_height=500, 
           x_range=plot.x_range, y_range=plot.y_range, 
           x_axis_type="mercator", y_axis_type="mercator",
           tools=tools)
plot2.add_tile(tile_provider)
plot2.circle(x='x', y='y', source=source2)


options = ['All']
for i in df['Data_Type'].unique() :
    options.append(i)

menu = Select(options=options, value=options[0], title='Data Type', width=250)

# Add callback to widgets
def callback(attr, old, new):
    if menu.value == df['Data_Type'].unique()[0] : f = dftype[0]
    elif menu.value == df['Data_Type'].unique()[1]: f = dftype[1]
    elif menu.value == df['Data_Type'].unique()[2] : f = dftype[2]
    elif menu.value == df['Data_Type'].unique()[3] : f = dftype[3]
    elif menu.value == df['Data_Type'].unique()[4] : f = dftype[4]
    elif menu.value == df['Data_Type'].unique()[5] : f = dftype[5]
    elif menu.value == df['Data_Type'].unique()[6] : f = dftype[6]
    else: f = df
    source2.data={'x': f['x'], 'y': f['y']}
menu.on_change('value', callback)


# create pie chart

#source data for pie chart
source3 = dict(df['Data_Type'].value_counts())

data = pd.Series(source3).reset_index(name='value').rename(columns={'index':'Data_Type'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(source3)]

plot3 = figure(title="Collected Data", toolbar_location=None,
           tools="hover", tooltips="@Data_Type: @value", x_range=(-0.5, 1.0))

plot3.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Data_Type', source=data)

plot3.axis.axis_label=None
plot3.axis.visible=False
plot3.grid.grid_line_color = None

# create data table
# source for data table

source4 = ColumnDataSource(df)
columns = [
        TableColumn(field="Data_Type", title="Data Type"),
        TableColumn(field="Values", title="Values"),
        TableColumn(field="x", title="X (m)"),
        TableColumn(field="y", title="Y (m)")
    ]
data_table = DataTable(name='Pie Chart of Collected Data', source=source4, columns=columns, height=500)

# creating outputfile
output_file(r"C:\Users\arlia\Documents\Python Scripts\SEGeo\flaskblog\templates\plotmap.html")
layout = gridplot([[plot, plot2], [None, menu], [None, None], [plot3, data_table]])
show(layout)
curdoc().add_root(layout)