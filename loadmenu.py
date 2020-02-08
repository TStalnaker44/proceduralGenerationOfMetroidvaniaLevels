"""
Author: Trevor Stalnaker
File: loadmenu.py
"""

import pygame, glob
from graphics import *
from modules.drawable import Drawable

class LoadMenu(Drawable, Window):

    def __init__(self, pos, dimensions):
        """Initializes the pause menu"""

        Drawable.__init__(self, "", pos, worldBound=False)
        Window.__init__(self)

        self._offset = (pos[0], pos[1])

        self._width  = dimensions[0]
        self._height = dimensions[1]

        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._smallFont = pygame.font.SysFont("Times New Roman", 14)
        self._borderColor = (0,0,0)
        self._borderWidth = 2
        self._backgroundColor = (80,80,80)

        buttonWidth  = 3 * (self._width // 4)
        buttonHeight = (self._height-30) // 5

        buttonXpos = self._width//2 - buttonWidth // 2
        buttonYpos = (self._height - buttonHeight) - 15

        self._tabs = Tabs(["Maps","Templates"], (0,0),
                          self._font, (0,0,0), (120,120,120),
                          (self._width, 35), (0,0,0),
                          (255,255,255))
        
        self._loadButton = Button("Load", (buttonXpos,buttonYpos),
                                    self._font, (0,0,0), (0,255,0),
                                    buttonHeight, buttonWidth//2, (0,0,0), 2)
        self._cancelButton = Button("Cancel", (buttonXpos+buttonWidth//2, buttonYpos),
                                    self._font, (0,0,0), (120,120,150),
                                    buttonHeight, buttonWidth//2, (0,0,0), 2)

        self._options = [{"text":x[5:][:-8],"func":self.updateSelection,"args":x[5:][:-8]} for x in glob.glob("maps/*")]
        self._levelSelect = ScrollSelector((pos[0]+3+buttonXpos,pos[1]+45),(buttonWidth,buttonHeight*2.75),
                                           30,self._options,(0,0,0))

        self._textbox = TextInput((buttonXpos,buttonYpos - (25 + 10)),
                                  self._smallFont, (buttonWidth, 25))
        self._selection = None

        self.updateMenu()

    def display(self):
        Window.display(self)
        self.updateOptions()
        self.updateMenu()

    def handleEvent(self, event):
        """Handles events on the pause menu"""
        self._loadButton.handleEvent(event, self.load, offset=self._offset)
        self._cancelButton.handleEvent(event, self.cancel, offset=self._offset)
        self._levelSelect.handleEvent(event)
        
        active = self._tabs.getActive()
        self._tabs.handleEvent(event, offset=self._offset)
        if active != self._tabs.getActive(): self.updateOptions()
        
        self.updateMenu()
        return self.getSelection()

    def updateOptions(self):
        if self._tabs.getActive() == 1:
            self._options = [{"text":x[10:][:-7],"func":self.updateSelection,"args":x[10:][:-7]}
                             for x in glob.glob("templates/*")]
        else:
            self._options = [{"text":x[5:][:-8],"func":self.updateSelection,"args":x[5:][:-8]}
                             for x in glob.glob("maps/*")]
        self._levelSelect.updateSelections(self._options)
        self._textbox.setText("")

    def updateSelection(self, text):
        self._textbox.setText(text)
        self.updateMenu()

    def load(self):
        """Sets the selection to resume""" 
        self._selection = self._textbox.getInput()
        self._textbox.setText("")
        self.close()

    def cancel(self):
        """Sets the selecton to controls"""
        self._textbox.setText("")
        self.close()

    def getSelection(self):
        """Returns the current selection and resets it to None"""
        sel = self._selection
        self._selection = None
        return sel

    def draw(self, screen):
        Drawable.draw(self, screen)
        self._levelSelect.draw(screen)

    def updateMenu(self):
        """Updates the display of the pause menu"""

        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        # Draw widgets
        self._loadButton.draw(surf)
        self._cancelButton.draw(surf)
        self._textbox.draw(surf)
        self._tabs.draw(surf)
        
        
        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
