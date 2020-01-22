"""
Author: Trevor Stalnaker, Justin Pusztay
File: popup.py

A class that models hover over pop ups
"""

import pygame
from .textbox import TextBox
from .mysurface import MySurface
from modules import Drawable

def makeMultiLineTextBox(text, position, font, color, backgroundColor):
    """
    Used to create multiline text boxes which are not native to
    pygame.  The user supplies the same information to this function
    that they would supplied to the TextBox Class. The function will
    split the text along new-lines and return a MySurface object
    containing all of the text formatted as desired.

    ## This is replicated here because the import statements refused to
    cooperate (ie nothing works in combat)
    """
    lines = text.split("\n")
    width = TextBox(max(lines, key=len),position, font, color).getWidth() + 10
    height = font.get_height()
    surf = pygame.Surface((width,height*len(lines)))
    surf.fill(backgroundColor)
    p = (0,0)
    for line in lines:
        t = TextBox(line, p, font, color)
        center = width // 2 - t.getWidth() // 2
        t.setPosition((center, t.getY()))
        t.draw(surf)
        p = (0, p[1] + height)
    return MySurface(surf, position)

class Popup(Drawable):

    def __init__(self, text, position, font,
                 color=(0,0,0), backgroundColor=(255,255,255),
                 borderColor=(0,0,0), borderWidth=1, margin=2,multiLine = False):
        """Initializes the widget with a variety of parameters"""
        super().__init__("", position, worldBound=False)
        if multiLine == True:
            self._textbox = makeMultiLineTextBox(text,(0,0),font,color,backgroundColor)
        else:
            self._textbox = TextBox(text, (0,0), font, color)
        self._backgroundColor = backgroundColor
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._width = self._textbox.getWidth() + (margin * 2)
        self._height = self._textbox.getHeight() + (margin * 2)
        self.__updatePopup()

    def __updatePopup(self):
        """Update the pop up after parameters have been changed"""
        surfBack = pygame.Surface((self._width+(self._borderWidth*2),
                                   (self._height+(self._borderWidth*2))))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width, self._height))
        surf.fill(self._backgroundColor)
        y_pos = (self._height // 2) - (self._textbox.getHeight() // 2)
        x_pos = (self._width // 2) - (self._textbox.getWidth() // 2)
        self._textbox.setPosition((x_pos, y_pos))
        self._textbox.draw(surf)
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
