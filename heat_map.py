import pandas as pd
import heapq
import folium
from folium.plugins import HeatMap

from pandas.io.json import json_normalize


def load_uber_file(movement):
    '''
    Can read all kinds of uber movement csv files
    :param movement: the uber movement csv file
    :return: a cleaned dataframe contains travel times and movement ids
    '''

    assert isinstance(movement, str)
    assert len(movement) != 0

    return pd.read_csv(movement)


def extract_movement_id(la_map):
    '''
    By reading the map file, we can extract the coordinates of different uber movement ids
    :param la_map: the Los Angeles map json file provided by Uber
    :return: a dataframe contains each movement id and their coordinates
    '''

    assert isinstance(la_map, str)
    assert len(la_map) != 0

    map_LA = pd.read_json(la_map, orient='records')
    map_LA_header = pd.DataFrame(map_LA.features.values.tolist())
    map_LA_coor = dict(pd.DataFrame(map_LA_header.geometry.tolist())['coordinates'])  # the index off by 1

    rows = []
    for i in range(len(map_LA_coor)):
        row = []
        row.append(i + 1)

        if len(map_LA_coor[i][0][0]) == 2:
            row.append(round(map_LA_coor[i][0][0][1], 4))
            row.append(round(map_LA_coor[i][0][0][0], 4))

        else:
            row.append(round(map_LA_coor[i][0][0][0][1], 4))
            row.append(round(map_LA_coor[i][0][0][0][0], 4))
        rows.append(row)
    return pd.DataFrame(rows, columns=['movement_id', 'long', 'lat'])


def top_500_pickup_location(movement):
    '''
    Picking the top 500 popular pickup locations and return a list contains those movement ids
    :param movement: the dataframe of movement information
    :return: a list of top 500 pickup locations
    '''

    assert isinstance(movement, pd.DataFrame)

    sid = dict(movement.groupby('dstid')['dstid'].count())
    top_500_pickup_tuple = heapq.nlargest(500, sid.items(), key=lambda i: i[1])
    top_500_dest = [x[0] for x in top_500_pickup_tuple]

    return top_500_dest


def heat_map(movement_ids, top_500_pickup, movement):
    '''
    Use the top 500 pickup ids and their coordinates draw a heat map;
    the more popular pickup location, the color will be darker.
    :param movement_ids: a dataframe contains all ids and their coordinates
    :param top_500_pickup: the top 500 locations' list
    :param movement: the dataframe contains all the movement information
    :return: a heat map
    '''

    assert isinstance(movement_ids, pd.DataFrame)
    assert isinstance(top_500_pickup, list)
    assert len(top_500_pickup) == 500

    lat = []
    long = []
    selectids = []
    sid = dict(movement.groupby('sourceid')['sourceid'].count())
    for i in top_500_pickup:
        lat.append(float(movement_ids[movement_ids['movement_id'] == i]['lat']))
        long.append(float(movement_ids[movement_ids['movement_id'] == i]['long']))

        selectids.append(sid[i])

    max_amount = float(max(selectids))

    hmap = folium.Map(location=[34.07225, -118.244728], zoom_start=10, )

    hm_wide = HeatMap(list(zip(long, lat, selectids)),
                      min_opacity=0.8,
                      max_val=max_amount,
                      radius=6, blur=6,
                      max_zoom=1,
                      )

    # folium.GeoJson(district23).add_to(hmap)
    return hmap.add_child(hm_wide)

