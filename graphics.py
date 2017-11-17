#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
This module contains some simple graphical elements such as
Buttons, Disks and the Go Grid to use them in Pyglet.
"""

import pyglet
import math

class Button(object):
    """Simple implementation of a button in pyglet.
    
    You can check if the button has been clicked like in
    the following example:
    >>> button = Button(pos=(100,100), size=(100,30), text='Click me!')
    >>> if (mousex, mousey) in button:
    >>>     print('The button has been clicked.')
    
    If there is a batch specified, it will be added to that one with
    ordering priority around 100.
    Otherwise, it can be drawn later with the .draw() method.
    """
    grp_label = pyglet.graphics.OrderedGroup(101)
    grp_button = pyglet.graphics.OrderedGroup(100)

    def __init__(self, pos=(100, 100), size=(100, 30), text='Button',
                 align='center', batch=None, **kwargs):
        """
        Arguments:
            pos (2-tuple) : (x, y) position of the anchor of the button.
            size (2-tuple): (x, y) size of the button.
            text (str)    : text displayed on the button.
            align (str)   : alignment of the button relative to the
                            anchor either 'center' or combination of
                            'left'/'right' or 'top'/'bottom'.
                            E.g. 'center','left', 'topright', 'bottomright'
            batch (pyglet.graphics.Batch):
                            pyglet batch where the button should be added to.
            **kwargs      : Further graphical options
                'label_color' (4-tuple): RGBA colors from 0 to 255
        """
        # Start and ending position of the button's rectangle
        self.x = [0, 0]
        self.y = [0, 0]

        if batch is None:
            self.batch = pyglet.graphics.Batch()
        else:
            self.batch = batch

        # Alignment of the button
        if 'top' in align:
            self.y = [pos[1]-size[1], pos[1]]
        elif 'bottom' in align:
            self.y = [pos[1], pos[1]+size[1]]
        else:
            self.y = [pos[1]-size[1]//2, pos[1]+size[1]//2]

        if 'right' in align:
            self.x = [pos[0]-size[0], pos[0]]
        elif 'left' in align:
            self.x = [pos[0], pos[0]+size[0]]
        else:
            self.x = [pos[0]-size[0]//2, pos[0]+size[0]//2]


        # Creating the rectangle
        pos = [self.x[0], self.y[0], self.x[1], self.y[0],
               self.x[1], self.y[1], self.x[0], self.y[1]]
        self.background = self.batch.add(4, pyglet.gl.GL_QUADS, self.grp_button, ('v2f', pos),
                                    ('c3f', [.8 for _ in range(12)]))
        pos = [self.x[0], self.y[0], self.x[1], self.y[0], self.x[1], self.y[0],
               self.x[1], self.y[1], self.x[1], self.y[1], self.x[0], self.y[1],
               self.x[0], self.y[1], self.x[0], self.y[0]]
        self.batch.add(8, pyglet.gl.GL_LINES, self.grp_button, ('v2f', pos),
                                    ('c3f', [0 for _ in range(24)]))

        # Creating the label
        self.label = pyglet.text.Label(x=self.x[0]+size[0]//2,
                                       y=self.y[0]+size[1]//2, text=text,
                                       color=kwargs.get('label_color', (0, 0, 0, 255)),
                                       batch=self.batch, group=self.grp_label,
                                       anchor_x='center',
                                       font_size=min(size[0]//len(text),
                                                     size[1]//2),
                                       anchor_y='center')

    def __contains__(self, coords):
        """Returns: True if other is a position tuple (x, y) that lies
        inside the button.

        Can be used to check for pushing the button.
        
        Arguments:
            coords (2-tuple): Coordinates that are tested if they lie inside
                             the button.
        
        Returns:
            (bool): True if coords are inside the button's area.
        """
        try:
            if (coords[0] >= self.x[0] and coords[0] <= self.x[1] and
                    coords[1] >= self.y[0] and coords[1] <= self.y[1]):
                return True
        except (IndexError, TypeError):
            pass
        return False

    def draw(self):
        self.batch.draw()

class Grid(object):
    """Graphical object representing a grid for the Go board game including
    the hoshi points.
    """

    def __init__(self, x, y, n=19, width=None, height=None,
                 color=(0, 0, 0, 255), align='center',
                 batch=None, group=None):
        """
        
        Arguments:
            x, y (float)          : position (anchor) of the grid
            n (int)               : size of the (n x n) grid.
                                    (default: 19)
            width, height (int)   : width, height of the grid in pixels.
                                    If only one is specified, the other will
                                    default to the set one.
                                    (default: 100)
            color (4-tuple of int): RGBA (each 0-255) value of the color
            algin (str)           : 
            batch (Batch)         : 
            group (Group)         : 
        """

        if batch is None:
            raise ValueError('You must specify a pyglet batch for the grid!')

        # Add opacity value
        col = [i/255. for i in color]
        if len(col) == 3:
            col.append(1)

        # Default values for width / height
        if width is None and height is not None:
            width = height
        elif height is None and width is not None:
            height = width
        elif width is None and height is None:
            width = height = 100

        self.width = width
        self.height = height
        self.size = n

        # Alignment of the grid
        if 'top' in align:
            self.y0 = y-height
        elif 'bottom' in align:
            self.y0 = y
        else:
            self.y0 = y - height//2

        if 'right' in align:
            self.x0 = x-width
        elif 'left' in align:
            self.x0 = x
        else:
            self.x0 = x-width//2

        # self.x = [x0 + i*width/n for i in range(n)]
        # self.y = [y0 + i*height/n for i in range(n)]

        # Creating the endpoints of the lines
        pos = sum([[self.x0 + (i//2)*self.field_width, self.y0 + (i%2)*height] for i in range(2*n)] +
                  [[self.x0 + (i%2)*width, self.y0 + (i//2)*self.field_height] for i in range(2*n)], [])

        # drawing the grid
        batch.add(4*n, pyglet.gl.GL_LINES, group, ('v2f', pos),
                       ('c4f', sum([list(col) for _ in range(4*n)], [])))

        # Additional: Hoshi points
        # ------------------------

        if n >= 7:
            # If n >= 13 the corner hoshi points are on the 4th diag. point
            # else they're on the 3rd one.
            if n >= 13:
                q = 1
            else:
                q = 0

            # Adding coords. for the corner hoshi points
            points = [(self.x0 + i*self.field_width, self.y0 + j*self.field_height)
                      for i, j in [(2+q, 2+q), (2+q, n-3-q), (n-3-q, n-3-q),
                                    (n-3-q, 2+q)]]

            if n%2 == 1:
                # Add hoshi points in the very center
                if n >= 9:
                    points.append((self.x0 + (n//2)*self.field_width, self.y0 + (n//2)*self.field_height))
                # Add hoshi points in the middle of each edge
                if n >= 15:
                    points += [(self.x0 + i*width/(n-1), self.y0 + j*height/(n-1))
                               for i, j in [(2+q, n//2), (n//2, n-3-q), (n-3-q, n//2), (n//2, 2+q)]]

            for u, v in points:
                Circle(u, v, r=3, n=32, color=color, batch=batch, group=group)

    def get_indices(self, x, y):
        """
        Arguments:
            x, y (floats): mouse position in the window

        Returns:
            i, j (ints): indices of the clicked grid point.
                         Returns None if out of bounds.
        """

        i_x = int(round((x-self.x0)/self.field_width))
        i_y = int(round((y-self.y0)/self.field_height))
        if i_x >= 0 and i_x < self.size and i_y >= 0 and i_y < self.size:
            return (i_x, i_y)
        else:
            return None

    def get_coords(self, i, j):
        """Takes indices (i, j) and returns the coordinates of that point"""
        return (self.x0 + i*self.field_width,
                self.y0 + j*self.field_height)

    @property
    def field_width(self):
        return self.width/(self.size-1.)

    @property
    def field_height(self):
        return self.height/(self.size-1.)

class Circle(object):
    """Draw a filled disk (circle) and add it to a pyglet batch."""

    def __init__(self, x, y, r=10, n=10, color=(0, 0, 0, 255), batch=None, group=None):
        """
        Arguments:
            x, y (float) : position of the circle
            r (float)    : radius
            n (int)      : number of edges of the circle
            color (4-tuple of int):
                           RGBA value (each 0-255) for the circle.
                           (default: (0, 0, 0, 255)) 
            batch (Batch): pyglet.graphics.Batch where the circle should 
                           be added to.
            group (Group): pyglet.graphics.OrderedGroup where the circle
                           should be added.
                           (default: None)
            
        Raises:
            ValueError: argument batch must be a existing pyglet batch
        """

        if batch is None:
            raise ValueError('You must specify a pyglet batch for the circle!')

        # Add opacity value
        color = [i/255. for i in color]
        if len(color) == 3:
            color.append(1)

        # Positions of multiple triangles from the center to the vertices of
        # of the circle.
        pos = sum([[x, y,
                    x + r*math.cos(i*2*math.pi/n), y + r*math.sin(i*2*math.pi/n),
                    x + r*math.cos((i+1)*2*math.pi/n), y + r*math.sin((i+1)*2*math.pi/n)]
                   for i in range(n+1)], [])
        # Draw filled circle.
        batch.add(3*(n+1), pyglet.gl.GL_TRIANGLES, group, ('v2f', pos),
                  ('c4f', sum([color for _ in range(3*(n+1))], [])))



