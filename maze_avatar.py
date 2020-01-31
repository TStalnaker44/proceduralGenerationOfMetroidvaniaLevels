"""
Author: Trevor Stalnaker
File: maze_avatar.py
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
        self._movement = {pygame.K_LEFT:False,
                          pygame.K_RIGHT:False,
                          pygame.K_UP:False,
                          pygame.K_DOWN:False}

        self._keys = []

        self._jumpTime = 0.5
        self._jumpTimer = 0

        self._gravity = 2
        self._friction = 0.3
        self._jumpPower = 125
        
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

    def update(self, worldInfo, ticks, platforms, walls):
        """Updates the position of the star"""
        
        if self._movement[pygame.K_LEFT]:
            self._velocity.x = -self._maxVelocity
            if not self.isFlipped():
                self.flip()
        elif self._movement[pygame.K_RIGHT]:
            self._velocity.x = self._maxVelocity
            if self.isFlipped():
                self.flip()
        else:
            self._velocity.x = 0

        if self._movement[pygame.K_UP]:
            self._velocity.y = -self._maxVelocity
        elif self._movement[pygame.K_DOWN]:
            self._velocity.y = self._maxVelocity
        else:
            self._velocity.y = 0

        #Update the position of the star based on its current velocity and ticks
        newPosition = self._position + (self._velocity * ticks)
        if newPosition[0] < 0 or \
           (newPosition[0] + self.getWidth()) > worldInfo[0]:
           self._velocity[0] = 0
        if (newPosition[1] + self.getHeight()) > worldInfo[1] or \
           (newPosition[1] < 0):
           self._velocity[1] = 0

        self._position += (self._velocity * ticks)
        
        for other in platforms:

            # Check if the type of collidable is a gate
            if type(other) == Gate:

                # Check if the player can pass through a given platform
                if not other.getType() in self._keys and \
                   self.getCollideRect().colliderect(other.getCollideRect()):
                
                    # Check that the player is falling
                    if self._velocity.y > 0:
                        # Check that the player is above the platform
                        if self.getY() + self.getHeight()//2 < other.getY(): 
                            #Put the player on the platform
                            self._position.y = other.getY() - self.getHeight()
                            self._velocity.y = 0 # Reset the player's velocity
                            self._jumpTimer = 0 # Reset the jump timer

                    # Check that the player is jumping
                    elif self._velocity.y < 0:
                        # Check that the player is above the platform
                        if self.getY() + (self.getHeight()//2)  > other.getY(): 
                            #Put the player on the platform
                            self._position.y = other.getY() + other.getHeight()
                            self._velocity.y = 0 # Reset the player's velocity

        for other in walls:

            # Check if the type of collidable is a gate
            if type(other) == Gate:

                # Check if the player can pass through a given platform
                if not other.getType() in self._keys and \
                   self.getCollideRect().colliderect(other.getCollideRect()):
                
                    # Check that the player is moving right
                    if self._velocity.x > 0:
                        # Check that the player is above the platform
                        if self.getX() + self.getWidth()//2 < other.getX(): 
                            #Put the player on the platform
                            self._position.x = other.getX() - self.getWidth()
                            self._velocity.x = 0 # Reset the player's velocity

                    # Check that the player is moving left
                    elif self._velocity.x < 0:
                        # Check that the player is above the platform
                        if self.getX() + (self.getWidth()//2) > other.getX(): 
                            #Put the player on the platform
                            self._position.x = other.getX() + other.getWidth()
                            self._velocity.x = 0 # Reset the player's velocity
            

        
