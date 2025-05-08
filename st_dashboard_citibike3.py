################################################ CITIBIKE NYC DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title = 'CitiBike NYC Strategy Dashboard', layout='wide')
st.title("CitiBike NYC Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])
########################## Import data ###########################################################################################

df = pd.read_parquet('2 Data/Prepped Data/reworked_for_streamlit.parquet')
df_line = pd.read_csv('2 Data/Prepped Data/reduced_data_for_plot.csv')

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at assessing the current logistics model of bike distribution across the city, and identifying expansion opportunities.")
    st.markdown("There are many positive aspects to CitiBike NYC's existing program. It's a cost effective means of transportation. It has thousands of docking stations aiding in convenient access to most any destination in the city. It also promotes health and fitness.") 
    st.markdown("However, it faces operational challenges as well. Certain stations are full to the point that some riders are unable to return their bikes. Some stations are empty, or only contain broken bikes so riders can't rent when and where they need to. Rebalancing, maintenance, and rising costs are also potential problems.") 
    st.markdown("This analysis will look at the potential reasons behind these. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("dylan-dehnert-Yq2U8oTvcsQ-unsplash.jpg") #source: https://https://unsplash.com/photos/a-row-of-bikes-parked-in-front-of-a-building-Yq2U8oTvcsQ
    st.image(myImage)

 ### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(
        x = df_line['date'], 
        y = df_line['bike_rides_daily'], 
        name = 'Daily Bike Rides',
        marker = {'color': 'blue'}
    ),
    secondary_y=False
)

    fig_2.add_trace(
    go.Scatter(
        x = df_line['date'], 
        y = df_line['avg_temp'], 
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
    st.markdown("There is a noticeable correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. However, during the middle to late spring, there is a period when rides spike above the temperature line. When it's hot in summer, rides lag beneath the heat line. Then rides jump up slightly in the first half of the fall, even while the temperature begins its gradual descent. These insights indicate that the shortage, and overcrowding problems may be prevalent during these times when expected ridership fluctuates slightly. Daily rides frequently top 100K from mid-April through mid-November. It's important to note that late-August through late-September is the most active month-long period, with rides often approaching 140K per day. There are a handful or so days, especially around Mother's Day and Labor Day weekends, throughout the year when rides drop severely. These could be good times to do quick maintenance on the bike fleet. The winter would be the best time for large-scale fleet maintenance.")

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    # Step 1: Create the season filter on the sidebar
    with st.sidebar:
        season_filter = st.multiselect(
        label='Select the season',
        options = df['season'].unique(),
        default = df['season'].unique()  # Default shows all seasons
    )

    # Step 2: Filter the data based on the selected seasons
    df1 = df.query('season == @season_filter')

    # Step 3: Calculate the total bike rides for the selected seasons
    total_rides = float(df1['daily_trips_per_station'].sum())

    # Step 4: Display the Total Bike Rides widget
    st.metric(label = 'Total Bike Rides', value = numerize(total_rides))

    # Step 5: Group the data by 'start_station_name' and sum the 'daily_trips_per_station'
    df_station_trips = df1.groupby('start_station_name', as_index = False).agg(
    total_trips = ('daily_trips_per_station', 'sum')
    )

    # Step 6: Get the top 20 stations based on total trips
    top20 = df_station_trips.nlargest(20, 'total_trips')

    # Step 7: Create a bar chart to show the top 20 stations
    fig = go.Figure(go.Bar(
    x = top20['start_station_name'], 
    y = top20['total_trips'],
    marker = {'color': top20['total_trips'], 'colorscale': 'Blues'}
    ))

    fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York City ',
    xaxis_title = 'Start Station Name',
    yaxis_title = 'Total Trips',
    width = 900, 
    height = 600
    )

    # Step 8: Display the bar chart
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is clear that some start stations are more popular than others. Summer is the busiest season, with nearly three times the total rides compared to winter, the least busy season. The top 20 start stations account for just over 6% of all rides in the city, year-round. The top 3 busiest start stations throughout the year, are W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St.") 
    st.markdown("It's well known that 6th Avenue is a top shopping spot in NYC. There are also several corporate headquarters located there. The World Trade Center, 9/11 Memorial and Museum, Oculus - a major a transportation hub, as well as Hudson River Park, are major attractions near West St & Chambers St. Central Park, and Rockefeller Center are within walking distance of Broadway and W 58th St.")

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated CitiBike trips over NYC")

    path_to_html = "Citibike Trips Aggregated.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.markdown("<h2 style='margin-bottom: -20px;'>Aggregated CitiBike Trips in NYC</h2>", unsafe_allow_html=True)
    st.components.v1.html(html_data, height=800)  # Adjusted height to 800
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("Within the most common trips made, there are few end-station points, and many start-station points. The most popular end points are near popular areas in, and outside the city.")
    st.markdown("11th & West 27th street is among the most popular destinations. This is near The High Line, which is an elevated park. Built on former railway tracks, it offers unique views of the city. Also nearby are: Chelsea Market, a popular food hall; Hudson Yards, large-scale development featuring the Vessel - a unique interactive art structure; The Museum of Modern Art (MoMA); Rockefeller Center. These are popular spots for both locals and tourists.")
    st.markdown("Newport parkway, which is actually located in New Jersey, offers views of the New York City skyline. Notable attractions nearby include Pier-A Park, the Hoboken Waterfront, and Newport Centre Mall. This area is also known for its scenic walkings, and boat tours along the Hudson River.")
    st.markdown("4th & Jackson street is near Jackson Avenue Station, which is served by the 2 train at all hours.")

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("tom-dillon-L9OHAHs41Lk-unsplash.jpg")  #source: https://https://unsplash.com/photos/woman-in-black-jacket-riding-blue-motorcycle-on-road-during-daytime-L9OHAHs41Lk
    st.image(bikes)
    st.markdown("### Our analysis has shown that CitiBikes should focus on the following objectives moving forward:")
    st.markdown("- Ensure bikes are fully stocked in the busiest stations from mid-April through June. Then, to avoid overcrowding, cut back the fleet by the amount of units that need upkeep and maintenance during July and the first weeks August to guarantee we have the most bikes available for our busiest month-long period from late August to late September. Then maintain as full and functional a fleet as possible through mid-November. The dropping temperatures in early fall don't necessarily translate into less demand for bikes.")
    st.markdown("- Create more stations near ferry terminals, major attractions, and parks, to both serve demand, and encourage more usage, in our established areas.")
    st.markdown("- Scout new areas for more bike stations near subway entrances, and bus stops, to inscrease connectivity and supplemental transportation.")
    st.markdown("- Focus new stations in places with high foot traffic, like waterfront parkways, piers, and cultural hubs, as these are proven areas of interest for tourists and locals.")
    st.markdown("- Frequently redistribute bikes from heavily trafficked end stations to popular start stations to maintain a balanced circulation of bikes. This way we reduce overuse/underuse of portions of our fleet, therefore dispersing an even amount of wear and tear on the units. This will help lower maintenance costs.")