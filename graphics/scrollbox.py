"""
Author: Trevor Stalnaker
File: scrollbox.py

A class that models and manages a Scroll Box widget
"""

import pygame
from modules.drawable import Drawable
from graphics.mysurface import MySurface
from graphics.banner import Banner

class ScrollBox(Drawable):

    def __init__(self, position, dimensions, internalSurface,
                 borderColor=(0,0,0), borderWidth=0):
        """Initializes the widget with a variety of parameters"""
        super().__init__("", position, worldBound=False)
        self._height = dimensions[0]
        self._width = dimensions[1]
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._internalSurface = internalSurface
        
        self._sidebarWidth = 10
        self._sidebarColor = (120,120,120)
        if self._height > self._internalSurface.getHeight():
            self._sliderHeight = self._height
        else:
            self._sliderHeight = (self._height ** 2) // \
                                 self._internalSurface.getHeight()
        self._sliderColor = (180,180,180)

        # Used to allow the scrollbox to appear around the screen
        self._offset = position

        self._currentOffset = 0

        # Calculate slide step
        self._step = (self._internalSurface.getHeight() - self._height) / \
                     max(1, (self._height-self._sliderHeight))

        self._scrollOffset = 0

        self._slider = Banner((self._width-self._sidebarWidth,0),self._sliderColor,
                         (self._sliderHeight,self._sidebarWidth))

        self._scrolling = False
        
        self.updateScrollBox()

    def getOffset(self):
        """Returns the current internal offset of the scroll box"""
        return self._slider.getY() * self._step * -1

    def getInternalSurface(self):
        """Return the surface within the scroll box"""
        return self._internalSurface

    def setInternalSurface(self, surface):
        """Replaces the internal surface of the scroll box with a given surface"""
        if issubclass(type(surface), MySurface):
            self._internalSurface.update(surface.getImage())
        else:
            self._internalSurface.update(surface)

        #Update Scroll Information
        if self._height > self._internalSurface.getHeight():
            self._sliderHeight = self._height
        else:
            self._sliderHeight = (self._height ** 2) // \
                                 self._internalSurface.getHeight()
            
        self._step = (self._internalSurface.getHeight() - self._height) / \
                     max(1, (self._height-self._sliderHeight))
        tempPos = self._slider.getPosition()
        self._slider = Banner((self._width-self._sidebarWidth,0),self._sliderColor,
                         (self._sliderHeight,self._sidebarWidth))
        self._slider.setPosition(tempPos)

    def dragSlider(self):
        """Determines the positioning of the slider and updates it accordingly"""
        if self._scrolling:
            prevY = self._slider.getY()
            x,y = pygame.mouse.get_pos()
            y -= self._offset[1]

            # Check that the slider bar has not reached the top or bottom of the window
            if (prevY - y > 0 and self._slider.getY() > 0) or \
                    (prevY - y < 0 and \
                    self._slider.getY() + self._sliderHeight < self._height):

                self.moveBar(y)

    def moveBar(self, y):
        """Updates the side slider's position"""
        # Update the slider's position
        self._slider.setPosition((self._slider.getX(), min(self._height - self._slider.getHeight(),
                                                                   max(0,y))))
        self._internalSurface.setPosition((self._internalSurface.getX(),
                                                   round(self._slider.getY() * self._step * -1)))

        # Update the scroll box
        self.updateScrollBox()
        

    def move(self, event):
        """Handles events on the scroll box"""
        # Check if the side bar is being clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                ex,ey = event.pos
                ox,oy = self._offset
                pos = (ex-ox, ey-oy)
                if self._slider.getCollideRect().collidepoint(pos):
                    self._scrolling = True
            # Check if the scroll wheel is being used
            if event.button==4 and self.getCollideRect().collidepoint(event.pos):
                self.moveBar(self._slider.getY()-5)
            if event.button==5 and self.getCollideRect().collidepoint(event.pos):
                self.moveBar(self._slider.getY()+5)
        # Set scrolling to false when the mouse button is released
        if event.type == pygame.MOUSEBUTTONUP and event.button==1:
            self._scrolling = False
        
            # Update the scroll box
            self.updateScrollBox()
        self.dragSlider()
    
    def updateScrollBox(self):
        """Updates the display of the scroll box based on offsets and parameters"""
        surfBack = pygame.Surface((self._width+(self._borderWidth*2),
                                   (self._height+(self._borderWidth*2))))
        surfBack.fill(self._borderColor)
        displaySurf = pygame.Surface((self._width, self._height))
        if issubclass(type(self._internalSurface), Drawable):
            self._internalSurface.draw(displaySurf)
        sideBar = Banner((self._width-self._sidebarWidth,0),self._sidebarColor,
                         (self._height,self._sidebarWidth))
        sideBar.draw(displaySurf)
        self._slider.draw(displaySurf)
        surfBack.blit(displaySurf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
