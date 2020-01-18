"""
Author: Trevor Stalnaker
File: avatar.py
"""

from modules.drawable import Drawable
from modules.vector2D import Vector2
from gate import Gate
import pygame

class Avatar(Drawable):

    def __init__(self, position):
        super().__init__("", position)
        self._width = 30
        self._height = 30
        self._image = pygame.Surface((self._width,self._height))
        self._image.fill((255,255,255,255))
        pygame.draw.circle(self._image, (0,0,0), (15,15), 15)
        self._image.set_colorkey(self._image.get_at((0,0)))

        self._velocity = Vector2(0,0)
        self._maxVelocity = 100
        self._acceleration = 0.5
        self._movement = {pygame.K_w:False,
                          pygame.K_s:False,
                          pygame.K_a:False,
                          pygame.K_d:False}

        self._keys = []

    def getKeys(self):
        return self._keys

    def hasKey(self, key):
        return key in self._keys

    def giveKey(self,key):
        self._keys.append(key)

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            self._movement[event.key] = True
        elif event.type == pygame.KEYUP:
            self._movement[event.key] = False

    def update(self, worldInfo, ticks, collidables):
        """Updates the position of the star"""

        #Update the velocity of the star based on the keyboard inputs
        if self._movement[pygame.K_w]:
            self._velocity.y = -self._maxVelocity
        elif self._movement[pygame.K_s]:
            self._velocity.y = self._maxVelocity
        else:
            self._velocity.y = 0
            
        if self._movement[pygame.K_a]:
            self._velocity.x = -self._maxVelocity
            if not self.isFlipped():
                self.flip()
        elif self._movement[pygame.K_d]:
            self._velocity.x = self._maxVelocity
            if self.isFlipped():
                self.flip()
        else:
            self._velocity.x = 0

        #If the current velocity exceeds the maximum, scale it down
        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)

        #Update the position of the star based on its current velocity and ticks
        newPosition = self._position + (self._velocity * ticks)
        if newPosition[0] < 0 or \
           (newPosition[0] + self.getWidth()) > worldInfo[0]:
           self._velocity[0] = 0
        if (newPosition[1] + self.getHeight()) > worldInfo[1] or \
           (newPosition[1] < 0):
           self._velocity[1] = 0
        self._position += (self._velocity * ticks)
        
        for other in collidables:

            # Check if the type of collidable is a gate
            if type(other) == Gate:
                
                if not other.getType() in self._keys and \
                   self.getCollideRect().colliderect(other.getCollideRect()):

                    # Scale the velocity of the avatar and break it into components
                    v = self._velocity
                    v.scale(1)
                    vx, vy = v

                    # Determine how the avatar is intersecting with the barrier
                    if vx > 0:
                        x_embed = -1 * (self.getWidth() - (other.getX() - self.getX()))
                    elif vx < 0:
                        x_embed = (self.getX()-other.getX()) - (other.getWidth())
                    else:
                        x_embed = 0
                    if vy > 0:
                        y_embed = -1 * (self.getHeight() - (other.getY() - self.getY()))
                    elif vy < 0:
                        y_embed = (self.getY()-other.getY()) - other.getHeight()
                    else:
                        y_embed = 0

                    # Prevent the player from being able to slide up the sides of obstacles
                    if abs(vx) > 0 and (self.getY()>other.getY() or \
                                        self.getY()+self.getHeight() < \
                                        other.getY()+self.getHeight()):
                        y_embed = 0

                    # Calculate the amount and direction of pushback
                    pushback = Vector2(vx*x_embed, vy*y_embed)

                    # Apply the pushback to the avatar's position
                    self._position += pushback
        
