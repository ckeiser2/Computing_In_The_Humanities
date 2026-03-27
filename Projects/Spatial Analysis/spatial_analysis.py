#!/usr/bin/env python
# coding: utf-8

# # Geocoding with GeoPy

# In[45]:


# install geopy
get_ipython().system('pip install geopy')


# In[46]:


import pandas as pd

# Import Nominatim ("Name" in Latin) and initialize
# Though most of these services require an API key, Nominatim, which uses OpenStreetMap data, does not,
# which is why we’re going to use it here. But we still need to create a unique application name.
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Wenyi Shang's mapping app", timeout=2)


# In[47]:


# Locate a specific location
location = geolocator.geocode("East Daniel Street, Champaign")
location


# In[48]:


# Full information
location.raw


# In[49]:


print(location.address)
print(location.raw['lat'])
print(location.raw['lon'])
print(location.raw['class'])
print(location.raw['type'])


# In[50]:


possible_locations = geolocator.geocode("East Daniel Street", exactly_one=False)
for location in possible_locations:
    print(location.address)


# In[51]:


Illini_Union = geolocator.geocode('Illini Union')
Illini_Union.address


# # Task 1

# In[52]:


# Create a dataframe to store the geographical locations of a list of places in Champaign.
# The dataframe "Champaign_df" should contain 6 columns:
# "Place", "Address" (obtained by ".address"), "Latitude", "Longitude", "Class", "Type" (obtained by corresponding keys in ".raw")

Champaign_places = ['Foellinger Auditorium', 'Altgeld Hall', 'Krannert Center for the Performing Arts', 
                    'University of Illinois Urbana-Champaign University Library', 'Japan House']

geolocator = Nominatim(user_agent="champaign_locator")

place_list = []
address_list = []
latitude_list = []
longitude_list = []
class_list = []
type_list = []

Cham = geolocator.geocode('Champaign, Illinois')

for place in Champaign_places:
    location = geolocator.geocode(place)
    place_list.append(place)
    address_list.append(location.address)
    latitude_list.append(location.latitude)
    longitude_list.append(location.longitude)
    location_raw = location.raw
    class_list.append(location_raw.get('class'))
    type_list.append(location_raw.get('type'))

Champaign_df = pd.DataFrame({
    'Place': place_list,
    'Address': address_list,
    'Latitude': latitude_list,
    'Longitude': longitude_list,
    'Class': class_list,
    'Type': type_list
})

print(Champaign_df)




# # Making Interactive Maps with folium

# In[54]:


get_ipython().system('pip install folium')


# In[55]:


import folium


# In[58]:


Champaign = geolocator.geocode('Champaign')
Champaign


# In[59]:


Champaign = geolocator.geocode('Champaign')
champaign_map


# In[66]:


# Add a marker
folium.Marker(location=([Illini_Union.raw['lat'], Illini_Union.raw['lon']]), tooltip = 'click me', 
              popup="Illini Union").add_to(champaign_map)
champaign_map


# In[65]:


champaign_map.save("Data/Champaign-map.html")


# # Task 2

# In[67]:


# First, reload the champaign_map to drop the added Marker of Illini Union
# Then for each place in Champaign_df you created for Task 1, add it as a Marker, with location defined by the
# latitude and longitude values in the DataFrame, popup value as the place names in the dataframe



champaign_map = folium.Map(location=[Cham.latitude, Cham.longitude], zoom_start=14)

for i in range(len(Champaign_df)):
    folium.Marker(
        location=[Champaign_df['Latitude'][i], Champaign_df['Longitude'][i]],
        popup=Champaign_df['Place'][i],
    ).add_to(champaign_map)

champaign_map






# # Add a Circle Marker

# In[68]:


# Scottish witchcraft dataset
# (http://witches.hca.ed.ac.uk/#:~:text=The%20database%20contains%20all%20people,to%20social%20and%20cultural%20history)
df = pd.read_csv('data/accused_witches.csv')
df


# In[69]:


# Count the number of witches accused in each county
county_witches = df.groupby("Res_county")["AccusedRef"].count()
county_witches


# In[70]:


# Obtain the latitude and longitude of each county by getting the median of the all latitude and longitude records
# under the name of that county. Median is chose so that incorrect record will be ignored
# (the incorrect data can only be the outliers and will not influence the median),
# and convert them to dictionaries.
county_latitude = df.groupby("Res_county")["latitude"].median()
county_longitude = df.groupby("Res_county")["longitude"].median()
county_latitude_dict = county_latitude.to_dict()
county_longitude_dict = county_longitude.to_dict()
print(county_latitude_dict, county_longitude_dict)


# In[71]:


# Create a dataframe to record the county names, number of cases, and their latitudes and longitudes
county_name = []
county_witch_num = []
county_latitude = []
county_longitude = []
for i in range(len(county_witches)):
    current_county_name = county_witches.index[i]
    county_name.append(current_county_name)
    county_witch_num.append(county_witches[i])
    county_latitude.append(county_latitude_dict[current_county_name])
    county_longitude.append(county_longitude_dict[current_county_name])
data_df = pd.DataFrame({
    'name': county_name,
    'case number': county_witch_num,
    'latitude': county_latitude,
    'longitude': county_longitude,
})
data_df['case number'] = data_df['case number'].astype(float)
data_df = data_df.dropna().reset_index(drop=True) # remove the counties with na values and reset the index
data_df


# In[72]:


data_df.info()


# In[73]:


# Get the location of Scotland
Scotland = geolocator.geocode('Scotland')
Scotland


# In[74]:


# Create the map of Scotland. Zoom_start is smaller than Champaign map because we want to cover a larger area
Scotland_map = folium.Map(location=[Scotland.raw['lat'], Scotland.raw['lon']], zoom_start=6)
Scotland_map


# In[75]:


# Add circles to the map, each representing the witch accused data of a county
for i in range(len(data_df)):
    folium.Circle(location = (data_df['latitude'][i], data_df['longitude'][i]),
                  radius = data_df['case number'][i]*100,
                  tooltip = data_df['name'][i]).add_to(Scotland_map)
Scotland_map


# # Task 3

# In[95]:


# Recreate the map of Scottish witchcraft. First, reload the map with the location of Scottish capital "Edinburgh",
# and set the zoom_start as 7 to focus on the surrounding area of the city. Then add the data of each county into the new map,
# but the radius will be 1000*the square root (this can be obtained by importing "math" and use "math.sqrt") of the case number,
# to get a smoothed result. Besides, add popup according to the format "County_name Case Number: number"
# (e.g., Edinburgh Case Number: 374.0), and set "fill" as True. Finally display the new map.

import math

Edinburgh = geolocator.geocode('Edinburgh, Scotland')


Scotland_map = folium.Map(location=[Edinburgh.latitude, Edinburgh.longitude], zoom_start=7)

for i in range(len(data_df)):
    radius = 1000 * math.sqrt(data_df['case number'][i])
    popup_text = f"{data_df['name'][i]} Case Number: {data_df['case number'][i]}"
    folium.Circle(location=(data_df['latitude'][i], data_df['longitude'][i]), radius=radius, popup=popup_text, fill=True,).add_to(Scotland_map)

Scotland_map


# # Customize Map Backgrounds

# In[82]:


# Using titles in folium
folium.Map(location=[Scotland.raw['lat'], Scotland.raw['lon']], tiles = 'cartodbpositron', zoom_start=6)


# In[83]:


# Using external background
folium.Map(location=[Scotland.raw['lat'], Scotland.raw['lon']],
           zoom_start=4,
           tiles='http://services.arcgisonline.com/arcgis/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',
           attr="Sources: National Geographic, Esri, Garmin, HERE, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, INCREMENT P")


# In[84]:


# And this not necessarily need to be real world...
folium.Map(location=[0, 30],
           zoom_start=4, min_zoom=4, max_zoom=10,
           max_bounds=True,
           min_lon=0, max_lon=70, min_lat=-40, max_lat=40,
           tiles='https://cartocdn-gusc.global.ssl.fastly.net//ramirocartodb/api/v1/map/named/tpl_756aec63_3adb_48b6_9d14_331c6cbc47cf/all/{z}/{x}/{y}.png',
           attr='Textures and Icons from https://www.textures.com/ & https://thenounproject.com/')


# # Geojson

# In[85]:


# US states geojson file (obtained from https://github.com/python-visualization/folium/blob/main/examples/data/us-states.json)
US_states = "Data/us-states.json"


# In[86]:


# Include the US States boundaries in the US Map
US_map = folium.Map(location=[42, -102], zoom_start=4)

folium.Choropleth(
    geo_data = US_states,
).add_to(US_map)

US_map


# In[87]:


# US unemployment rate data (obtained from https://www.kaggle.com/datasets/aniruddhasshirahatti/us-unemployment-dataset-2010-2020?resource=download)
US_unemployment = pd.read_csv("Data/unemployment_data_us_state.csv")
US_unemployment


# In[88]:


# Change column name to match the geojson data
US_unemployment = US_unemployment.rename(columns={'State': 'name'})
US_unemployment


# In[89]:


# Visualize based on unemployment rate of January 2020
US_map = folium.Map(location=[42, -102], zoom_start=4)
folium.Choropleth(
    geo_data = US_states, # Geo_data to be used
    data = US_unemployment, # Data used for visualization
    columns = ['name', 'Unemployment_Rate_Jan_20'], # First column is the key to match, second column is the value to display
    key_on = 'feature.properties.name', # The matched key in geo_data
    fill_color = 'OrRd', # Seelct a color scheme
    line_opacity = 0.2, # Select line opacity
    legend_name= 'Unemployment Rate by State in January 2020', # Choose a name for the legend
).add_to(US_map)

US_map


# In[90]:


# Add tooltip to display the state names
tooltip = folium.features.GeoJson(
    US_states,
    tooltip=folium.features.GeoJsonTooltip(fields=['name'], localize=True)
                                )
US_map.add_child(tooltip)
US_map


# # Task 4

# In[97]:


# Recreate the map of US unemployment. First, create a column 'Unemployment_Rate_2020_spring' in the DataFrame, as the average
# of the unemployment rates of January, Feburary, and March. Then, reload the map using the geocode of "USA" in gelocator.
# Next, create folium.Choropleth, and set the values of the newly-created column Unemployment_Rate_2020_spring, fill_color as
# "GnBu" (green and blue), and line_opacity as 0.3. Also, change the legend name to reflect the change of data.
# Finally, add the State names as tooltip, and display the new map.

US_unemployment['Unemployment_Rate_2020_spring'] = (US_unemployment['Unemployment_Rate_Jan_20']+
                                                  US_unemployment['Unemployment_Rate_Feb_20']+
                                                  US_unemployment['Unemployment_Rate_Mar_20'])/3
USA = geolocator.geocode('USA')

US_map = folium.Map(location=[USA.latitude, USA.longitude], zoom_start=4)


folium.Choropleth(
    geo_data = US_states,
    data = US_unemployment, 
    columns = ['name', 'Unemployment_Rate_2020_spring'],
    key_on = 'feature.properties.name', 
    fill_color = 'GnBu', 
    line_opacity = 0.3, 
    legend_name= 'Unemployment Rate spring 2020',).add_to(US_map)

tooltip = folium.features.GeoJson(
    US_states,
    tooltip=folium.features.GeoJsonTooltip(fields=['name'], localize=True)
                                )
US_map.add_child(tooltip)
US_map







# # Task 5

# This task is designed to enhance your critical analysis and interpretation skills when dealing with visualizations.<br>Write a short paragraph in the following cell for Task 3 to draw conclusions from the data visualization of the geographical distribution of witchcraft cases in Scotland. Additionally, make some assumptions regarding the reasons behind this distribution.<br>Then, write a separate paragraph in the next cell for Task 4 to examine areas in the US with higher or lower unemployment rates in Spring 2020. Also, make assumptions regarding the reasons for this distribution.<br>Finally, remember to convert the cell type for both cells to "markdown" and execute it.

# For the distribution of witchcraft cases in Scotland we can see that through the congregation of major roads/rivers that these are cities. This including the fact that one of them is for sure the capital of Edinburgh this makes sense. As the increase in cases in these areas would be because of the higher populations compared to the countryside/rural areas of scotland. Individuals tend to congregate more leading to altercations or accusations of witchcraft. Also there may be more individuals interested in practicing witchcraft but many of these cases were probably be false cases of witchcraft. But these larger populations in cities is why we see more cases like in Edinburgh, the surrounding areas, and Glasgow. 

# The reason for this distribution may be more nuanced. We see areas with the highest rates of unemployment were states like West Virginia, Virginia, Arizona, Missippi, Lousiana, and Alaska. Many of these states with Arizona and Virginia being outliers have a tendency to be pretty rural states and West Virginia/Missippi are the poorest states in the country. Since they are so poor with a lacking in Urban development there may less job opportunities as businesses don't want to set up in these states also with lower populations. This also pertains to Alaska as they lack population and don't share the same benefit of interstate commerce like other states can benefit from due to Alaska's isolated nature. We can see support for this trend as the most urban, wealthy, and large states like California, Texas, New York, and Illinois all are in the lesser portion of states suffering from unemployment.
# 
# Reference for some of my state assumptions: https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_GDP#:~:text=GDP%20per%20capita%20also%20varied,recorded%20the%20three%20lowest%20GDP
