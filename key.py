"""
Author: Trevor Stalnaker
File: key.py
"""

from modules.drawable import Drawable
import pygame

class Key(Drawable):

    def __init__(self, position, color, keyType):
        super().__init__("", position)
        self._width = 15
        self._height = 15
        self._image = pygame.Surface((self._width, self._height))
        self._image.fill(color)
        self._color = color

        self._collected = False
        self._type = keyType

    def collect(self):
        self._collected = True

    def collected(self):
        return self._collected

    def getType(self):
        return self._type

    def getColor(self):
        return self._color


