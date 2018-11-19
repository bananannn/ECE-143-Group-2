"""
Finding any 20 locations’travelling relationships and frequency and generating a graph of relation
Author: Cai Chen
"""

import pandas as pd
from pyecharts import Graph

quarter_1_2017 = 'los_angeles-taz-2017-1-All-MonthlyAggregate.csv'
quarter_2_2017 = 'los_angeles-taz-2017-2-All-MonthlyAggregate.csv'
quarter_3_2017 = 'los_angeles-taz-2017-3-All-MonthlyAggregate.csv'
quarter_4_2017 = 'los_angeles-taz-2017-4-All-MonthlyAggregate.csv'
quarter_1_2018 = 'los_angeles-taz-2018-1-All-MonthlyAggregate.csv'
month = 2

df = pd.read_csv(quarter_1_2018, encoding='utf8', engine='python')

index = df.columns
index = index[:4]
print(index)
location_id = [234, 23, 657, 2345, 233, 11, 3, 5678, 123, 1235]
sourceid = df.loc[df['month'] == month, 'sourceid']
dstid = df['dstid']
source_freq = sourceid.value_counts()

for i in range(10):
    try:
        source_freq[location_id[i]]
    except KeyError:
        source_freq[location_id[i]] = 1

nodes = [{"name": str(location_id[0]), "symbolSize": source_freq[location_id[0]]/50},
         {"name": str(location_id[1]), "symbolSize": source_freq[location_id[1]]/50},
         {"name": str(location_id[2]), "symbolSize": source_freq[location_id[2]]/50},
         {"name": str(location_id[3]), "symbolSize": source_freq[location_id[3]]/50},
         {"name": str(location_id[4]), "symbolSize": source_freq[location_id[4]]/50},
         {"name": str(location_id[5]), "symbolSize": source_freq[location_id[5]]/50},
         {"name": str(location_id[6]), "symbolSize": source_freq[location_id[6]]/50},
         {"name": str(location_id[7]), "symbolSize": source_freq[location_id[7]]/50},
         {"name": str(location_id[8]), "symbolSize": source_freq[location_id[8]]/50},
         {"name": str(location_id[9]), "symbolSize": source_freq[location_id[9]]/50}]

links = []
# for i in nodes:
#     for j in nodes:
#         links.append({"source": i.get('name'), "target": j.get('name')})

for i in range(10):
    search = df.loc[df['sourceid'] == location_id[i], ['dstid', 'month', 'mean_travel_time']]
    ssearch = search.loc[search['month'] == month, ['dstid', 'mean_travel_time']]
    for j in range(10):
        if ssearch[(ssearch.dstid == location_id[j])].index.tolist():
            value = ssearch.loc[ssearch['dstid'] == location_id[j], ['mean_travel_time']]
            value = list(value['mean_travel_time'])
            links.append({"source": str(location_id[i]), "target": str(location_id[j]), "value": str(value[0]) + ' sec'})
""""value": value[0]"""
graph = Graph("")
graph.add("",
          nodes,
          links,
          is_label_show=True,
          graph_layout="circular",
          label_text_color=None,
          graph_edge_symbol="arrow")
graph.render()


