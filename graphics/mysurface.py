"""
Author: Trevor Stalnaker
File: mysurface.py

A class that converts pygame surfaces to surfaces inheriting from Drawable
"""

from modules.drawable import Drawable

class MySurface(Drawable):

    def __init__(self, surface, position=(0,0)):
        """Initializes the MySurface object"""
        super().__init__("", position, worldBound=False)
        self._image = surface

    def update(self, surface):
        """Updates the MySurface object with a new surface"""
        self._image = surface
