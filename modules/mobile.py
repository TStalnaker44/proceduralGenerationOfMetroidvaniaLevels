
from .drawable import Drawable
from .vector2D import Vector2

class Mobile(Drawable):
   """A game object that can move."""
   def __init__(self, imageName, position, size, subImageRect=None):
      super().__init__(imageName, position, size, subImageRect)
      self._velocity = Vector2(0,0)
   
   def update(self):
      
      newPosition = self.getPosition() + self._velocity
      
      self.setPosition(newPosition)
      
      