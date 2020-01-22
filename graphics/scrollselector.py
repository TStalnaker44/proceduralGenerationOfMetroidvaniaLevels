"""
Author: Trevor Stalnaker
File: scrollselector.py

A class that models a scroll selector, a scroll box with internal buttons
"""

import pygame
from modules.drawable import Drawable
from .scrollbox import ScrollBox
from .button import Button
from .mysurface import MySurface

class ScrollSelector(Drawable):

    def __init__(self, position, dimensions, selectionHeight, selections, backgroundColor,
                 borderColor=(0,0,0), borderWidth=0):
        """Initializes the widget with a variety of parameters"""
        super().__init__("", position, worldBound=False)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._internalHeight = selectionHeight * len(selections)
        self._selectionHeight = selectionHeight
        self._selections = selections
        self._buttons = []
        self._scrollBarWidth = 10
        self._backgroundColor = backgroundColor
        internalSurface = self.makeDisplay()
        self._scrollBox = ScrollBox(position, (self._height, self._width), internalSurface,
                                    borderColor, borderWidth)
        self.update()

    def makeDisplay(self):
        """Creates the buttons for the internal surface"""
        surf = pygame.Surface((self._width, self._internalHeight))
        font = pygame.font.SysFont("Times New Roman", 16)        
        ypos = 0
        for sel in self._selections:
            b = Button(sel["text"], (0,ypos), font,(255,255,255),self._backgroundColor,
                   self._selectionHeight-2, self._width-self._scrollBarWidth-2,
                       borderWidth=0)
            b.draw(surf)
            self._buttons.append(b)
            ypos += self._selectionHeight
        return MySurface(surf)

    def updateSelections(self, selections):
        """Update the buttons with the new selections"""
        self._internalHeight = self._selectionHeight * len(selections)
        self._selections = selections
        self._buttons = []
        internalSurface = self.makeDisplay()
        self._scrollBox.setInternalSurface(internalSurface)
        self.update()

    def updateDisplay(self):
        """Updates the internal surface"""
        surf = pygame.Surface((self._width, self._internalHeight))
        for b in self._buttons:
            b.draw(surf)
        return surf

    def handleEvent(self, event):
        """Handle events on the scroll selector"""
        self._scrollBox.move(event)
        offset = (self._position[0], self._position[1] + self._scrollBox.getOffset())
        if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP)\
           and event.button==1:
            if self._scrollBox.getCollideRect().collidepoint(event.pos):
                for i,b in enumerate(self._buttons):
                    if self._selections[i]["args"] != "":
                        b.handleEvent(event, self._selections[i]["func"],
                              self._selections[i]["args"], offset=offset)
                    else:
                        b.handleEvent(event, self._selections[i]["func"], offset=offset)        
        self._scrollBox.setInternalSurface(self.updateDisplay())
        self.update()

    def update(self):
        """Update the scroll selector"""
        self._scrollBox.updateScrollBox()
        self._image = self._scrollBox.getImage()
        

    
