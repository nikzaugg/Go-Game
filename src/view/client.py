#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import pyglet

class Window(pyglet.window.Window):
    
    def __init__(self):
        super(Window, self).__init__(700, 700, fullscreen=False, caption='')

    def on_draw(self):
        """Draw the interface.
       
        This function should only draw the graphics without
        doing any computations.
        """
        pass

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
        pass

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

if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
