"""
Author: Trevor Stalnaker
File: banner.py

A class that creates and manages a banner
"""

from modules.drawable import Drawable
import pygame

class Banner(Drawable):

    def __init__(self, position, color, dimensions, borderColor=(0,0,0), borderWidth=0):
        """Initializes the widget with a variety of parameters"""
        super().__init__("", position, worldBound=False)
        self._color = color
        self._height = dimensions[0]
        self._width = dimensions[1]
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self.__updateBanner()

    def __updateBanner(self):
        """Update the widget's display"""
        surfBack = pygame.Surface((self._width + (self._borderWidth*2),
                                   self._height + (self._borderWidth*2)))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width, self._height))
        surf.fill(self._color)
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
