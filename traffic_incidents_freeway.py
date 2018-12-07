import pandas as pd
import heapq
import bokeh.io as io
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import brewer


def load_pems_incidents(traffic):
    '''
    The function load the PEMS one-month traffic incidents files and clean the data
    :param traffic: str - the name of the dataset
    :return: a formed dataset
    '''
    assert isinstance(traffic, str)

    traffic = pd.read_csv(traffic, sep=',', header=None)
    traffic.columns = ['Incident ID', 'CC code', 'Incident Number', 'Timestamp', 'Description',
                       'Location', 'Area', 'Zoom Map', 'TB xy', 'lat', 'lon', 'District',
                       'County FIPS ID', 'City FIPS ID', 'Freeway Number', 'Freeway Direction',
                       'State Postmile', 'Absolute Postmile', 'Severity', 'Duration']

    traffic = traffic[(traffic['lat'] <= 34.4992) & (traffic['lon'] <= -117.7831) & (traffic['lon'] >= -118.6917) & (
                traffic['lat'] >= 33.7059)]

    traffic['Timestamp'] = pd.to_datetime(traffic['Timestamp'])
    traffic['hours'] = traffic['Timestamp'].dt.hour

    return traffic


def top_9_freeways(traffic):
    '''
    Return a list with top 9 freeways which has most incidents' numbers
    :param traffic: the traffic dataframe
    :return: a list with top 9 freeways' numbers
    '''

    assert isinstance(traffic, pd.DataFrame)

    freeways = dict(traffic.groupby(['Freeway Number'])['Freeway Number'].count())
    top_10_freeways_tuple = heapq.nlargest(10, freeways.items(), key=lambda i: i[1])

    top_9_freeways = []

    for i in range(8):
        top_9_freeways.append(top_10_freeways_tuple[i][0])

    top_9_freeways.append(top_10_freeways_tuple[9][0])

    return top_9_freeways


def total_traffic_incidents_dayofmonth(traffic):
    '''
    Input a traffic dataframe with extracted hour information
    return a line plot of the total number of incidents happened in each of the hours

    :param traffic: a cleaned dataframe
           fname: output file name
    :return: a line plot
    '''

    assert isinstance(traffic, pd.DataFrame)

    io.output_notebook()

    p = figure(title='Total Traffic incidents in one month', plot_width=400, plot_height=400)

    incidents_number = list(dict(traffic.groupby('hours')['hours'].count()).values())
    # add a line renderer
    p.line(list(range(24)), incidents_number, line_width=2)

    p.xaxis.axis_label = 'Hour of a day'
    p.yaxis.axis_label = 'Number of traffic incidents'

    show(p)


def traffic_incidents_freeways_dayofmonth(traffic):
    '''
    a plot with different freeways' incidents' number in different hours of a month
    :param traffic: a cleaned dataframe
    :param fname: output file name
    :return: a line plot with many different lines
    '''

    assert isinstance(traffic, pd.DataFrame)

    incidents_oneday_all_9_ways = []

    freeways = dict(traffic.groupby(['Freeway Number'])['Freeway Number'].count())
    top_10_freeways_tuple = heapq.nlargest(10, freeways.items(), key=lambda i: i[1])

    top_9_freeways = []

    for i in range(8):
        top_9_freeways.append(top_10_freeways_tuple[i][0])

    top_9_freeways.append(top_10_freeways_tuple[9][0])

    for j in top_9_freeways:
        incidents_oneday_oneway = []
        for i in list(range(24)):
            incidents_oneday_oneway.append(traffic[(traffic['hours'] == i) & (traffic['Freeway Number'] == j)].shape[0])

        incidents_oneday_all_9_ways.append(incidents_oneday_oneway)

    io.output_notebook()

    p = figure(title='Total Traffic incidents in All Freeways', plot_width=950, plot_height=600)
    colors_9 = brewer['Spectral'][9]

    # add a line renderer
    for i in range(9):
        current_label = "Freeway Number: " + str(top_9_freeways[i])
        p.line(list(range(24)), incidents_oneday_all_9_ways[i], color=colors_9[i], legend=current_label, line_width=2)

    p.xaxis.axis_label = 'Hour of Day'
    p.yaxis.axis_label = 'Number of traffic incidents'
    p.legend.label_text_font_size = '8pt'

    show(p)


