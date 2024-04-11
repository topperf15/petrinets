#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:34:50 2024

@author: andrew_s
"""

from Place import *
from Trans import *
from GPN import *

# initiate net
net = GPN()

# add places with their initial markings to the net
net.add_places('p1',2)
net.add_places('p2',1)
net.add_places('p3',0)
net.add_places('p4',0)
net.add_places('p5',0)

# add transitions and their relationships to the places
net.add_trans('t1', {'in':['p1','p2'],'out':['p3']})
net.add_trans('t2', {'in':['p3'],'out':['p4','p5']})

# simulate the net - run specified number of steps
net.simulate(2)

edges = []
for tname in net.trans.keys():
    x = net.trans[tname]
    pin = x.attributes['in']
    pout = x.attributes['out']
    
    for name in pin:
        edges.append((name,tname))
    for name in pout:
        edges.append((tname,name))


# importing networkx
import networkx as nx
# importing matplotlib.pyplot
import matplotlib.pyplot as plt

g = nx.DiGraph()
#g.add_nodes_from([d['movement'][0][0],d['movement'][1][0]])
g.add_edges_from(edges)
pos = nx.kamada_kawai_layout(g)
nx.draw_networkx(g,pos,arrows=True,with_labels=True)
plt.savefig("filename.png")

# write markings to file
headers = ['time']+list(net.places.keys())
f = open('flight.csv', 'w') 
f.write(','.join(headers) + '\n')
for tdata in net.markings:
    tdata = [tdata]+[str(items) for items in net.markings[tdata]]
    f.write(','.join(tdata) + '\n')
f.close()
