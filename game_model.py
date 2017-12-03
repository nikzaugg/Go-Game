#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Author: Moritz Eck

# Model part of the MVC architecture for an implementation of the Go game

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
        """Action when a player passes his turn.

        Variables changed by this function:
            self.game_over
            self.turn
            self.has_passed
            self.blocked_field
        """

        # do nothing if game is over
        if self.game_over:
            return False
        
        # both players pass => game over
        if self.has_passed:
            self.game_over = True
            return True
        
        # invert the turn & set passed to true
        self.turn = WHITE if (self.turn == BLACK) else BLACK     
        self.has_passed = True
        self.blocked_field = None

        return True

    def _stones(self):
        """Returns a nested list (same shape as board) containing the colors of each stone.

        Returns:
            list (boolean) : multidimensional list containing the colors of the stones on the board.
        """
        # initialize a new empty list with the size of the playing board
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
            grp (Group): The group that shall be added
        
        Attributes updated by this function:
            self.board
        """
        for (x, y) in grp.stones:
            self.board[y][x] = grp
    
    def _remove(self, grp):
        """Removes a group of stones from the game

        Arguments:
            grp (Group): The group that shall be removed
        
        Attributes updated by this function:
            self.board
        """
        for (x, y) in grp.stones:
            self.board[y][x] = None

    def _kill(self, grp):
        """Removes a group of stones from the game and increases the
        counter of captured stones.

        Arguments:
            grp (Group): The group that has been killed - needs to be removed

        Attributes updated by this function:
            self.board
            self.captured
            self.group
        """
        # increase the caputured counter of the opposite color by the nr. of stones in the grp 
        self.captured[not grp.color] += grp.size

        # remove the group
        self._remove(grp)

    def _liberties(self, grp):
        """Counts the number of empty fields adjacent to the group.

        Arguments:
            grp (Group): a group of stones.

        Returns:
            (int): nr. of liberties of that group
        """
        return sum([1 for u, v in grp.border if self.board[v][u] is None])     

    def add_scores(self):
        """Sums up the scores: adding empty fields + captured stones per player

        Returns:
            list (int): containing the scores of each player
        """
        return [self.score[0] + self.captured[0], self.score[1] + self.captured[1]]

    def get_data(self):
        """Returns the data object containing all relevant information to the controller.

        Returns:
            data (dictionary): data object for the controller
        """
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
        """Attempts to place a new stone. 
           Validates the move and if valid, executes the respective action. 

        Arguments
            x (int): x - coordinate of the new stone
            y (int): y - coordinate of the new stone

        Variables changed by this function
            self.has_passed
            self.blocked_field
            self.turn
            self.board - adds / removes / kills stones
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

        # create two lists to remember the groups to remove / kill
        groups_to_remove = []
        groups_to_kill = []

        ######################################
        # Move Validation
        ######################################

        # set the move validity initially to False
        is_valid = False

        # All direct neighbors of (x, y)
        for (u, v) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:

            # Check if the neighbor is on the board
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue
            
            # Add the neighbor to the border of the new group
            new_group.border.add((u, v))

            other_group = self.board[v][u]
            
            # check if neighbor is None
            if other_group is None:
                is_valid = True
                continue

            # same color
            if new_group.color == other_group.color:
                # merge the two groups
                new_group = new_group + other_group

                # remember to delte the old grp (other_group)
                groups_to_remove.append(other_group)

            # groups have different colors
            # check that there is only one free adjacent field to other_group
            elif self._liberties(other_group) == 1:
                is_valid = True
                
                # remember to kill the other_group
                if other_group not in groups_to_kill: 
                    groups_to_kill.append(other_group)

        # new_group must have at least one free adjacent field
        if self._liberties(new_group) >= 1:
            is_valid = True

        ######################################
        # Move Execution (only if valid)
        ######################################

        # the move is valid
        if is_valid:
            # remove groups
            for grp in groups_to_remove:
                self._remove(grp)

            # kill groups
            for grp in groups_to_kill:
                self._kill(grp)

            # add the new group
            self._add(new_group)
        
        # the move is invalid
        else:
            return False

        ######################################
        # ko-rule: block the field where the stone has just been placed
        ######################################

        # 3 conditions for the ko-rule to apply
        # 1. the new group has only one stone
        # 2. only one group has been killed
        # 3. the killed group has only had one stone
        if new_group.size == 1 and len(groups_to_kill) == 1 and groups_to_kill[0].size == 1:
            for (x, y) in groups_to_kill[0].stones:
                self.blocked_field = (x, y)
        else:
            self.blocked_field = None
        
        ######################################
        # Turn End Actions: Change the current player
        ######################################

        # switch the color (turn)
        self.turn = WHITE if (self.turn == BLACK) else BLACK
        self.has_passed = False

        return True

    def _compute_score(self):
        """Counts the number of marked fields and updates the score.

        Variables changed by this function 
            self.score
        """

        # reset the scores to zero
        self.score = [0, 0]

        for j in range(0, self.size):
            for i in range(0, self.size):
                # count the black stones
                if self.territory[j][i] == BLACK:
                    if self.board[j][i] != None:
                        # add 1 additional point for dead stones inside the territory 
                        self.score[BLACK] += 2
                    else:
                        self.score[BLACK] += 1
                        
                # count the white stones        
                elif self.territory[j][i] == WHITE:
                    if self.board[j][i] != None:
                        # add 1 additional point for dead stones inside the territory 
                        self.score[WHITE] += 2
                    else:
                        self.score[WHITE] += 1

    def _claim_empty(self, x, y, color, area=None):
        """ Claims an empty field including all adjacent (neighboring) empty fields.

        Arguments
            x (int): x-coordinate
            y (int): y-coordinate
            color (boolean): color the empty field will receive
            area (list):     visited coordinates / fields
        
        Variables changed by this function
            self.territory
        """

        # initialize a new empty list
        if area is None:
            area = list()

        # recursion stopping criteria
        # position is not empty or has already been traversed
        if self.board[y][x] is not None or (x, y) in area:
            return

        # claim the empty field
        self.territory[y][x] = color

        # remembering the current location 
        area.append((x, y))

        # recursively checking all neighbors
        for (u, v) in [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]:

            # check that the neighbor actually exists on the board
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue
            
            # claim neighboring empty field
            if (u, v) not in area and self.board[v][u] is None:
                self._claim_empty(u, v, color, area=area)

    def _claim_group(self, x, y, color, area=None):
        """Claims an entire group and also all adjacent empty fields.

        Arguments
            x (int) - x-coordinate
            y (int) - y-coordinate
            color (boolean) - color of player the empty field will receive
            area (list) - visited coordinates / fields

        Variables changed by this function
            self.territory
        """

        # initialize a new empty list
        if area is None:
            area = list()

        # claiming each stone in the group at coordinates (x, y)
        for (u, v) in self.board[y][x].stones:
            if (u, v) not in area:
                # remembering the current location
                area.append((u, v))

                # claiming the position
                self.territory[v][u] = color
        
        # claiming each empty field in the adjacent empty fields
        for (u, v) in self.board[y][x].border:
            if self.board[v][u] is None and (u, v) not in area:
                self._claim_empty(u, v, color, area=area) 
    
    def _find_empty(self, x, y, area=None, count=None):
        """ Finds the connected empty fields starting at (x, y) and
        counts the adjacent stones of each color.

        Returns:
            area (list):    empty fields [Black, White]
            count (list):   number of adjacents stones to [Black, White]
        """
        
        # TODO: BUG: Fix that stones are counted multiple times if more than one empty field is adjacent to them

        # initialize a new empty list
        if area is None:
            area = list()

        # initializes the count
        if count is None:
            count = [0, 0]

        # recursion stopping criteria
        # position is not empty or has already been traversed
        if self.board[y][x] is not None or (x, y) in area:
            return area, count

        # add the current position to the traversed
        area.append((x, y))

        # recursively checking all neighbors
        for (u, v) in [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]:

            # check that the neighbor actually exists on the board
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue
            
            # claim neighboring empty field
            if (u, v) not in area:
                if self.board[v][u] is None:
                    self._find_empty(u, v, area=area, count=count)
                else:
                    count[self.board[v][u].color] += 1

        return area, count

    def mark_territory(self, x, y):
        """Function that can be evoked by user to claim territory for one player.
        For empty fields it will also mark all adjacent empty fields,
        for fields that contain a stone it will mark the entire stone
        group and all adjacent empty spaces.

        Arguments:
            x (int): x-coordinate on the board
            y (int): y-coordinate on the board

        Attributes updated by this function:
            self.score
            self.territory
        """

        # valid if the game is finished
        if not self.game_over:
            return

        # claim an empty field
        if self.board[y][x] is None:
            # cycle through the colours depending on how the field is currently marked
            # None => Black => White => None
            col_dict = {None:BLACK, BLACK:WHITE, WHITE:None}

            # change the color
            color = col_dict[self.territory[y][x]]

            # recursively claim the fields
            self._claim_empty(x, y, color)

        # claim a group
        else:
            # Choose whether to mark or unmark the group
            if self.territory[y][x] is None:
                color = not self.board[y][x].color
            else:
                color = None

            # recursively claim the fields
            self._claim_group(x, y, color)

        # compute the score
        self._compute_score()

    def find_territory(self):
        """Tries to automatically claim territory for the proper players.

        Current algorithm:
            It just claims empty areas that are completely surrounded
            by one color. Therefore it will not recognise prisoners or dead groups.

        Attributes updated by this function:
            self.score
            self.territory
        """

        # TODO: Update this algorithm to claim fields that are completely surrounded by one color (recognize prisoners and dead groups).

        # Keep track of the checked fields
        covered_area = list()

        for y in range(self.size):
            for x in range(self.size):

                # skip the coordinates if they have already been checked
                if (x, y) in covered_area:
                    continue

                # only check empty fields
                if self.board[y][x] is None:

                    # Find all adjacent empty fields
                    # Count contains the number of adjacent stones of each color.
                    area, count = self._find_empty(x, y, area=covered_area)
                    covered_area += area

                    # claim the territory if black has no adjacent stones
                    if count[BLACK] == 0 and count[WHITE] > 0:
                        self._claim_empty(x, y, WHITE)

                    # claim the territory if white has no adjacent stones
                    elif count[WHITE] == 0 and count[BLACK] > 0:
                        self._claim_empty(x, y, BLACK)

        # compute the score
        self._compute_score()