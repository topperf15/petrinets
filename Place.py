#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:32:00 2024

@author: andrew_s
"""

class Place(object):
    '''!
    Class to represent a place or container in petri nets. The tokens 
    are represented as a dictionary where each token is represented as 
    a key-value pair. The key represents the type of token and the 
    value represents the number of such tokens. This enables more than 
    one type of tokens to be represented.
    '''
    def __init__(self, name, mark):
        '''!
        Contructor method.
        
        @param name string: name of the place/container
        '''
        self.name = str(name)
        self.mark = int(mark)
        self.attributes = {}