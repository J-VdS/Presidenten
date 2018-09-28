# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 21:24:34 2018

@author: Jeroen VdS
"""

from tkinter import *
import random, time

class presidenten(object):
    def __init__(self, ):
        #invoer voor aantal spelers en naam eerste persoon, 
        #geef dan mogelijkheid om evt online samen te spelen
        self.scherm = Tk()
        self.canvas = Canvas(self.scherm, width=300, height=200)
        self.canvas.pack()
        
        self.scherm.update()
        
        self.num_spelers = 4
        self.num_AI = 3
        self.spelers = []
        
        self.setup()
        
    def setup():
        pass     


class speler(object):
    def __init__(self):
        pass
    
    def get_cards(self, kaarten):
        self.kaarten = kaarten

class AI(speler):
    pass




if __name__ == '__main__':
    pass
