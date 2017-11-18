#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Author: Nik Zaugg

# Controller part of the MVC architecture for an implementation of the Go game

import pyglet
from game_model import Model
import client
# Size of Board (n x n)
n = 4
class Controller(object):
    def __init__(self):
        self.model = Model(n)
        self.window = client.Window(self, n)
        self.window.receive_data(self.model.get_data())
        pyglet.app.run()
    
    # Send updated Data to the View
    def _update_window(self):
        self.window.receive_data(self.model.get_data())
        
    # Send instructions of placing a stone to the Model
    def play(self, pos):
        if(self.model.place_stone(pos[0], pos[1])):
            self.window.info.text = "Nice Move!"
        else:
            self.window.info.text = 'Invalid move!'

        self._update_window()
    
    # Pass on a turn
    def passing(self):
        if self.model.passing():
            if self.model.get_data()['game_over']:
                self.window.info.text = 'Game is Over!'
            else:
                self.window.info.text = 'Continue playing!'

        self._update_window()
    
    # Mark the grid with color-circles to indicate points
    # Happens at the end of the game
    def mark_territory(self, pos):
        # TODO: remove comment once model has implemented Additional Task 2: Mark territory
        # self.model.mark_territory(pos[0], pos[1])
        self._update_window()

if __name__ == '__main__':
    c = Controller()