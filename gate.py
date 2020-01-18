"""
Author: Trevor Stalnaker
File: gate.py
"""

from modules.drawable import Drawable
import pygame

class Gate(Drawable):

    def __init__(self, position, color, gateType):
        super().__init__("", position)
        self._width = 10
        self._height = 40
        self._image = pygame.Surface((self._width, self._height))
        self._image.fill(color)
        self._type = gateType

    def getType(self):
        return self._type
