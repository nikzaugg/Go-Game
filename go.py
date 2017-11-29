#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Author: Alex Scheitlin

# Starting screen for an implementation of the Go game using the MVC architecture

from Tkinter import Tk, Label, Entry, Button, W, mainloop, StringVar
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

        # Create an input field for the grid size of the go game
        # (also add a callback method to detect changes)
        Label(starting_screen, text='Grid Size').grid(row=0)
        sv_grid_size = StringVar()
        sv_grid_size.trace("w", lambda name, index, mode, sv=sv_grid_size: self.callback_grid_size())
        self.grid_size = Entry(starting_screen, textvariable=sv_grid_size)
        self.grid_size.grid(row=0, column=1)

        # Create an input field for the name of the first (black) player
        # (also add a callback method to detect changes)
        Label(starting_screen, text='Name Player 1 (Black)').grid(row=1)
        sv_player_1 = StringVar()
        sv_player_1.trace("w", lambda name, index, mode, sv=sv_player_1: self.callback_player_1())
        self.player_1_name = Entry(starting_screen, textvariable=sv_player_1)
        self.player_1_name.grid(row=1, column=1)

        # Create an input field for the name of the second (white) player
        # (also add a callback method to detect changes)
        Label(starting_screen, text='Name Player 2 (White)').grid(row=3)
        sv_player_2 = StringVar()
        sv_player_2.trace("w", lambda name, index, mode, sv=sv_player_2: self.callback_player_1())
        self.player_2_name = Entry(starting_screen, textvariable=sv_player_2)
        self.player_2_name.grid(row=3, column=1)

        # Add a button to start a new go game
        Button(starting_screen, text='Start', command=self.start_game).grid(
            row=4, column=1, sticky=W, pady=4)

        # Create a label for messages
        self.info_label = Label(starting_screen, text='')
        self.info_label.grid(row=5, columnspan=2)

        # Display the starting screen
        mainloop()

    def callback_grid_size(self):
        """Empty the info label
        """
        self.info_label.config(text='')

    def callback_player_1(self):
        """Empty the info label
        """
        self.info_label.config(text='')

    def callback_player_2(self):
        """Empty the info label
        """
        self.info_label.config(text='')

    def start_game(self):
        """Start a new go game with a given grid size."""

        # Read the entered grid size
        n = self.grid_size.get()

        # Check if an integer was entered
        if not n.isdigit() or not int(n) > 1:
            self.info_label.config(text='Please enter a grid size larger than 1!')
            return None


        # Read the player's names
        player_1 = self.player_1_name.get()
        player_2 = self.player_2_name.get()

        # Check wheter names were entered
        if not player_1 or not player_2:
            self.info_label.config(text='Please enter your names!')
            return None

        #start a the game
        if __name__ == '__main__':
            Controller(n, player_1, player_2)

# Open the starting screen
Go_Game()
