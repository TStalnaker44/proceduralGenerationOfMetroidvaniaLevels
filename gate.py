"""
Author: Trevor Stalnaker
File: gate.py
"""

from modules.drawable import Drawable
import pygame

class Gate(Drawable):

    def __init__(self, position, color, gateType, direction=0,
                 size=(10,40), passUp=False):
        super().__init__("", position)
        self._direction = direction #The directionality of the gate
        if direction==0:
            self._width = size[0]
            self._height = size[1]
        elif direction==1:
            self._width = size[1]
            self._height = size[0]
        self._image = pygame.Surface((self._width, self._height))
        self._image.fill(color)
        self._type = gateType
        self._passUp = passUp
        

    def getType(self):
        return self._type
