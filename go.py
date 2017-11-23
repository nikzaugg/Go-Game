#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Author: Alex Scheitlin

# Starting screen for an implementation of the Go game using the MVC architecture

from Tkinter import *
from controller import Controller

class Go_Game():
    """This class provides an input field to enter the size of the grid
    of the go game and start a new go game."""

    def __init__(self):
        """Display a form to enter the size of the grid of the go game
        and start it

        Arguments:
            -

        Attributes updated by this function:
            self.grid_size
        """

        # Create a input field for the grid size of the go game
        starting_screen = Tk()
        Label(starting_screen, text='Grid Size').grid(row=0)
        self.grid_size = Entry(starting_screen)
        self.grid_size.grid(row=0, column=1)

        # Add a button to start a new go game
        Button(starting_screen, text='Start', command=self.start_game).grid(row=3, column=1, sticky=W, pady=4)

        # Display the starting screen
        mainloop()

    def start_game(self):
        """Start a new go game with a given grid size."""
        
        # Read the entered grid size
        n = self.grid_size.get()

        # Only start a new game if the size is valid
        if n.isdigit() and int(n) > 1:
            if __name__ == '__main__':
                Controller(self.grid_size.get())

# Open the starting screen
Go_Game()
