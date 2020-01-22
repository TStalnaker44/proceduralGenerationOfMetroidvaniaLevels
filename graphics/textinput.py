"""
Author: Trevor Stalnaker
File: textinput.py

A class that creates and manages textual input boxes
"""

from modules.drawable import Drawable
from graphics.textbox import TextBox
import pygame

class TextInput(Drawable):

    def __init__(self, position, font, dimensions, color=(0,0,0),
                 borderWidth=2, backgroundColor=(255,255,255),
                 borderColor=(0,0,0), borderHighlight=(100,100,200),
                 backgroundHighlight=(225,225,255), maxLen=10,
                 numerical=False, highlightColor=(0,0,0), defaultText="",
                 clearOnActive=False):
        """Initializes the widget with a variety of parameters"""
        super().__init__("", position, worldBound=False)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._defaultBorderWidth = borderWidth
        self._borderColor = borderColor
        self._borderHighlight = borderHighlight
        self._defaultBackgroundColor = backgroundColor
        self._backgroundHighlight = backgroundHighlight
        self._backgroundColor = backgroundColor
        self._textbox = TextBox(defaultText,(0,0),font,color)
        self._maxLen = maxLen
        self._active = False
        self._clearOnActive = clearOnActive
        self._numerical = numerical
        self._currentBorderColor = self._borderColor
        self._borderWidth = borderWidth
        self._color = color
        self._highlightColor = highlightColor
        self.__updateInput()

    def displayActive(self):
        """Sets the display mode to active"""
        self._currentBorderColor = self._borderHighlight
        self._borderWidth = self._defaultBorderWidth + 1
        self._backgroundColor = self._backgroundHighlight
        self._textbox.setFontColor(self._highlightColor)
        if self._clearOnActive:
            self._textbox.setText("")
        self.__updateInput()

    def displayPassive(self):
        """Sets the display mode to passive"""
        self._currentBorderColor = self._borderColor
        self._borderWidth = self._defaultBorderWidth
        self._backgroundColor = self._defaultBackgroundColor
        self._textbox.setFontColor(self._color)
        self.__updateInput()
        
    def handleEvent(self, event, *args, offset=(0,0), func=None,
                    clearOnEnter=False):
        """Handle events on the text input"""
        rect = self.getCollideRect()
        rect = rect.move(offset[0], offset[1])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if rect.collidepoint(event.pos):
                self._active = True
                self.displayActive()
            else:
                self._active = False
                self.displayPassive()
        elif event.type == pygame.KEYDOWN and self._active:
            text = self._textbox.getText()
            if len(text) < self._maxLen:
                # Check for letters
                if 96 < event.key < 123 and not self._numerical:
                    # Check if letter should be capitalized
                    if event.mod in [pygame.KMOD_CAPS, pygame.KMOD_LSHIFT,
                                     pygame.KMOD_RSHIFT]:
                        self._textbox.setText(text + chr(event.key - 32))
                    else:
                        self._textbox.setText(text + chr(event.key))
                # Check for spaces
                elif event.key == 32 and not self._numerical:
                    self._textbox.setText(text + chr(event.key))
                # Check for numbers
                elif 47 < event.key < 58:
                    self._textbox.setText(text + chr(event.key))
                # Check for numpad presses
                elif pygame.K_KP0 <= event.key <= pygame.K_KP9:
                    self._textbox.setText(text + chr(event.key-208))
                    
            # Check if backspace was pressed
            if event.key == 8:
                self._textbox.setText(text[:-1])
            # Check if the enter key was pressed
            if event.key == 13 or event.key == pygame.K_KP_ENTER:
                self._active = False
                self.displayPassive()
                if func != None:
                    func(*args)
                if clearOnEnter:
                    self._textbox.setText("")
            self.__updateInput()

    def getInput(self):
        """Get the current input text"""
        return self._textbox.getText()

    def setText(self, text):
        """Set the text displayed in the input bar"""
        self._textbox.setText(text)

    def __updateInput(self):
        """Update the widget's display"""
        surfBack = pygame.Surface((self._width+(self._borderWidth*2),
                                   (self._height+(self._borderWidth*2))))
        surfBack.fill(self._currentBorderColor)
        surf = pygame.Surface((self._width, self._height))
        surf.fill(self._backgroundColor)
        y_pos = (self._height // 2) - (self._textbox.getHeight() // 2)
        x_pos = (self._width // 2) - (self._textbox.getWidth() // 2)
        self._textbox.setPosition((x_pos, y_pos))
        self._textbox.draw(surf)
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
