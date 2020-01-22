"""
Author: Trevor Stalnaker
File: mask.py

Models and manages a rectangle of varying transparency 
"""

import pygame
from modules.drawable import Drawable

class Mask(Drawable):

    def __init__(self, position, dimensions, color, alpha, worldBound=False):
        """Initializes a mask object"""
        super().__init__("", position, worldBound=worldBound)
        self._image = pygame.Surface(dimensions)
        self._image.fill(color)
        self._image.set_alpha(0)
        self._alpha = alpha

    def setAlpha(self, alpha):
        """Sets the alpha value for the mask"""
        self._alpha = alpha
        self._image.set_alpha(alpha)

    def getAlpha(self):
        """Returns the current alpha value for the mask"""
        return self._alpha

    def setColor(self, color):
        """Sets the color of the mask"""
        self._image.fill(color)
