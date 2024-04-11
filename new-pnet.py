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

# write markings to file
headers = ['time']+list(net.places.keys())
f = open('flight.csv', 'w') 
f.write(','.join(headers) + '\n')
for tdata in net.markings:
    tdata = [tdata]+[str(items) for items in net.markings[tdata]]
    f.write(','.join(tdata) + '\n')
f.close()