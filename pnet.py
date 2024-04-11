#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 20:20:47 2024

@author: andrew_s
"""
from Place import *
from Trans import *

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
    
    def add_places(self, place_name, tokens):
        '''!
        Method to add a place/container into the Petri Net.
        '''
        self.places[place_name] = Place(place_name,tokens)

    def add_trans(self, trans_name, attrib):
        '''!
        Method to add a place/container into the Petri Net.
        '''
        self.trans[trans_name] = Trans(trans_name)
        self.trans[trans_name].attributes = attrib
        
    def _get_marking(self, clock):
        marking = {}
        for name in self.places.keys():
            marking[name] = self.places[name].mark
            #print(name,net.places[name].mark)
        self.markings[str(clock)] = list(marking.values())
        
        return marking
    
    def _set_marking(self, marking_prime, clock):
        for name in self.places.keys():
            self.places[name].mark = marking_prime[name]
            #print(name,self.places[name].mark)
        self.markings[str(clock)] = list(marking_prime.values())
        
    def _step(self,marking_prime,marking):
        for tname in self.trans.keys():
            x = self.trans[tname]
            pin = x.attributes['in']
            pout = x.attributes['out']
            
            for name in pin:
                test = True
                test = test and marking[name] > 0
            if test==True:
                for name in pin:
                    marking_prime[name] -= 1
                    #print(marking_prime[name])
                for name in pout:
                    marking_prime[name] += 1
        return marking_prime
    
    def simulate(self, steps):
        self._get_marking(0)
        clock = 1
        while clock <= steps:
            marking = self._get_marking(clock)
            marking_prime = marking.copy()
            marking_prime = self._step(marking_prime, marking)
            self._set_marking(marking_prime, clock)
            clock += 1
