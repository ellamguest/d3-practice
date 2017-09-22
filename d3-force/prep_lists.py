import os
import pandas as pd
import json

os.chdir('/Users/emg/Programming/GitHub/d3-practice')

# IMPORT AND TIDY LINK LIST
links = pd.read_csv('/Users/emg/Programming/GitHub/mod-timelines/moding-data/td/2017-07-18/lists/edgelist.csv')
links = links[['name','sub']].rename(columns={"name":"source","sub":"target"}).copy()
links["value"] = 1


# IMPORT AND TIDY NODE LIST
nodes = pd.read_csv('/Users/emg/Programming/GitHub/mod-timelines/moding-data/td/2017-07-18/lists/nodelist.csv')
nodes = nodes[['name','mod_type']].rename(columns={"name":"id","mod_type":"group"}).copy()

names = list(links['source']) + list(links['target'])
counts = {}
for i in names:
  counts[i] = counts.get(i, 0) + 1

nodes['degree'] = nodes['id'].apply(lambda x: counts[x])

groups = {0:'subreddit', 1:'former non-top', 2:'former top',
            3:'current top', 4:'current non-top'}
nodes['group_name'] = nodes['group'].apply(lambda x: groups[x])

def label(name, group_name, degree):
    return '{} is a {} and has degree of {}'.format(name, group_name, degree)

nodes['label'] = nodes.apply(lambda x: label(x['id'], x['group_name'], x['degree']), axis=1)

# MAKE JSON-STYLE OBJECT AND SAVE
links = links.to_dict(orient='records')
nodes = nodes.to_dict(orient='records')

d = {"nodes":nodes, "links":links}

with open('/Users/emg/Programming/GitHub/d3-practice/td.json', 'w') as fp:
    json.dump(d, fp)






