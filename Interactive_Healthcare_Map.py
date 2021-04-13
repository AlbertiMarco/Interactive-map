import pandas as pd
import numpy as np
import math
import geopandas as gpd
import json
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column

#Import Data
mun=gpd.read_file('data/dataframe.shp')
data=mun[mun['year']==2016] #select a single year
nl_data_json = json.loads(data.to_json())
json_data = json.dumps(nl_data_json)

#Define function that returns json_data for year selected by user.

def json_data(selectedYear):
    data=mun[mun['year']==selectedYear]
    nl_data_json = json.loads(data.to_json())
    json_data = json.dumps(nl_data_json)
    return json_data

#Input GeoJSON source that contains features for plotting.We select 2016 as the first year to show
geosource = GeoJSONDataSource(geojson = json_data(2016))

#Define the color palette.
palette = brewer['YlOrRd'][8]

#Reverse color order so that dark red is the highest health expenditure.
palette = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 880, high = 3000, nan_color = '#d9d9d9')

#Add hover tool
hover = HoverTool(tooltips = [ ('Postcode','@postcode'),('Health Expenditure per cap.', '@costs_per_'),('Average age'
                                ,'@age'),('Household income','@wa_SHI'),('Socio economic status','@status')])


#Create color bar.
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 400, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal')


#Create figure object.
p = figure(title = 'Health expenditure per capita in the Netherlands, 2016', plot_height = 768 , plot_width = 1024)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.add_tools(hover)
p.title.text_font_size= '16pt'
p.title.align='center'


#Add patch renderer to figure.
p.patches('xs','ys', source = geosource,fill_color = {'field' :'costs_per_', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)


p.add_layout(color_bar, 'below')

# Define the callback function: update_plot
def update_plot(attr, old, new):
    yr = slider.value
    new_data = json_data(yr)
    geosource.geojson = new_data
    p.title.text = 'Health expenditure per capita in the Netherlands,%d' %yr

# Make a slider object: slider
slider = Slider(title = 'Year',start =2011 , end = 2016, step = 1, value = 2016)
slider.on_change('value', update_plot)

# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p,widgetbox(slider))
curdoc().add_root(layout)
