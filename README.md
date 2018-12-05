# ECE-143-Group-2

Analysis of Traffic Data for the city of Los Angeles

## Group members
Moyan Zhou: email: moz006@ucsd.edu
Cai Chen: email: cac005@ucsd.edu
Yifan Ruan: email: yir021@ucsd.edu


## Problem:

Gathering and understanding Uber Movement data, traffic incidents data, and freeways data for the city of Los Angeles given the location data and the month of the year.

## Dataset:

Uber Movement dataset (https://ubr.to/2JvIdNA)

The entire dataset comprises of 6 CSV files, for 4 different quarters of the year 2017 and one quarter of the year 2018 along with one map JSON file for Los Angeles. The CSV files comprise of Source ID, Destination ID, Month of the Year, Mean Travel Time for the city of Los Angeles. The map file contains the boundaries in geospatial (.geoJSON) format, including Zone IDs.

Traffic Freeways dataset (http://pems.dot.ca.gov/?dnode=Clearinghouse)
The dataset of freeway flows and speeds contains the station information in the district 7 (LA areas). For each row in the table, it has the timestamp, the flow and speeds around the stations, and the direction of the route. 
The dataset of triffic incidents happened in each freeway in LA area. For each of the incidents, it has the timestamp, the direction of the freeway, the freeway number, and the description of the incident. 

Traffic incients dataset (https://data.lacity.org/A-Safe-City/Traffic-Collision-Data-from-2010-to-Present/d5tf-ez2w)
The dataset contains the traffic collisions happened in LA from 2010 to present. For each of the incidents, it includes the time it occured, the location in latitude and longitude, the cross street, and the area. 

## Proposed Solution and  Real-world applications:

We propose to understand the urban mobility of the city of Los Angeles using data visualization tools such as bar graphs, pie charts, heat maps of LA locations etc. to comprehend the travel duration given the source, destination and month of the year. The solution would be used to understand the urban mobility of Los Angeles given the month of the year. This would be useful to make informed decisions about location picking and route picking for a more efficient traffic flow. 


## Libraries Used
The user should import all the libararies listed below in order to run the project.

Bokeh: "an interactive visualization library that targets modern web browsers for presentation"
Website: https://bokeh.pydata.org/en/latest/docs/user_guide/quickstart.html#userguide-quickstart
To install: pip install bokeh

Forliumn: "folium builds on the data wrangling strengths of the Python ecosystem and the mapping strengths of the leaflet.js library. "
Website: https://python-visualization.github.io/folium/
To install: pip install folium

Matplotlib: "a Python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms"
To instal: pip install matplotlib


## Files Contained
Several python files contain all the funcitons used in the jupyter notebook.
One jupyter notebook file for the visualization.



