#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from template import Group

# constants
BLACK = False
WHITE = True

class Model(object):
    def __init__(self, n=11):
        # Gameplay Attributes
        self.size = n
        self.turn = BLACK

        # used for Ko rule
        self.blocked_field = None

        # used to detect if bother players pass
        self.has_passed = False

        # game over flag
        self.game_over = False

        # The board is represented by a SxS-matrix where each entry
        # contains the information which stone lies there.
        self.board = [[None for i in range(self.size)] for j in range(self.size)]   
        self.territory = [[None for i in range(self.size)] for j in range(self.size)]

        # We need to count the captured stones that got removed from the board
        # Score from empty fields at the end of the game.
        self.score = [0, 0]
        # Stones killed during the game
        self.captured = [0, 0] 

    def passing(self):
        # Do nothing if game_over = True
        if self.game_over:
            return False
        
        # passed => game over
        if self.has_passed:
            self.game_over = True
        else:
            # Invert the turn => next color's turn
            if self.turn == BLACK:
                self.turn = WHITE
            else:
                self.turn = BLACK
            
            self.has_passed = True
            self.blocked_field = None

    def _stones(self):
        colors = [[None for i in range(self.size)] for j in range(self.size)]

        for j in range(0, self.size):
            for i in range(0, self.size):
                if board[j][i] == None:
                    colors[j][i] = None
                else:
                    colors[j][i] = board[j][i].color
                            
        return colors

    def _add(self, grp):
        """Adds a group of stones to the game

        Arguments:
            grp (Group): The group that should be removed
        
        Attributes updated by this function:
            self.board
        """
        for (x,y) in grp.stones:
            self.board[y][x] = grp

    
    def _remove(self, grp):
        """Removes a group of stones from the game

        Arguments:
            grp (Group): The group that should be removed
        
        Attributes updated by this function:
            self.board
        """
        for (x,y) in grp.stones:
            self.board[y][x] = None

    def _kill(self, grp):
        """Removes a group of stones from the game and increases the
        counter of captured stones.

        Arguments:
            grp (Group): The group that should be removed

        Attributes updated by this function:
            self.board
            self.captured
            self.group
        """
        self.captured[not grp.color] += grp.size
        self._remove(grp)

    def _liberties(self, grp):
        """Counts the number of empty fields adjacent to the group.

        Arguments:
            grp (Group): A group of stones.

        Returns:
            (int): nr. of liberties of that group


        """
        return sum([1 for u, v in grp.border if self.board[v][u] is None])     

    def add_scores(self):
        return sum(self.score) + sum(self.captured)

    def get_data(self):
        data = {
            'size' : self.size,
            'stones' : self._stones(),
            'territory' : self.territory,
            'game_over' : self.game_over,
            'score' : self.add_scores(),
            'color' : self.turn
        }

        return data

    def place_stone(x,y):
        # Check if the game is finished
        if self.game_over:
            return False
        
        # Check if the position is free
        if self.board[y][x] != None:
            return False

        new_stone = Group(stones=[(x,y)], color=self.turn)
        groups_to_remove = []
        groups_to_kill = []

        is_valid = False

        # Look at all direct neighbors 
        for (u, v) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            # Check if the neighbor is actually on the board
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue
            
            # Add the neighbor to the border of the new group
            new_group.border.add((u,v))

            # Check if the element at position neighbor is None
            other_group = self.board[v][u]

            if other_group == None:
                is_valid = True
            else:
                # check if the two have the same color
                if new_group.color == other_group.color:
                    # merge the two groups
                    new_group = new_group + other_group
                    # remember to delete the old group
                    groups_to_remove.append(other_group)

                # The groups have different colors
                else:
                    if self._liberties(other) == 1:
                        is_valid = True

                        # make sure other_group is not already in the to-kill list
                        if other_group not in groups_to_kill: 
                            groups_to_kill.append(other_group)

        if self._liberties(new_group) == 1:
            is_valid = True

        # Check if the move is valid
        if is_valid:
            # Remove groups
            for grp in groups_to_remove:
                self._remove(grp)
            # Kill groups
            for grp in groups_to_kill:
                self._kill(grp)

            # Add new group
            self._add(grp)
        
        self.has_passed = False

        # Switch the color (turn)
        self.turn = WHITE if (self.turn == BLACK) else BLACK
        return True
