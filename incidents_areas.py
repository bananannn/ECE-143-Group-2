import pandas as pd
import bokeh.io as io
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import mpl, inferno, all_palettes, Reds
from bokeh.models import LogColorMapper, LogTicker, ColorBar


def load_incidents_area_file(fname):
    '''
    Load the incidents information of LA areas and clean the data
    :param fname: the name of the input file
    :param year: the year we want to focus on (we only have data from 2010 to 2018)
    :return: a dataframe contains cleaned incidents data by areas
    '''

    assert isinstance(fname, str)

    traffic = pd.read_csv(fname)

    traffic['Date Occurred'] = pd.to_datetime(traffic['Date Occurred'])
    traffic['year'], traffic['month'] = traffic['Date Occurred'].dt.year, traffic['Date Occurred'].dt.month

    traffic['lon'] = traffic['Location'].apply(lambda x: float(x.split(',')[0][1:]))
    traffic['lat'] = traffic['Location'].apply(lambda x: float(x.split(',')[1][:-1]))

    traffic = traffic[(traffic['year'] == 2017) & (traffic['lat'] != 0) & (traffic['lon'] != 0)]

    traffic.reset_index(inplace=True)

    return traffic


def define_la_areas(traffic):
    '''

    By taking in the incidents' area information, we can organize a new table with the areas boundaries
    :param traffic: the dataframe contains cleaned incidents information by area
    :return: a dataframe contains the boundary of Los Angeles areas
    '''

    assert isinstance(traffic, pd.DataFrame)

    areas = dict(traffic.groupby('Area Name')['Area Name'].count())
    area_name = list(areas.keys())

    area_name_rows = []
    for i in area_name:
        area_row = []
        area_row.append(i)
        lats = list(traffic[traffic['Area Name'] == i]['lat'])
        lons = list(traffic[traffic['Area Name'] == i]['lon'])
        area_row.append(min(lats))
        area_row.append(max(lats))

        area_row.append(min(lons))
        area_row.append(max(lons))

        area_name_rows.append(area_row)

    area_name_table = pd.DataFrame(area_name_rows, columns=['Area_Name', 'min_lat', 'max_lat', 'min_lon', 'max_lon'])

    new = area_name_table.drop([0, 7, 11, 13, 15, 17, 20], axis=0)

    # 1 & 9
    new.at[1, 'min_lat'] = min(new.loc[[1, 9], 'min_lat'])
    new.at[1, 'max_lat'] = max(new.loc[[1, 9], 'max_lat'])
    new.at[1, 'min_lon'] = min(new.loc[[1, 9], 'min_lon'])
    new.at[1, 'max_lon'] = max(new.loc[[1, 9], 'max_lon'])
    new = new.drop(9, axis=0)

    # 6 & 8
    new.at[6, 'min_lat'] = min(new.loc[[6, 8], 'min_lat'])
    new.at[6, 'max_lat'] = max(new.loc[[6, 8], 'max_lat'])
    new.at[6, 'min_lon'] = min(new.loc[[6, 8], 'min_lon'])
    new.at[6, 'max_lon'] = max(new.loc[[6, 8], 'max_lon'])
    new = new.drop(8, axis=0)

    # 10
    new.at[10, 'min_lat'] = new.loc[10, 'min_lat'] + 0.025
    new.at[10, 'max_lat'] = new.loc[10, 'max_lat'] + 0.025
    new.at[10, 'min_lon'] = new.loc[10, 'min_lon'] + 0.045
    new.at[10, 'max_lon'] = new.loc[10, 'max_lon'] + 0.045

    # 14
    new.at[14, 'min_lat'] = new.loc[14, 'min_lat'] + 0.015
    new.at[14, 'max_lat'] = new.loc[14, 'max_lat'] + 0.015

    # 18
    new.at[18, 'min_lat'] = new.loc[18, 'min_lat'] - 0.055
    new.at[18, 'max_lat'] = new.loc[18, 'max_lat'] - 0.055

    # 19
    new.at[19, 'max_lat'] = new.loc[19, 'max_lat'] - 0.01

    # 3
    new.at[3, 'min_lon'] = new.loc[3, 'min_lon'] + 0.025
    new.at[3, 'max_lon'] = new.loc[3, 'max_lon'] + 0.025

    # 2
    new.at[2, 'min_lon'] = new.loc[2, 'min_lon'] + 0.018
    new.at[2, 'max_lon'] = new.loc[2, 'max_lon'] + 0.018

    new.reset_index(inplace=True)
    return new


def draw_blocks_area(new):
    '''
    By taking in the incidents' area information, we create a plot with the areas boundaries
    :param new: the dataframe contains cleaned incidents information by area
    :param fname: the output filename
    :return: a html file contains the blocks of Los Angeles areas
    '''

    assert isinstance(new, pd.DataFrame)

    io.output_notebook()

    p = figure(plot_width=450, plot_height=400)
    # num_square = 21
    p = figure(title='LA Areas')
    p.quad(top=list(new['max_lon']), bottom=list(new['min_lon']),
           left=list(new['min_lat']), right=list(new['max_lat']), fill_alpha=0)

    p.xaxis.axis_label = 'Latitude'
    p.yaxis.axis_label = 'Longitude'
    return show(p)


def draw_blocks_incidents(new, traffic):
    '''
    By taking in the incidents' area information, we create a plot with the areas boundaries.
    The colors filled is based on the number of incidents happened in the area.
    If there are more incidents, the color will be darker.
    :param new: the dataframe contains cleaned incidents information by area
    :param traffic: the dataframe will full traffic incidents information
    :param fname: the output filename
    :return: a html file contains the blocks of Los Angeles areas
    '''

    assert isinstance(new, pd.DataFrame)
    assert isinstance(traffic, pd.DataFrame)

    new_area = list(dict(new.groupby('Area_Name')['Area_Name'].count()))
    incidents_counter = [0] * len(new_area)

    for i in range(traffic.shape[0]):
        for j in range(len(new_area)):
            if (traffic['lon'][i] >= new['min_lon'][j]) & (traffic['lon'][i] <= new['max_lon'][j]) & (
                    traffic['lat'][i] >= new['min_lat'][j]) & (traffic['lat'][i] <= new['max_lat'][j]):
                incidents_counter[j] += 1

    area_dict = dict(zip(new_area, incidents_counter))
    area_dict['Southeast'] += 3187
    area_dict['West LA'] += 1361
    sorted_by_value = sorted(area_dict.items(), key=lambda kv: kv[1], reverse=True)

    checklist = []
    for i in sorted_by_value:
        checklist.append(i[0])

    max_lons = []
    min_lons = []
    max_lats = []
    min_lats = []

    for i in checklist:
        max_lons.append(float(new[new['Area_Name'] == i]['max_lon']))
        min_lons.append(float(new[new['Area_Name'] == i]['min_lon']))
        max_lats.append(float(new[new['Area_Name'] == i]['max_lat']))
        min_lats.append(float(new[new['Area_Name'] == i]['min_lat']))

    io.output_notebook()

    palettes = inferno(120)
    final_palettes = []
    count = 0
    for i in palettes:
        count += 1
        if count % 10 == 0:
            final_palettes.append(i)

    #all_palettes['Reds'][9]

    p = figure(plot_width=450, plot_height=400)
    p.quad(top=max_lons, bottom=min_lons, left=min_lats, right=max_lats, color=final_palettes, fill_alpha=0.8)

    color_mapper = LogColorMapper(palette=final_palettes)
    color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0))

    p.add_layout(color_bar, 'left')

    return show(p)
