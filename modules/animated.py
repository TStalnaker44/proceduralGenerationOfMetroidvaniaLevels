import pygame, os
from pygame import image
from .frameManager import FRAMES
from .drawable import Drawable

class Animated(Drawable):
   
   def __init__(self, imageName, location):
      super().__init__(imageName, location, (0,0))
      
      self._frame = 0
      self._row = 0
      self._animationTimer = 0
      self._framesPerSecond = 5
      self._nFrames = 2
      
      self._animate = True
      

      
   def updateAnimation(self, ticks):
      if self._animate:
         self._animationTimer += ticks
         
         if self._animationTimer > 1 / self._framesPerSecond:
            self._frame += 1
            self._frame %= self._nFrames
            self._animationTimer -= 1 / self._framesPerSecond
            self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))
            if self.isFlipped():
               self._image = pygame.transform.flip(self._image, True, False)
            if self.isScaled():
               self.scale(self._scaleValue)
   
   def startAnimation(self):
      self._animate = True
   
   
   def stopAnimation(self):
      self._animate = False
