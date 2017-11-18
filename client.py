#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import pyglet
from pyglet.sprite import Sprite
from graphics import Grid
from graphics import Circle

# constants
BLACK = True
WHITE = False

BLACK_TERRITORY = (255,255,255,255)
WHITE_TERRITORY = (0,0,0,255)

class Window(pyglet.window.Window):
    
    def __init__(self):
        super(Window, self).__init__(700, 700, fullscreen=False, caption='')
        
        # TODO: remove me later
        n = 10
		
        # Gamplay information passed by the controller
        self.data = {'size' : n, #n comes as keyword-argument to __init__()
			'stones' : [[None for x in range(n)] for y in range(n)],
			'territory': [[None for x in range(n)] for y in range(n)],
			'color' : None,
			'game_over': False,
			'score' : [0, 0]}
        
        # Set default background color
        pyglet.gl.glClearColor(0.5,0.5,0.5,1)
        
        # Load background image and stones
        self.image_background = pyglet.resource.image('images/Background.png')
        self.image_black_stone = pyglet.resource.image('images/BlackStone.png')
        self.image_white_stone = pyglet.resource.image('images/WhiteStone.png')
        
        # Initialize the display
        self.init_display()

    def on_draw(self):
        """Draw the interface.
       
        This function should only draw the graphics without
        doing any computations.
        """
        # Clear out old graphics
        self.clear()
        
        # Drawing the batch (which does not contain any graphics yet) [in on_draw()]
        self.batch.draw()

    def on_mouse_press(self, mousex, mousey, button, modifiers):
        """Function called on any mouse button press.

        Arguments:
            mousex    : x-coord of the click
            mousey    : y-coord of the click
            button    :
            modifiers :


        The buttons are saved as constants in pyglet.window.mouse,
        the modifiers under pyglet.window.key

        E.g.
        >>> if button == pyglet.window.mouse.LEFT: pass

        Look at the documentation for more information:
        >>> import pyglet
        >>> help(pyglet.window.mouse)
        """
        if button == pyglet.window.mouse.LEFT:
            # Print mouse coordinates
            #print('Left-click at position x={}, y={}'.format(mousex, mousey))
            pos = self.grid.get_indices(mousex, mousey)
            print('Left-click at field x={}, y={}'.format(pos[0], pos[1]))

    def on_key_press(self, symbol, modifiers):
        """Function that gets called on any key press (keyboard).

        Arguments:
            symbol   : symbol that was pressed
            modifiers : modifiers (e.g. l-shift, r-shift, ctrl, ...)

        You can compare symbol/modifiers to the constants defined
        in pyglet.window.key:

        E.g.
        >>> if symbol == pyglet.window.key.A: pass

        For more information look on the help page:
        >>> import pyglet
        >>> help(pyglet.window.key)
        """
        pass
    
    def update(self, *args):
        """This function does all the calculations when the data gets updated.
        Side note: Has to be called manually.
            For other games that require permanent simulations you would add
            the following line of code at the end of __init__():
            pyglet.clock.schedule_interval(self.update, 1/30)
        """
        if self.data['size'] == self.grid.size:
            self.init_display()
            
        self.batch_stones = pyglet.graphics.Batch()
        self.stone_sprites = []
    
    def init_display(self):
        """Gather all graphical elements together and draw them simutaneously.
        """
        # Creating a batch [in init_display()]
        self.batch = pyglet.graphics.Batch()
        
        # Ordered groups are like different layers inside the batch. The lowest
        # number will be drawn first.
        # Inside a group the order is arbitrary (gives Pyglet the opportunity
        # to optimize).
        self.grp_back = pyglet.graphics.OrderedGroup(0)
        self.grp_grid = pyglet.graphics.OrderedGroup(1)
        self.grp_label = pyglet.graphics.OrderedGroup(2)
        self.grp_stones = pyglet.graphics.OrderedGroup(3)
        self.grp_territory = pyglet.graphics.OrderedGroup(4)
        
        # Display background image
        self.background = Sprite(self.image_background, batch=self.batch, group=self.grp_back)
        
        # Alternative approach to display image
        #self.graphical_obj = []
        #self.graphical_obj.append(Sprite(self.image_background, batch=self.batch, group=self.grp_back))
        
        # Display grid
        scale_factor = 0.75
        self.grid = Grid(x=self.width/2,
                         y=self.height/2,
                         width=self.width*scale_factor,
                         height=self.height*scale_factor,
                         batch=self.batch,
                         group=self.grp_grid,
                         n=self.data['size'])
        
        # Center both black and white stones
        def center_image(image):
            """Sets an image's anchor point to its center"""
            image.anchor_x = image.width/2
            image.anchor_y = image.height/2
            
        center_image(self.image_black_stone)
        center_image(self.image_white_stone)
        
        # Display the stones on the regular batch
        self.batch_stones = self.batch
        self.stone_sprites = []
        
        # TODO: remove this test data set for the stones
        self.data['stones'][1][1] = BLACK
        self.data['stones'][5][3] = BLACK
        self.data['stones'][6][8] = BLACK
        self.data['stones'][2][6] = WHITE
        
        # Iterate trough all data stones and place the corresponding black or
        # white stone on the grid
        scaling = self.grid.field_width / self.image_black_stone.width
        for i in range(0, self.data['size']):
            for j in range(0, self.data['size']):
                if self.data['stones'][j][i] != None:
                    x_coord, y_coord = self.grid.get_coords(i, j)
                    if self.data['stones'][j][i] == BLACK:
                        _s = Sprite(self.image_black_stone,
                                    batch=self.batch_stones,
                                    group=self.grp_stones,
                                    x=x_coord,
                                    y=y_coord)
                    elif self.data['stones'][j][i] == WHITE:
                        _s = Sprite(self.image_white_stone,
                                    batch=self.batch_stones,
                                    group=self.grp_stones,
                                    x=x_coord,
                                    y=y_coord)
                        
                    _s.scale = scaling
                    self.stone_sprites.append(_s)
                    
        
        # TODO: remove this test data set for the territory indicators
        self.data['territory'][5][3] = BLACK
        
        rad = 5
        
        # Iterate trough all territory indicators and place the corresponding
        # black or white circle on the grid or above stones
        for i in range(0, self.data['size']):
            for j in range(0, self.data['size']):
                if self.data['territory'][j][i] != None:
                    x_coord, y_coord = self.grid.get_coords(i, j)
                    if self.data['territory'][j][i] == BLACK:
                        Circle(x_coord,
                               y_coord,
                               color=BLACK_TERRITORY,
                               r=rad,
                               batch=self.batch_stones,
                               group=self.grp_territory)
                    elif self.data['territory'][j][i] == WHITE:
                        Circle(x_coord,
                               y_coord,
                               color=WHITE_TERRITORY,
                               r=rad,
                               batch=self.batch_stones,
                               group=self.grp_territory)
            
# main program
# open the window
if __name__ == '__main__':
    window = Window()
    pyglet.app.run()