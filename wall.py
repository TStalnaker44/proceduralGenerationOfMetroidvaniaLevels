
import pygame
from gate import Gate
from graphics.mysurface import MySurface

class Wall():

    def __init__(self, pos, direction, connectionType):
        # Save the position of the wall component
        self._position = pos
        # Save the directionality of the wall component (vertical or horizontal)
        self._direction = direction
        # Save the connection type of the wall component
        self._type = connectionType

        self._components = [] #Store components of the wall

        if connectionType == 0: #Basic barrier wall or edge
            g = Gate(self._position, (120,120,120),99,self._direction)
            self._components.append(g)
        elif connectionType == 1: #Absence of wall
            pass
        else:
            pass

    def draw(self, screen):
        for component in self._components:
            component.draw(screen)

    def getComponents(self):
        return self._components
