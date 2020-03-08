"""
Author: Trevor Stalnaker
File: maze_avatar.py
"""

from modules.drawable import Drawable
from modules.vector2D import Vector2
from .gate import Gate
from .fsm import *
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
        self._maxVelocity = 150
        self._movement = {pygame.K_LEFT:False,
                          pygame.K_RIGHT:False,
                          pygame.K_UP:False,
                          pygame.K_DOWN:False}

        self._keys = []

        states = ["standing","jumping","falling","walking"]
        transitions = [Rule("standing","jump","jumping"),
                       Rule("jumping","fall","falling"),
                       Rule("falling","stop","standing"),
                       Rule("standing","walk","walking"),
                       Rule("walking","stop","standing"),
                       Rule("walking","jump","jumping"),
                       Rule("walking","fall","falling"),
                       Rule("standing","fall","falling")]
        self._fsm = FSM("standing", states, transitions)

        self._onGround = False

        self._jumpTime = 0.5
        self._jumpTimer = 0

        self._jumpCount = 0

        self._gravity = 2
        self._friction = 0.3
        self._jumpPower = 125

        self._shrunk = False
        
    def getKeys(self):
        return self._keys

    def hasKey(self, key):
        return key in self._keys

    def giveKey(self,key):
        self._keys.append(key)

    def move(self, event):
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if (self._fsm.getCurrentState() == "standing" or \
               self._fsm.getCurrentState() == "walking"):
                self._fsm.changeState("jump")
                self._onGround = False
                self._jumpCount += 1
                
            elif (self._fsm.getCurrentState() == "jumping") and \
                 self._jumpCount < 2 and \
                 "double_jump" in self._keys:
                self._jumpTimer = self._jumpTime
                self._jumpCount += 1

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if "shrink" in self._keys:
                if self._shrunk:
                    self._position.y -= self.getHeight()
                    self.scale(2)
                else:
                    self.scale(0.5)
                self._shrunk = not self._shrunk
                
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

        if (self._fsm.getCurrentState() == "standing" or \
           self._fsm.getCurrentState() == "walking") and \
           not self._onGround:
            self._fsm.changeState("fall")

        if self._fsm.getCurrentState() == "jumping":
            if self._jumpTimer > 0:
                self._velocity.y = -self._maxVelocity
                self._jumpTimer -= ticks
            else:
                self._fsm.changeState("fall")
                self._jumpTimer = self._jumpTime
                self._jumpCount = 0
                
        if self._fsm.getCurrentState() == "falling":
            if not self._onGround:
                self._velocity.y = self._maxVelocity
            else:
                self._fsm.changeState("stop")

        #Update the position of the star based on its current velocity and ticks
        newPosition = self._position + (self._velocity * ticks)
        if newPosition[0] < 0 or \
           (newPosition[0] + self.getWidth()) > worldInfo[0]:
           self._velocity[0] = 0
        if (newPosition[1] + self.getHeight()) > worldInfo[1] or \
           (newPosition[1] < 0):
           self._velocity[1] = 0

        self._position += (self._velocity * ticks)

        # Reset on ground to false (the default)
        self._onGround = False
        
        for other in platforms + walls:

            # Check if the type of collidable is a gate
            # and if it is a platform (direction is 1)
            if type(other) == Gate and other._direction==1:

                # Check if the player can pass through a given platform
                if not other.getType() in self._keys and \
                   self.getCollideRect().colliderect(other.getCollideRect()):
                
                    # Check that the player is falling
                    if self._velocity.y > 0 and not other._passThrough[1]:
                        # Check that the player is above the platform
                        if self.getY() + self.getHeight()//2 < other.getY(): 
                            #Put the player on the platform
                            self._position.y = other.getY() - self.getHeight()
                            self._onGround = True

                    # Check that the player is jumping
                    elif self._velocity.y < 0 and not other._passThrough[0]:
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
                    if self._velocity.x > 0 and not other._passThrough[2]:
                        # Check that the player is above the platform
                        if self.getX() + self.getWidth()//2 < other.getX(): 
                            #Put the player on the platform
                            self._position.x = other.getX() - self.getWidth()
                            self._velocity.x = 0 # Reset the player's velocity

                    # Check that the player is moving left
                    elif self._velocity.x < 0 and not other._passThrough[3]:
                        # Check that the player is above the platform
                        if self.getX() + (self.getWidth()//2) > other.getX(): 
                            #Put the player on the platform
                            self._position.x = other.getX() + other.getWidth()
                            self._velocity.x = 0 # Reset the player's velocity
            

        
