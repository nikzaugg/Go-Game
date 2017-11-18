#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Author: Nik Zaugg

# Controller part of the MVC architecture for an implementation of the Go game

import pyglet
from game_model import Model
import client

class Controller(object):
    def __init__(self):
        self.window = client.Window()
        self.model = Model(19)
        self.data = self.model.get_data()
        self.window.receive_data(self.data)
        
        # TODO: Do we run the app here as well?
        # pyglet.app.run()
    
    def _update_window(self):
        self.window.receive_data(self.model.get_data())
        
    def play(self, pos):
        if(self.model.place_stone(pos[0], pos[1])):
            self.window.info.text = "Nice Move!"
        else:
            self.window.info.text = 'Invalid move!'

        self._update_window()
            
    def passing(self):
        if self.model.passing():
            if self.model.get_data()['game_over']:
                self.window.info.text = 'Game is Over!'
            else:
                self.window.info.text = 'Continue playing!'

        self._update_window()
    
    def mark_territory(self, pos):
        # TODO: remove comment once model has implemented Additional Task 2: Mark territory
        # self.model.mark_territory(pos.x, pos.y)
        self._update_window()

if __name__ == '__main__':
    c = Controller()