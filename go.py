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

        # Create screen to ask for game settings
        starting_screen = Tk()

        # Create a input field for the grid size of the go game
        Label(starting_screen, text='Grid Size').grid(row=0)
        self.grid_size = Entry(starting_screen)
        self.grid_size.grid(row=0, column=1)

        # Create a input field for the name of the first (black) player
        Label(starting_screen, text='Name Player 1 (Black)').grid(row=1)
        self.player_1_name = Entry(starting_screen)
        self.player_1_name.grid(row=1, column=1)

        # Create a input field for the name of the second (white) player
        Label(starting_screen, text='Name Player 2 (White)').grid(row=3)
        self.player_2_name = Entry(starting_screen)
        self.player_2_name.grid(row=3, column=1)

        # Add a button to start a new go game
        Button(starting_screen, text='Start', command=self.start_game).grid(
            row=4, column=1, sticky=W, pady=4)

        # Display the starting screen
        mainloop()

    def start_game(self):
        """Start a new go game with a given grid size."""

        # Read the entered grid size
        n = self.grid_size.get()

        # Read the player's names
        player_1 = self.player_1_name.get()
        player_2 = self.player_2_name.get()

        # Only start a new game if the size is valid
        if n.isdigit() and int(n) > 1:
            if __name__ == '__main__':
                Controller(n, player_1, player_2)

# Open the starting screen
Go_Game()
