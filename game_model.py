#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from template import Group

# constants
BLACK = True
WHITE = False

class Model(object):
    """ This class takes care of all the calulcations and the game logic. 
        It prepares the data for the Controller. 

    """
    def __init__(self, n=11):
        """This function initializes a new model. 

        Arguments:
            n (int) - size of the grid

        Attributes initialized by this function:
            self.size
            self.turn
            self.blocked_field
            self.has_passed
            self.game_over
            self.board
            self.territory
            self.score
            self.captured
        """
        # gameplay attributes
        self.size = n
        self.turn = BLACK

        # used for ko-rule
        self.blocked_field = None

        # used to detect if bother players pass
        self.has_passed = False

        # game over flag
        self.game_over = False

        # the board is represented by a size x size - matrix. 
        self.board = [[None for i in range(self.size)] for j in range(self.size)]   
        self.territory = [[None for i in range(self.size)] for j in range(self.size)]

        # score from empty fields at the end of the game.
        self.score = [0, 0]

        # stones killed during the game
        self.captured = [0, 0] 

    def passing(self):
        """
        """

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
        """Returns a nested list (same shape as board) containing the colors of each stone.

        Returns:
            list (boolean) : 
        """
        colors = [[None for i in range(self.size)] for j in range(self.size)]

        for j in range(0, self.size):
            for i in range(0, self.size):
                if self.board[j][i] is None:
                    colors[j][i] = None
                else:
                    colors[j][i] = self.board[j][i].color
                            
        return colors

    def _add(self, grp):
        """Adds a group of stones to the game

        Arguments:
            grp (Group): The group that should be removed
        
        Attributes updated by this function:
            self.board
        """
        for (x, y) in grp.stones:
            self.board[y][x] = grp
    
    def _remove(self, grp):
        """Removes a group of stones from the game

        Arguments:
            grp (Group): The group that should be removed
        
        Attributes updated by this function:
            self.board
        """
        for (x, y) in grp.stones:
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
        """Sums up the scores: adding empty fields + captured stones per player

        Returns:
            list (int): containing the scores of each player
        """
        return [self.score[0] + self.captured[0], 
                self.score[1] + self.captured[1]]

    def get_data(self):
        data = {
            'size'      : self.size,
            'stones'    : self._stones(),
            'territory' : self.territory,
            'game_over' : self.game_over,
            'score'     : self.add_scores(),
            'color'     : self.turn
        }

        return data

    def place_stone(self, x, y):
        """Validates a move and place the new stone.

        Arguments
            x (int): x - coordinate of the new stone
            y (int): y - coordinate of the new stone

        """
        # check if the game is finished
        if self.game_over:
            return False
        
        # check if the position is free
        if self.board[y][x] is not None:
            return False

        # check if the field is already blocked
        if self.blocked_field == (x, y):
            return False

        # create new group with the given coordinates
        new_group = Group(stones=[(x, y)], color=self.turn)

        groups_to_remove = []
        groups_to_kill = []

        # set the move initially to False
        is_valid = False

        # Look at all direct neighbors 
        for (u, v) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            # Check if the neighbor is actually on the board
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue
            
            # Add the neighbor to the border of the new group
            new_group.border.add((u, v))

            # Check if the element at position neighbor is None
            other_group = self.board[v][u]

            if other_group is None:
                is_valid = True
            else:
                # check the colors
                if new_group.color == other_group.color:
                    # merge the two groups
                    # remember to delete the old one
                    new_group = new_group + other_group
                    groups_to_remove.append(other_group)
                else:
                    # check that there is only one free adjacent field to other_group
                    if self._liberties(other_group) == 1:
                        is_valid = True

                        # remember to kill the group
                        if other_group not in groups_to_kill: 
                            groups_to_kill.append(other_group)

        # new_group must have at least one free adjacent field
        if self._liberties(new_group) == 1:
            is_valid = True

        # check if the move is valid
        if is_valid:
            # remove groups
            for grp in groups_to_remove:
                self._remove(grp)

            # kill groups
            for grp in groups_to_kill:
                self._kill(grp)

            # add the new group
            self._add(new_group)

        # ko-rule: block the field where the stone has just been placed
        if new_group.size == 1 and len(groups_to_kill) == 1 and groups_to_kill[0].size == 1:
            for coordinates in groups_to_kill[0].stones:
                self.blocked_field = coordinates
        else:
            self.blocked_field = None
        
        # switch the color (turn)
        self.turn = WHITE if (self.turn == BLACK) else BLACK
        self.has_passed = False

        return True
