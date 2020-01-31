
import pygame
from gate import Gate
from graphics.mysurface import MySurface

class Wall():

    def __init__(self, pos, connectionType, color=None,
                 size=(10,120)):
        # Save the position of the wall component
        self._position = pos
        
        # Save the connection type of the wall component
        self._type = connectionType

        self._components = [] #Store components of the wall

        self._neutral = (120,120,120)

        gateHeight = size[1] // 3

        self._components.append(Gate(self._position, self._neutral,
                                     99, size=(size[0],gateHeight)))
        self._components.append(Gate((self._position[0],self._position[1]+(2*gateHeight)),
                                     self._neutral,
                                     99, size=(size[0],gateHeight)))

        if connectionType == 0: #Basic barrier wall or edge
            g = Gate((self._position[0],self._position[1]+gateHeight),
                     self._neutral, 99, direction=0, size=(size[0],gateHeight))
            self._components.append(g)
        else:
            g = Gate((self._position[0],self._position[1]+gateHeight),
                     color, connectionType, direction=0, size=(size[0],gateHeight))
            self._components.append(g)

    def draw(self, screen):
        for component in self._components:
            component.draw(screen)

    def getComponents(self):
        return self._components

    def update(self, worldsize, ticks):
        for component in self._components:
            component.update(worldsize, ticks)


class Platform():

    def __init__(self, pos, connectionType, color=(120,120,120),
                 size=(10,120)):
        # Save the position of the wall component
        self._position = pos
        # Save the connection type of the wall component
        self._type = connectionType

        self._components = [] #Store components of the wall

        self._neutral = (120,120,120)

        gateWidth = size[1] // 3

        self._components.append(Gate(self._position, self._neutral,
                                     99, direction=1, size=(size[0],gateWidth)))
        self._components.append(Gate((self._position[0]+(2*gateWidth),self._position[1]),
                                     self._neutral,
                                     99, direction=1, size=(size[0],gateWidth)))

        if connectionType == 0: #Basic barrier wall or edge
            g = Gate((self._position[0]+gateWidth,self._position[1]),
                     self._neutral, 99, direction=1, size=(size[0],gateWidth))
            self._components.append(g)
        else:
            g = Gate((self._position[0]+gateWidth,self._position[1]),
                     color, connectionType, direction=1, size=(size[0],gateWidth))
            self._components.append(g)

    def draw(self, screen):
        for component in self._components:
            component.draw(screen)

    def getComponents(self):
        return self._components

    def update(self, worldsize, ticks):
        for component in self._components:
            component.update(worldsize, ticks)

