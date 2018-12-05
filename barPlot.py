import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.palettes import RdBu10
from bokeh.plotting import figure,show
from bokeh.plotting import figure
from bokeh.io import output_notebook, push_notebook, show


def getPlotSource(record, id1, id2):
    '''
    Extract the minimum and maxmum mean travel time of fixed destination and source and return it
    input param: record ,id1, id2
    input param type: dataframe, int, int
    return param:
    return param type: dataframe
    '''

    assert isinstance(record, pd.DataFrame)
    assert isinstance(id1, int)
    assert isinstance(id2, int)
    rows = []
    area_1 = (record.loc[record.area_id == id1, 'movement_id']).tolist()
    area_2 = (record.loc[record.area_id == id2, 'movement_id']).tolist()

    wd = pd.DataFrame()
    we = pd.DataFrame()
    for i in area_1:
        weekdays = df[(df['dstid'] == i) & (df['mean_travel_time'] > 0)]
        weekends = df1[(df1['dstid'] == i) & (df1['mean_travel_time'] > 0)]
        wd = wd.append(weekdays)
        we = we.append(weekends)

    for i in area_2:
        wdd = wd[wd['sourceid'] == i]
        wee = we[we['sourceid'] == i]

    for h in range(24):
        time1 = wdd.loc[wdd.hod == h, ['mean_travel_time']]
        time2 = wee.loc[wee.hod == h, ['mean_travel_time']]
        try:
            min1 = min(time1['mean_travel_time']) / 60
            max1 = max(time1['mean_travel_time']) / 60
        except:
            min1 = 0
            max1 = 0
        try:
            min2 = min(time2['mean_travel_time']) / 60
            max2 = max(time2['mean_travel_time']) / 60
        except:
            min2 = 0
            max2 = 0
        rows.append([h, min1, max1, min2, max2])

    res = pd.DataFrame(rows, columns=['hod', 'weekdayMin', 'weekdayMax', 'weekendMin', 'weekendMax'])
    return res


def make_plot(source):
    '''
    Use the dataframe to plot multiple bars on one diagram
    input param: source
    input param type: dataframe
    return param: plot
    return param type: plot
    '''

    assert isinstance(source, pd.DataFrame)
    plot = figure(x_axis_type="linear", plot_height=600, plot_width=600, tools="", toolbar_location=None)
    plot.title.text = 'Mean travel time during a day from Harbor to Central'
    plot.title.text_font_size = '14pt'

    plot.quad(top='weekdayMax', bottom='weekdayMin', left='left', right='right',
              color=RdBu10[7], source=source, legend="Weekdays", fill_alpha=0.7, line_alpha=0)
    plot.quad(top='weekendMax', bottom='weekendMin', left='left', right='right',
              color=RdBu10[2], source=source, legend="Weekends", fill_alpha=0.7, line_alpha=0)

    # fixed attributes
    plot.xaxis.axis_label = "Hour of day (h)"
    plot.yaxis.axis_label = "Mean travel time (min)"
    plot.axis.axis_label_text_font_style = "bold"
    plot.axis.axis_label_text_font_size = '12pt'
    plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 0.7

    return plot