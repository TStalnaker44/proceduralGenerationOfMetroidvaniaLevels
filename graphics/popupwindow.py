"""
Author: Trevor Stalnaker
File: popupwindow.py

A class that models and manages a pop up notification window
"""

import pygame
from modules.drawable import Drawable
from graphics.window import Window
from graphics.textbox import TextBox
from graphics.button import Button
from graphics.guiUtils import makeMultiLineTextBox

class PopupWindow(Drawable, Window):

    def __init__(self, text, position, dimensions, font, fontColor,
                 backgroundColor, buttonColor, buttonDimensions, buttonFont,
                 buttonFontColor, buttontext="OK", buttonBorderWidth=1,
                 buttonBorderColor=(0,0,0), borderWidth=0, borderColor=(0,0,0)):
        """Initializes the widget with a variety of parameters"""
        Drawable.__init__(self, "", position, worldBound=False)
        Window.__init__(self)
        self._height = dimensions[1]
        self._width = dimensions[0]
        self._text = text
        self._font = font
        self._fontColor = fontColor
        self._backgroundColor = backgroundColor
        self._borderWidth = borderWidth
        self._borderColor = borderColor

        self._offset = position

        self._confirmed = None

        # Create the textbox
##        self._t = TextBox(self._text, (0,0), self._font, self._fontColor)
        self._t = makeMultiLineTextBox(self._text, (0,0), self._font,
                                       self._fontColor, self._backgroundColor)
        y_pos = (self._height // 4) - (self._t.getHeight() // 2)
        x_pos = (self._width // 2) - (self._t.getWidth() // 2)
        self._t.setPosition((x_pos, y_pos))
        
        # Create the Okay button
        self._b = Button(buttontext, (0,0), buttonFont, buttonFontColor,
                         buttonColor,buttonDimensions[1],
                         buttonDimensions[0],buttonBorderColor, buttonBorderWidth)
        y_pos = (3*(self._height // 4)) - (self._b.getHeight() // 2)
        x_pos = (self._width // 2) - (self._b.getWidth() // 2)
        self._b.setPosition((x_pos, y_pos))

        self.updateWindow()

    def setText(self, text):
        """Sets the text of the pop up and centers the new text"""
        self._t = makeMultiLineTextBox(text, (0,0), self._font,
                                       self._fontColor, self._backgroundColor)
        y_pos = (self._height // 4) - (self._t.getHeight() // 2)
        x_pos = (self._width // 2) - (self._t.getWidth() // 2)
        self._t.setPosition((x_pos, y_pos))
        self.updateWindow()

    def confirm(self):
        """Closes the window and sets the confirmed flag to true"""
        self.close()
        self._confirmed = True

    def getConfirmed(self):
        """Returns the boolean confirmation and resets it to None"""
        con = self._confirmed
        self._confirmed = None
        return con

    def handleEvent(self, event):
        """Handles events on the pop up window"""
        self._offset = self._position
        self._b.handleEvent(event,self.confirm,offset=self._offset)
        self.updateWindow()

    def updateWindow(self):
        """Updates the attributes of the pop up window"""
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width-(self._borderWidth*2),
                               self._height-(self._borderWidth*2)))
        surf.fill(self._backgroundColor)       
        self._t.draw(surf)
        self._b.draw(surf)        
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
