#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 20:20:47 2024
Updates on Cinco de Maio 2024
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
    
    def add_places(self, place_name, tokens, times, delay=0):
        '''!
        Method to add a place/container into the Petri Net.
        '''
        self.places[place_name] = Place(place_name,tokens)
        self.places[place_name].timer = times
        self.places[place_name].delay = delay

    def add_trans(self, trans_name, attrib, func):
        '''!
        Method to add a tranition into the Petri Net.
        '''
        self.trans[trans_name] = Trans(trans_name)
        self.trans[trans_name].attributes = attrib
        self.trans[trans_name].functions = func
        
    def _get_marking(self):
        marking = {}
        timing = {}
        for name in self.places.keys():
            marking[name] = self.places[name].mark
            timing[name] = self.places[name].timer
        return marking , timing
    
    def _set_marking(self, marking_prime, timing_prime):
        for name in self.places.keys():
            self.places[name].mark = marking_prime[name]
            self.places[name].timer = timing_prime[name]
        
    def _store_marking(self, clock, marking):
        self.markings[str(clock)] = tuple(marking.values())
        
    def _step(self,marking,timing): # add timing_prime, timing
        # loop through the transitions by name
        marking_prime = marking.copy()
        timing_prime = timing.copy()
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
                din = self.places[name].delay # delay for each pin
                tin = self.places[name].timer # timer list at pin
                # timer = timing[name] # timer list at pin
                a_token = len([t for t in tin if t>=din]) #num that have timed out - available
                test = test and a_token >= fin[pin.index(name)]
                
                # test = test and marking[name] >= fin[pin.index(name)]
                # print(marking[name],fin[pin.index(name)],test)
            if test==True:
                for name in pin:
                    marking_prime[name] -= fin[pin.index(name)]
                    # and update the timer list
                    # del timer[0:fin[pin.index(name)]]
                    timing_prime[name] = timing_prime[name][fin[pin.index(name)]:]
                    # print(marking_prime[name])
                for name in pout:
                    marking_prime[name] += fout[pout.index(name)]
                    # and update the timer list
                    # timer.extend([0]*fout[pout.index(name))
                    timing_prime[name] = timing_prime[name] + [0]*fout[pout.index(name)]
        for name in self.places.keys():
            timing_prime[name] = [x+1 for x in timing_prime[name]]
        return marking_prime , timing_prime
    
    def simulate(self, steps):
        # get and store and intial marking
        marking, timing= self._get_marking()
        self._store_marking(0, marking)
        clock = 1
        while clock <= steps:
            marking, timing = self._get_marking()
            #marking_prime = marking.copy()
            # timing_prime = timing.copy()
            marking_prime, timing_prime = self._step(marking,timing) # ,timing_prime, timing
            self._set_marking(marking_prime, timing_prime) #, timing_prime
            self._store_marking(clock, marking_prime)
            clock += 1
