#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import pyglet

class Controller(object):
    def __init__(self):
        print("hasodijasiodioasd")
        exit()
        self.window = DummyWindow()
        self.model = DummyModel(19)
        self.data = self.model.get_data()
        self.window.receive_data(self.data)
        pyglet.app.run()
    
    def _update_window(self):
        self.window.receive_data(self.model.data)
        
    def play(self, pos):
        if(self.model.play(pos)):
            self.window.info.text = 'TRUE'
        else:
            self.window.info.text = 'FALSE'

        self._update_window()
            
    def passing(self):
        if self.model.passing():
            if self.model.get_data()['game_over']:
                self.window.info.text = 'Game is Over!'
            else:
                self.window.info.text = 'Continue playing!'

        self._update_window()
    
    def mark_territory(self, pos):
        self.model.mark_territory(pos.x, pos.y)
        self._update_window()
        

######### DUMMY WINDOW VIEW ###########
class DummyWindow(object):
    def __init__(self):
        self.info = self.Label()

    def receive_data(self, data):
        pass

    class Label():
        def __init__(self):
            self.text = ''

######### DUMMY MODEL ###########
class DummyModel(object):
    def __init__(self,n=19):
        self.data = {   'size' : n,
                        'stones' : [[None for i in range(n)]for j in range(n)],
                        'territory': [[None for i in range(n)]for j in range(n)],
                        'game_over': False,
                        'score' : (0,0),
                        'color' : True} 

    def find_territory(self):
        pass

    def get_data(self):
        return self.data

    def mark_territory(self,x, y):
        pass

    def passing(self):
        return True

    def place_stone(self, x, y):
        return False

    def play(self, pos):
        return True

#########################

if __name__ == '__main__':
    c = Controller()