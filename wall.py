
import pygame, random
from gate import Gate
from graphics.mysurface import MySurface

class Wall():

    def __init__(self, pos, connectionType, color=None,
                 size=(10,120), standardUnit=None):
        # Save the position of the wall component
        self._position = pos
        
        # Save the connection type of the wall component
        self._type = connectionType

        self._components = [] #Store components of the wall

        self._neutral = (120,120,120)

        gateHeight = standardUnit#size[1] // 3

        # Create a barrier (exterior) wall
        if connectionType == 0:
            self._components.append(Gate(self._position, self._neutral,
                                         99, size=size))
        # Add a wall with some sort of a gate
        else:
            
            variant = random.randint(1,2)
                
            # Create a wall with the gate entrance at ground level
            if variant == 1:
                # Create the top portion of the wall
                self._components.append(
                    Gate(self._position, #start at position provided to the wall
                         self._neutral, #neutral (grey) coloring
                         99, #key type is 99, ie doesn't exist
                         # The height of the wall is the height of the total wall minus
                         # the height of the gate and the width of the map's walls,
                         # this prevents the gate entrance from being partially embedded
                         # in the ground
                         size=(size[0],size[1]-(gateHeight + size[0])) 
                         )
                    )
                
                # Add the game component unless there is a neutral connection
                if connectionType != "neutral":
                    g = Gate(
                        # Start the gate at the y position just under the top section, but
                        # leave space below for the final wall piece
                        (self._position[0],self._position[1]+(size[1]-(gateHeight + size[0]))),
                        color, # gate color
                        connectionType, # key to unlock the gate
                        direction=0, # direction of the gate (vertical)
                        size=(size[0],gateHeight)) # set the size of the gate
                    self._components.append(g)
                    
                # Add the bottom floor level piece, used to make map corners look nice
                self._components.append(Gate((self._position[0],self._position[1]+(size[1]-size[0])),
                                                self._neutral, 99, size=(size[0],size[0])))

            # Create a wall with a gate one standard unit above ground level
            elif variant == 2:
                
                topHeight = size[1] - ((2 * standardUnit) + size[0])
                bottomHeight = size[0] + standardUnit
                platformWidth = (2 * standardUnit) + size[0]
                platformPos = ((self._position[0] - (platformWidth//2)) + (size[0]//2),
                               self._position[1]+topHeight+gateHeight)

                # Create the top wall component
                self._components.append(Gate(self._position,
                                             self._neutral,
                                             99,
                                             size=(size[0],topHeight)
                                             ))

                # Add the gate component unless there's a neutral connection
                if connectionType != "neutral":
                    g = Gate(
                        # Start the gate at the y position just under the top section
                        (self._position[0],self._position[1]+topHeight),
                        color, # gate color
                        connectionType, # key to unlock the gate
                        direction=0, # direction of the gate (vertical)
                        size=(size[0],gateHeight)) # set the size of the gate
                    self._components.append(g)

                # Add the bottom floor level piece, used to make map corners look nice
                self._components.append(Gate((self._position[0],self._position[1]+topHeight+gateHeight),
                                             self._neutral,
                                             99,
                                             size=(size[0],bottomHeight)))

                # Add the platform for the player to land on
                self._components.append(Gate(platformPos,
                                             self._neutral,
                                             99,
                                             direction=1, #Set to have a horizontal direction
                                             size=(size[0],platformWidth)))
                           
    def draw(self, screen):
        for component in self._components:
            component.draw(screen)

    def getComponents(self):
        return self._components

    def update(self, worldsize, ticks):
        for component in self._components:
            component.update(worldsize, ticks)


class Platform():

    def __init__(self, pos, connectionType, color=None,
                 size=(10,120), standardUnit=None):
        # Save the position of the wall component
        self._position = pos
        # Save the connection type of the wall component
        self._type = connectionType

        self._components = [] #Store components of the wall

        self._neutral = (120,120,120)

        gateWidth = standardUnit

        # Create a barrier (exterior) platform
        if connectionType == 0:
            g = Gate(self._position,
                     self._neutral, 99, direction=1, size=(size[0],size[1]))
            self._components.append(g)

        else:

            leftEdgeLength = (size[1]-gateWidth) // 2
            rightEdgeLength = (size[1] - leftEdgeLength) - gateWidth
            midplatformLength = 3 * standardUnit
            midplatformXPos = self._position[0] + ((size[1] // 2) - (midplatformLength // 2))
                              
            upperplatformLength = standardUnit

            # Create the gating surface
            
            # Create the left subpart
            self._components.append(Gate(
                self._position,
                self._neutral,
                99,
                direction=1,
                size=(size[0],leftEdgeLength)))

            if connectionType != "neutral": 
                # Create the gated opening
                self._components.append(Gate(
                    (self._position[0]+leftEdgeLength,self._position[1]),
                    color,
                    connectionType,
                    direction=1,
                    size=(size[0],gateWidth)))            

            # Create the right subpart
            self._components.append(Gate(
                (self._position[0]+leftEdgeLength+gateWidth,self._position[1]),
                self._neutral,
                99,
                direction=1,
                size=(size[0],rightEdgeLength)))

            # Create the middle platforms
            for x in range(1, int(size[1]//standardUnit)+1):
                self._components.append(Gate(
                    ((midplatformXPos, self._position[1]+(x*standardUnit))),
                    self._neutral,
                    99,
                    direction=1,
                    size=(size[0],midplatformLength)))
            
            
    def draw(self, screen):
        for component in self._components:
            component.draw(screen)

    def getComponents(self):
        return self._components

    def update(self, worldsize, ticks):
        for component in self._components:
            component.update(worldsize, ticks)

