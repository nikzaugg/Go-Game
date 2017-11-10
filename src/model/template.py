#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
This module contains the example solution for finding marking
the territory and counting the score and a class representing
a stone group.

The game Model needs to inherit from Terr_Template if it does not
implement those methods itself.
"""

class Terr_Template(object):
    """This class does not work on it's own but can be inherited from by
    the Model."""
    
    def find_territory(self):
        """Tries to automatically claim territory for the proper players.

        Current algorithm:
            It just claims empty areas that are completely surrounded
            by one color.
            Therefore it will not recognise prisoners or dead groups.

        Attributes updated by this function:
            self.score
            self.territory
        """

        # Keep track of the checked fields
        area = []
        for y in range(self.size):
            for x in range(self.size):

                if (x, y) in area:
                    continue

                # Only look at empty fields
                if self.board[y][x] is None:
                    # Find all adjacent empty fields
                    # Count contains the number of adjacent stones
                    # of each color.
                    _a, count = self._find_empty(x, y, area=area)
                    area += _a

                    # Claim the territory if one color has no
                    # stones adjacent
                    if count[BLACK] == 0 and count[WHITE] > 0:
                        self._claim_empty(x, y, WHITE)
                    elif count[WHITE] == 0 and count[BLACK] > 0:
                        self._claim_empty(x, y, BLACK)

        # Recompute the score
        self._compute_score()

    def mark_territory(self, x, y):
        """Function that can be evoked by user to claim territory for
        one player.
        For empty fields it will also mark all adjacent empty fields,
        for fields that contain a stone it will mark the entire stone
        group and all adjacent empty spaces.

        Arguments:
            x, y (int): coordinates of the field

        Attributes updated by this function:
            self.score
            self.territory
        """

        # Only valid when the game is over
        if not self.game_over:
            return

        # Claim an empty field
        if self.board[y][x] is None:
            # Cycle through the colours depending on how the
            # field is currently marked
            col_dict = {None:BLACK, BLACK:WHITE, WHITE:None}
            color = col_dict[self.territory[y][x]]
            # Start recursively claim the fields
            self._claim_empty(x, y, color)

        # Claim a group
        else:
            # Choose whether to mark or unmark the group
            if self.territory[y][x] is None:
                color = not self.board[y][x].color
            else:
                color = None
            # Start recursively claim the fields
            self._claim_group(x, y, color)

        # Recompute the score
        self._compute_score()

        def _claim_empty(self, x, y, color, area=None):
            """First part of the recursive claim function, which claims
            an empty field and then tries to claim all adjacent fields, too.

            Arguments:
                x, y (int)       : coordinates
                color (bool/None): The color which the territory should
                                   be claimed for.
                area (list)      : For recursion to keep track of visited fields.

            Attributes updated by this function:
                self.territory
            """

            # Don't do that in the function definition, because then you get
            # a weird behaviour (mutable obj) and area will not be empty
            # when you expect it to be.
            if area is None:
                area = []

            # Stop recursion
            if self.board[y][x] is not None or (x, y) in area:
                return

            # Claim field
            area.append((x, y))
            self.territory[y][x] = color

            # Go recursively over all adjacent fields
            for (u, v) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:

                # Not on the board
                if u < 0 or v < 0 or u >= self.size or v >= self.size:
                    continue

                # Only claim adjacent empty fields
                if (u, v) not in area and self.board[v][u] is None:
                    self._claim_empty(u, v, color, area=area)

    def _claim_empty(self, x, y, color, area=None):
        """First part of the recursive claim function, which claims
        an empty field and then tries to claim all adjacent fields, too.

        Arguments:
            x, y (int)       : coordinates
            color (bool/None): The color which the territory should
                               be claimed for.
            area (list)      : For recursion to keep track of visited fields.

        Attributes updated by this function:
            self.territory
        """

        # Don't do that in the function definition, because then you get
        # a weird behaviour (mutable obj) and area will not be empty
        # when you expect it to be.
        if area is None:
            area = []

        # Stop recursion
        if self.board[y][x] is not None or (x, y) in area:
            return

        # Claim field
        area.append((x, y))
        self.territory[y][x] = color

        # Go recursively over all adjacent fields
        for (u, v) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:

            # Not on the board
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue

            # Only claim adjacent empty fields
            if (u, v) not in area and self.board[v][u] is None:
                self._claim_empty(u, v, color, area=area)

    def _claim_group(self, x, y, color, area=None):
        """Second part of the recursive claim function, which claims
        a group for the enemies team (dead stones) and the also
        claims all adjacent empty spaces.

        Arguments:
            x, y (int)       : coordinates
            color (bool/None): The color which the territory should
                               be claimed for.
            area (list)      : For recursion to keep track of visited
                               fields.

        Attributes updated by this function:
            self.territory
        """
        if area is None:
            area = []
        # Claim the group
        for u, v in self.board[y][x].stones:
            if (u, v) not in area:
                area.append((u, v))
                self.territory[v][u] = color
        # Go recursively over all adjacent fields
        # (in the border of the group)
        for u, v in self.board[y][x].border:
            # Claim all empty adjacent fields
            if self.board[v][u] is None and (u, v) not in area:
                self._claim_empty(u, v, color, area=area)

    def _compute_score(self):
        """Computes the score of the players from the current
        territory and the player's prisoners.
        Set:
            self.score (list): sum of prisoners and number of coloured
                               territory fields
        """
        self.score = [0, 0]
        for j in range(self.size):
            for i in range(self.size):
                # Count black territory
                if self.territory[j][i] == BLACK:
                    self.score[BLACK] += 1
                    # Additional point for dead stones inside the territory
                    if self.board[j][i] is not None:
                        self.score[BLACK] += 1
                # Count white territory
                elif self.territory[j][i] == WHITE:
                    self.score[WHITE] += 1
                    # Additional point for dead stones inside the territory
                    if self.board[j][i] is not None:
                        self.score[WHITE] += 1

    def _find_empty(self, x, y, area=None, count=None):
        """ Finds all connected empty fields starting at (x, y) and
        counts the number of  adjacent stones of each color

        Returns:
            area (list) : List of empty fields
            count (list): Number of adjacent stones to the[black, white]

        Known bug:
            stones are counted several times if more than one
            empty field is adjacent to them
        """
        if area is None:
            area = []
        if count is None:
            count = [0, 0]
        # Stop recursion
        if self.board[y][x] is not None or (x, y) in area:
            return area, count
        area.append((x, y))
        # Look at al neighbours
        for (u, v) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            # Not on the board
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue
            # Go recursively over empty fields and add adjacent stones
            if (u, v) not in area:
                if self.board[v][u] is None:
                    self._find_empty(u, v, area=area, count=count)
                else:
                    count[self.board[v][u].color] += 1
        return area, count


class Grp_Template(object):
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


class Group(object):
    """Represents a group of connected stones on the board.

    Attributes:
        stones (set): list of all coordinates where the group has a stone
        border (set): list of all fields that are adjacent to the group
                      For a new group empty fields must be added manually
                      since the group does not know about the field size
        color (bool): color of the group

    Property:
        size (int): equal to len(self.stones), the number of stones in
                    the group.
    """

    def __init__(self, stones=None, color=None):
        """
        Initialise group
        """
        if stones is not None:
            self.stones = set(stones)
        else:
            self.stones = set()

        self.border = set()
        self.color = color

    def __add__(self, other):
        """To add two groups of the same color
        The new group contains all the stones of the previous groups and
        the border will be updated correctly.

        Raises:
            TypeError: The colours of the groups do not match
        """
        if self.color != other.color:
            raise ValueError('Only groups of same colour can be added!')
        grp = Group(stones=self.stones.union(other.stones))
        grp.color = self.color
        grp.border = self.border.union(other.border).difference(grp.stones)
        return grp

    @property
    def size(self):
        """Size of the group"""
        return len(self.stones)

