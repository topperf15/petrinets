#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 20:20:47 2024

@author: andrew_s
"""
class Place(object):
    '''!
    Class to represent a place or container in petri nets.
    '''
    def __init__(self, name, mark):
        '''!
        Contructor method.
        
        @param name string: name of the place/container
        '''
        self.name = str(name)
        self.mark = int(mark)
        self.timer = []
        self.delay = 0
        self.attributes = {}
        
class Trans(object):
    '''!
    Class to represent a transition in petri nets.
    '''
    def __init__(self, name):
        '''!
        Contructor method.
        
        @param name string: name of the transition
        '''
        self.name = str(name)
        self.attributes = {}
        self.functions = {}

class GPN(object):
    '''!

    '''
    def __init__(self):
        '''!
        Contructor method.
        '''
        self.places = {}
        self.trans = {}
        self.markings = {}
    
    def add_places(self, place_name, tokens, delay=0):
        '''!
        Method to add a place/container into the Petri Net.
        '''
        self.places[place_name] = Place(place_name,tokens)
        self.places[place_name].timer = [0]*tokens

    def add_trans(self, trans_name, attrib, func):
        '''!
        Method to add a tranition into the Petri Net.
        '''
        self.trans[trans_name] = Trans(trans_name)
        self.trans[trans_name].attributes = attrib
        self.trans[trans_name].functions = func
        
    def _get_marking(self):
        marking = {}
        # a_marking = {}
        for name in self.places.keys():
            marking[name] = self.places[name].mark
            # timer = self.places[name].timer
            # delay = self.places[name}.delay
            # a_mark = len([t for t in timer if t>=delay]) #num that have timed out - available
            # a_marking[name] = a_mark
        
        return marking  # also return avail marking (a_marking)
    
    def _set_marking(self, delta):
        for name in self.places.keys():
            self.places[name].mark += delta[name]
        #self._store_marking(clock, marking_prime)
        
    def _store_marking(self, clock, marking):
        self.markings[str(clock)] = list(marking.values())
        
    def _step(self,marking):
        # loop through the transitions by name
        delta = {}
        for name in self.places.keys():
            delta[name] = 0
        for tname in self.trans.keys():
            x = self.trans[tname]       # transition
            pin = x.attributes['in']    # input places list
            pout = x.attributes['out']  # output places list
            fin = x.functions['in']     # value of input arcs
            fout = x.functions['out']   # value at output arcs
            
            # check to see if there are enough avail tokens
            # at each input place to fire the transtion (True)
            test = True
            for name in pin:
                test = test and marking[name] >= fin[pin.index(name)]
                #print(marking[name],fin[pin.index(name)],test)
            if test==True:
                for name in pin:
                    delta[name] -= fin[pin.index(name)]
                    #print(marking_prime[name])
                for name in pout:
                    delta[name] += fout[pout.index(name)]
        return delta
    
    def simulate(self, steps):
        # get and store and intial marking
        marking = self._get_marking()
        self._store_marking(0, marking)
        clock = 1
        while clock <= steps:
            marking = self._get_marking()
            marking_prime = marking.copy()
            delta = self._step(marking)
            self._set_marking(delta)
            self._store_marking(clock, marking_prime)
            clock += 1
