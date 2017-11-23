#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Author: Alex Scheitlin & Nik Zaugg

# View part of the MVC architecture for an implementation of the Go game

import pyglet
from pyglet.sprite import Sprite
from pyglet.text import Label
from graphics import Grid
from graphics import Button
from graphics import Circle
import controller

# constants
BLACK = True
WHITE = False

BLACK_TERRITORY = (0, 0, 0, 255)
WHITE_TERRITORY = (255, 255, 255, 255)

MAX_STONE_SCALING = 0.6     # 1 is original size
MAX_GRID_SIZE = 0.7         # 1 is full size of window
LITTLE_STONE_SIZE = 0.2

# resources
BACKGROUND = pyglet.resource.image('images/Background.png')
BLACK_STONE = pyglet.resource.image('images/BlackStone.png')
WHITE_STONE = pyglet.resource.image('images/WhiteStone.png')

class Window(pyglet.window.Window):
    """This class renders the game data within a pyglet window."""

    def __init__(self, my_controller, size):
        super(Window, self).__init__(700, 700, fullscreen=False, caption='')
        
        # Link the view to the controller
        self.controller = my_controller
		
        # Gamplay information passed by the controller
        self.data = {   'size' : size,
                        'stones' : [[None for x in range(size)] for y in range(size)],
                        'territory': [[None for x in range(size)] for y in range(size)],
                        'color' : None,
                        'game_over': False,
                        'score' : [0, 20]
                        }
        
        # Set default background color
        pyglet.gl.glClearColor(0.5,0.5,0.5,1)
        
        # Load background image and stones
        self.image_background = BACKGROUND
        self.image_black_stone = BLACK_STONE
        self.image_white_stone = WHITE_STONE

        # Center black and white stones
        self.init_resources()
        
        # Initialize the display
        self.init_display()

    def init_resources(self):
        """Center black and whtie stones for proper visualization

        Attributes updated by this function:
            self.image_black_stone
            self.image_white_stone
        """
        def center_image(image):
            """Set an image's anchor point to its center

            Arguments:
                image (pyglet.resource.image) - image to center

            Attributes updated by this function:
                image
            """
            image.anchor_x = image.width/2
            image.anchor_y = image.height/2
            
        center_image(self.image_black_stone)
        center_image(self.image_white_stone)

    def init_display(self):
        """Gather all graphical elements together and draw them simutaneously.

            Attributes updated by this function:
                self.batch
                self.grp_back
                self.grp_grid
                self.grp_label
                self.grp_stones
                self.grp_territory
                self.background
                self.grid
                self.info
                self.score_black
                self.black_label_stone
                self.score_white
                self.white_label_stone
                self.player_color
                self.current_player_stone
                self.button_pass
                self.button_newgame
        """
        # Creating a batch to display all graphics
        self.batch = pyglet.graphics.Batch()
        
        # Graphic groups (groups of lower index get drawn first)
        self.grp_back = pyglet.graphics.OrderedGroup(0)
        self.grp_grid = pyglet.graphics.OrderedGroup(1)
        self.grp_label = pyglet.graphics.OrderedGroup(2)
        self.grp_stones = pyglet.graphics.OrderedGroup(3)
        self.grp_territory = pyglet.graphics.OrderedGroup(4)

        # Initially load all graphic groups.
        self.init_back()
        self.init_grid()
        self.init_label()

    def init_back(self):
        """Load the background.

            Attributes updated by this function:
                self.background
        """
        # Display background image
        self.background = Sprite(self.image_background, batch=self.batch, group=self.grp_back)

    def init_grid(self):
        """Load the grid.

            Attributes updated by this function:
                self.grid
        """
        # Display grid
        self.grid = Grid(x=self.width/2,
                         y=self.height/2,
                         width=self.width*MAX_GRID_SIZE,
                         height=self.height*MAX_GRID_SIZE,
                         batch=self.batch,
                         group=self.grp_grid,
                         n=self.data['size'])

    def init_label(self):
        """Load all labels and buttons.

            Attributes updated by this function:
                self.info
                self.score_black
                self.black_label_stone
                self.score_white
                self.white_label_stone
                self.player_color
                self.current_player_stone
                self.button_pass
                self.button_newgame
        """
        # Game Information Display
        label_y = 670                 # y position of scores and next turn labels
        label_font_size = 12
        label_text_color = (0, 0, 0, 255)
        
        # Controller-Info Panel
        # The Text of this label is directly changed inside the controller
        self.info = Label(x=10, y=10, text="Let's start!", color=label_text_color,
                          font_size=label_font_size, batch=self.batch, group=self.grp_label)

        # Score-Label
        Label(x=10, y=label_y, text='Score:', color=label_text_color,
                          font_size=label_font_size, bold=True, batch=self.batch, group=self.grp_label)

        # SCORES BLACK PLAYER
        self.score_black = Label(x=100, y=label_y, text=str(self.data['score'][1]), color=label_text_color,
                          font_size=label_font_size, batch=self.batch, group=self.grp_label)
        self.black_label_stone = Sprite(self.image_black_stone,
                           batch=self.batch, group=self.grp_label,
                           x=0, y=0)
        self.black_label_stone.scale = LITTLE_STONE_SIZE
        self.black_label_stone.set_position(80, label_y + self.black_label_stone.height/4)

        # SCORES WHITE PLAYER
        self.score_white = Label(x=170, y=label_y, text=str(self.data['score'][0]), color=label_text_color,
                          font_size=label_font_size, batch=self.batch, group=self.grp_label)
        self.white_label_stone = Sprite(self.image_white_stone,
                           batch=self.batch, group=self.grp_label,
                           x=0, y=0)
        self.white_label_stone.scale = LITTLE_STONE_SIZE
        self.white_label_stone.set_position(150, label_y + self.white_label_stone.height/4)

        # CURRENT PLAYER STONE
        self.player_color = Label(x=550, y=label_y, text="Your color: ", color=label_text_color,
            font_size=label_font_size, bold=True, batch=self.batch, group=self.grp_label)

        # INITIAL PLAYER STONE
        self.current_player_stone = Sprite(self.image_black_stone,
                           batch=self.batch, group=self.grp_label,
                           x=0, y=0)
        self.current_player_stone.scale = LITTLE_STONE_SIZE
        self.current_player_stone.set_position(660, label_y + self.current_player_stone.height/4)

        # Game Buttons  
        # Button that can be pressed to pass on current round
        self.button_pass = Button(pos=(600,40), text='Pass', batch=self.batch)
        
        # New-Game Button
        self.button_newgame = Button(pos=(480,40), text='New Game')

    def update(self, *args):
        """This function does all the calculations when the data gets updated.
            For other games that require permanent simulations you would add
            the following line of code at the end of __init__():
            pyglet.clock.schedule_interval(self.update, 1/30)

            Attributes updated by this function:
                self.batch_stones
                self.stone_sprites
                self.image_black_stone
                self.image_white_stone
                self.batch_territory
                self.score_black
                self.score_white
                self.current_player_stone
        """
        # Game Information Updates
        # Scores of each player
        self.update_stones()
        self.update_territories()
        self.update_scores()
        self.update_current_player()
            
        # If the new size in the data is different than the current size
        if self.data['size'] != self.grid.size:
            self.init_display()
    
    def update_stones(self):
        """Update the black and white stones on the game board.

            Attributes updated by this function:
                self.batch_stones
                self.stone_sprites
                self.image_black_stone
                self.image_white_stone
        """
        # Display the stones on the regular batch
        self.batch_stones = self.batch
        self.stone_sprites = []

        # Center black and white stones
        def center_image(image):
            """Sets an image's anchor point to its center"""
            image.anchor_x = image.width/2
            image.anchor_y = image.height/2
            
        center_image(self.image_black_stone)
        center_image(self.image_white_stone)

        # Place all stones on the grid

        # Scale stone images
        scaling = self.grid.field_width / self.image_black_stone.width

        # Limit max size of stones
        if scaling > MAX_STONE_SCALING:
            scaling = MAX_STONE_SCALING

        # Iterate trough all data stones and place the corresponding black or
        # white stone on the grid
        for i in range(0, self.data['size']):
            for j in range(0, self.data['size']):
                if self.data['stones'][j][i] != None:
                    # Get x and y grid coordinates
                    x_coord, y_coord = self.grid.get_coords(i, j)

                    # Get the stone color to place
                    stone_color = self.image_black_stone if self.data['stones'][j][i] == BLACK else None
                    stone_color = self.image_white_stone if self.data['stones'][j][i] == WHITE else stone_color

                    # Place the stone on the grid
                    if stone_color:
                        _s = Sprite(stone_color,
                                    batch=self.batch_stones,
                                    group=self.grp_stones,
                                    x=x_coord,
                                    y=y_coord)
                        _s.scale = scaling
                        self.stone_sprites.append(_s)   
    
    def update_territories(self):
        """Update the black and white territories on the board.

            Attributes updated by this function:
                self.batch_territory
        """
        # Display the territory an the regular batch
        # Display the stones on the regular batch
        self.batch_territory = self.batch
        
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
                               batch=self.batch_territory,
                               group=self.grp_territory)
                    elif self.data['territory'][j][i] == WHITE:
                        Circle(x_coord,
                               y_coord,
                               color=WHITE_TERRITORY,
                               r=rad,
                               batch=self.batch_territory,
                               group=self.grp_territory)

    def update_scores(self):
        """Update scores for BLACK and WHITE.
        
            Attributes updated by this function:
                self.score_black
                self.score_white
        """
        self.score_black.text = str(self.data['score'][1])
        self.score_white.text = str(self.data['score'][0])

    def update_current_player(self):
        """Update stone of current player.
        
            Attributes updated by this function:
                self.current_player_stone
        """
        # Remve the last current player stone
        self.current_player_stone.delete()

        # If its the BLACK players turn
        if self.data['color']:
            self.current_player_stone = Sprite(self.image_black_stone,
                           batch=self.batch, group=self.grp_label,
                           x=0, y=0)
            self.current_player_stone.scale = LITTLE_STONE_SIZE
            self.current_player_stone.set_position(660, 670 + self.current_player_stone.height/4)
        # If its the WHITE players turn
        else:
            self.current_player_stone = Sprite(self.image_white_stone,
                           batch=self.batch, group=self.grp_label,
                           x=0, y=0)
            self.current_player_stone.scale = LITTLE_STONE_SIZE
            self.current_player_stone.set_position(660, 670 + self.current_player_stone.height/4)


    def on_draw(self):
        """Draw the interface.
        
            Attributes updated by this function:
                self
                self.batch
                self.button_newgame
        """
        # Clear out old graphics
        self.clear()

        # Drawing the batch (which does not contain any graphics yet)
        self.batch.draw()

        # Check if Game is over, if True, draw the New Game Button
        if(self.data['game_over']):
            self.button_newgame.draw()

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
        # Check for clicks on New Game Button only when game is Over
        if(self.data['game_over']):
            if (mousex, mousey) in self.button_newgame:
                self.controller.new_game()
                
            if button == pyglet.window.mouse.LEFT:
                # Mark territory if the game is over
                pos = self.grid.get_indices(mousex, mousey)
                if pos != None:
                    self.controller.mark_territory(pos)

        # Handle clicks during game
        
        # Check if pass-button was pressed
        if (mousex, mousey) in self.button_pass:
            self.controller.passing()

        # Grid position clicked (only if above buttons)
        elif button == pyglet.window.mouse.LEFT and mousey > 60:
            # Place a stone at clicked position
            pos = self.grid.get_indices(mousex, mousey)
            if pos != None:
                self.controller.play(pos)

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
    
    def receive_data(self, data):
        """Receive data from the controller and update view.
        
            Attributes updated by this function:
                self.data
        """
        self.data.update(data)
        self.update()

    def new_game(self, data):
        """Receive data from the controller and start a new game.
        
            Attributes updated by this function:
                self.data
        """
        # Initialize the display
        self.data.update(data)
        self.init_display()
        self.update()
         
# main program
# open the window
if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
