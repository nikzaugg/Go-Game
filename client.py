#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

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

BLACK_TERRITORY = (255, 255, 255, 255)
WHITE_TERRITORY = (0, 0, 0, 255)

MAX_STONE_SCALING = 0.6     # 1 is original size
MAX_GRID_SIZE = 0.7         # 1 is full size of window
LITTLE_STONE_SIZE = 0.2

class Window(pyglet.window.Window):
    """Render the game data within a pyglet window."""

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
                    self.controller.mark_territory()

        # Handle cliucks during game
        
        # Check if pass-button was pressed
        if (mousex, mousey) in self.button_pass:
            self.controller.passing()

        # Grid position clicked
        if button == pyglet.window.mouse.LEFT:
            # Place a stone at clicked position
            pos = self.grid.get_indices(mousex, mousey)
            if pos != None:
                # TODO: remove print statement once everything is integrated
                # print('Left-click at field x={}, y={}'.format(pos[0], pos[1]))
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
    
    def update(self, *args):
        """This function does all the calculations when the data gets updated.
            For other games that require permanent simulations you would add
            the following line of code at the end of __init__():
            pyglet.clock.schedule_interval(self.update, 1/30)
        """
        # Game Information Updates
        # Scores of each player
        self.update_scores()
            
        self.batch_stones = pyglet.graphics.Batch()
        self.stone_sprites = []

        if self.data['size'] == self.grid.size:
            self.init_display()
    
    def init_display(self):
        """Gather all graphical elements together and draw them simutaneously.
        """
        # Creating a batch to display all graphics
        self.batch = pyglet.graphics.Batch()
        
        # Graphic groups (groups of lower index get drawn first)
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
        self.grid = Grid(x=self.width/2,
                         y=self.height/2,
                         width=self.width*MAX_GRID_SIZE,
                         height=self.height*MAX_GRID_SIZE,
                         batch=self.batch,
                         group=self.grp_grid,
                         n=self.data['size'])
        
        # Game Information Display
        label_y = 670                 # y position of scores and next turn labels
        label_font_size = 12
        label_text_color = (0, 0, 0, 255)
        
        # Controler-Info Panel
        # The Text of this label is directly changed inside the controller
        self.info = Label(x=10, y=10, text="Welcome!", color=label_text_color,
                          font_size=label_font_size, batch=self.batch, group=self.grp_label)
        
        # Score-Label
        Label(x=10, y=label_y, text='Score:', color=label_text_color,
                          font_size=label_font_size, bold=True, batch=self.batch, group=self.grp_label)

        # Scores for BLACK and WHITE
        self.score_black = Label(x=100, y=label_y, text=str(self.data['score'][1]), color=label_text_color,
                          font_size=label_font_size, batch=self.batch, group=self.grp_label)
        self.score_white = Label(x=170, y=label_y, text=str(self.data['score'][0]), color=label_text_color,
                          font_size=label_font_size, batch=self.batch, group=self.grp_label)



        # Create little black stones to use them for labels and current player indicator
        # BLACK label stone
        self.black_label_stone = Sprite(self.image_black_stone,
                           batch=self.batch, group=self.grp_label,
                           x=0, y=0)
        self.black_label_stone.scale = LITTLE_STONE_SIZE

        # WHITE label stone
        self.white_label_stone = Sprite(self.image_white_stone,
                           batch=self.batch, group=self.grp_label,
                           x=0, y=0)
        self.white_label_stone.scale = LITTLE_STONE_SIZE

        # BLACK current player stone
        self.black_current_stone = Sprite(self.image_black_stone,
                           batch=self.batch, group=self.grp_label,
                           x=0, y=0)
        self.black_current_stone.scale = LITTLE_STONE_SIZE

        # WHITE current stone
        self.white_current_stone = Sprite(self.image_white_stone,
                           batch=self.batch, group=self.grp_label,
                           x=0, y=0)
        self.white_current_stone.scale = LITTLE_STONE_SIZE

        # Stone label for scores
        self.label_stones = []
        # BLACK stone for score label
        black_label = self.black_label_stone
        black_label.set_position(80, label_y + self.image_black_stone.height*LITTLE_STONE_SIZE/4)
        self.label_stones.append(black_label)

        # WHITE stone for score label
        white_label = self.white_label_stone
        white_label.set_position(150, label_y + self.image_white_stone.height*LITTLE_STONE_SIZE/4)
        self.label_stones.append(white_label)

        # Player Color Label
        self.player_color = Label(x=550, y=label_y, text="Your color: ", color=(0, 0, 0, 255),
            font_size=label_font_size, bold=True, batch=self.batch, group=self.grp_label)
        
        # Set position of current player stones
        self.black_current_stone.set_position(660, label_y + self.image_white_stone.height*LITTLE_STONE_SIZE/4)
        self.white_current_stone.set_position(660, label_y + self.image_white_stone.height*LITTLE_STONE_SIZE/4)

        # Display current player
        self.label_current_player = []
        self.update_current_player()

        # Game Buttons
        # Button that can be pressed to pass on current round
        self.button_pass = Button(pos=(600,40), text='Pass', batch=self.batch)

        # New-Game Button
        self.button_newgame = Button(pos=(480,40), text='New Game')
        
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

        self.update_stones_on_grid()
        
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


    def update_stones_on_grid(self):
        """Place all stones on the grid"""
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

    def update_scores(self):
        """Update scores for BLACK and WHITE."""
        self.score_black.text = str(self.data['score'][1])
        self.score_white.text = str(self.data['score'][0])

    def update_current_player(self):
        """"""
        current_stone = self.black_current_stone if self.data['color'] == BLACK else self.white_current_stone
        self.label_current_player = current_stone


    def receive_data(self, data):
        """Receive data from the controller and update view"""
        self.data.update(data)
        self.update()
         
# main program
# open the window
if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
