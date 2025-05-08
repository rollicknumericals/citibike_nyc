################################################  CITIBIKE NYC DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title = 'CitiBike NYC Strategy Dashboard', layout='wide')
st.title("CitiBike NYC Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems CitiBike NYC faces")
st.markdown("Right now, CitiBike runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")

########################## Import data ###########################################################################################

df = pd.read_csv('/Users/mainframe/Documents/GitHub/citibike_nyc/2 Data/Prepped Data/reduced_data_for_plot.csv', index_col = 0)
top20 = pd.read_csv('/Users/mainframe/Documents/GitHub/citibike_nyc/2 Data/Prepped Data/top20.csv', index_col = 0)

########################################## DEFINE THE CHARTS #####################################################################

####### Bar chart #######

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['trips'], marker={'color': top20['trips'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 Most Popular Citi Bike Stations in New York City',
    xaxis_title = 'Start Stations',
    yaxis_title ='Sum of Trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)

####### Line chart #######

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
    go.Scatter(
        x = df['date'], 
        y = df['bike_rides_daily'], 
        name = 'Daily Bike Rides',
        marker = {'color': 'blue'}
    ),
    secondary_y=False
)

fig_2.add_trace(
    go.Scatter(
        x = df['date'], 
        y = df['avg_temp'], 
        name = 'Daily Temperature (°F)',
        marker = {'color': 'red'}
    ),
    secondary_y=True
)

fig_2.update_layout(
    title_text = 'Daily Bike Rides and Temperature for 2022',
    height = 600,
    xaxis_title = 'Date',
    yaxis_title = 'Number of Rides',
    yaxis2_title = 'Temperature (°F)',
)

st.plotly_chart(fig_2, use_container_width=True)

####### Add the map #######

path_to_html = "Citibike Trips Aggregated.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in NYC")
st.components.v1.html(html_data,height=1000)
