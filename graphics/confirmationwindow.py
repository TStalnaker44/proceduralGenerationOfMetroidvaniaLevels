"""
Author: Trevor Stalnaker
File: confirmationwindow.py

A class that models and manages a confirmation window
"""

import pygame
from modules.drawable import Drawable
from graphics.window import Window
from graphics.textbox import TextBox
from graphics.button import Button
from graphics.guiUtils import makeMultiLineTextBox

class ConfirmationWindow(Drawable, Window):

    def __init__(self, text, position, dimensions, font, fontColor,
                 backgroundColor, buttonColor, buttonDimensions, buttonFont,
                 buttonFontColor, confirmationText="YES", denialText="NO",
                 buttonBorderWidth=1,buttonBorderColor=(0,0,0), borderWidth=0,
                 borderColor=(0,0,0)):
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

        # Create the textbox
        self._t = makeMultiLineTextBox(self._text, (0,0), self._font,
                                       self._fontColor, self._backgroundColor)
        y_pos = (self._height // 4) - (self._t.getHeight() // 2)
        x_pos = (self._width // 2) - (self._t.getWidth() // 2)
        self._t.setPosition((x_pos, y_pos))
        
        # Create the buttons
        self._b1 = Button(confirmationText, (0,0), buttonFont, buttonFontColor,
                         buttonColor,buttonDimensions[1],
                         buttonDimensions[0],buttonBorderColor, buttonBorderWidth)
        y_pos = (3*(self._height // 4)) - (self._b1.getHeight() // 2)
        x_pos = (self._width // 3) - (self._b1.getWidth() // 2)
        self._b1.setPosition((x_pos, y_pos))

        self._b2 = Button(denialText, (0,0), buttonFont, buttonFontColor,
                         buttonColor,buttonDimensions[1],
                         buttonDimensions[0],buttonBorderColor, buttonBorderWidth)
        y_pos = (3*(self._height // 4)) - (self._b2.getHeight() // 2)
        x_pos = (2*(self._width // 3)) - (self._b2.getWidth() // 2)
        self._b2.setPosition((x_pos, y_pos))

        self._sel = None

        self.updateWindow()

    def setText(self, text):
        """Sets the text of the window"""
        self._t = makeMultiLineTextBox(text, (0,0), self._font,
                                       self._fontColor, self._backgroundColor)
        y_pos = (self._height // 4) - (self._t.getHeight() // 2)
        x_pos = (self._width // 2) - (self._t.getWidth() // 2)
        self._t.setPosition((x_pos, y_pos))
        self.updateWindow()

    def handleEvent(self, event):
        """Handles events on the window"""
        self._offset = self._position
        self._b1.handleEvent(event,self.confirm,offset=self._offset)
        self._b2.handleEvent(event,self.reject,offset=self._offset)
        self.updateWindow()
        return self.getSelection()

    def confirm(self):
        """Sets selection to confirm and closes the window"""
        self.close()
        self._sel = 1

    def reject(self):
        """Sets selection to reject and closes the window"""
        self.close()
        self._sel = 0

    def getSelection(self):
        """Returns the current selection and resets the selection to None"""
        sel = self._sel
        self._sel = None
        return sel

    def updateWindow(self):
        """Update the window after parameters have been changed"""
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width-(self._borderWidth*2),
                               self._height-(self._borderWidth*2)))
        surf.fill(self._backgroundColor)       
        self._t.draw(surf)
        self._b1.draw(surf)
        self._b2.draw(surf)
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
