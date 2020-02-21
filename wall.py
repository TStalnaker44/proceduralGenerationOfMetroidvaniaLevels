
import pygame, random
from gate import Gate
from graphics.mysurface import MySurface

class Barrier():

    def draw(self, screen):
        for component in self._components:
            component.draw(screen)

    def getComponents(self):
        return self._components

    def update(self, worldsize, ticks):
        for component in self._components:
            component.update(worldsize, ticks)

    def makePickleSafe(self):
        for component in self._components:
            component.makePickleSafe()

    def undoPickleSafe(self):
        for component in self._components:
            component.undoPickleSafe()
    

class Wall(Barrier):

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
        # Add a double jump gate
        elif connectionType == ("double_jump","double_jump"):
            topHeight = size[1] - ((3 * standardUnit) + size[0])
            bottomHeight = size[0] + (standardUnit*2)
            platformWidth = (2 * standardUnit) + size[0]
            platformPos = ((self._position[0] - (platformWidth//2)) + (size[0]//2),
                           self._position[1]+topHeight+gateHeight)

            # Create the top wall component
            if connectionType != "neutral" or random.random() > .5:
                self._components.append(Gate(self._position,
                                             self._neutral,
                                             99,
                                             size=(size[0],topHeight)
                                             ))

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

        elif connectionType == ("shrink","shrink"):
            # Create the top portion of the wall
            self._components.append(
                    Gate(self._position, #start at position provided to the wall
                         self._neutral, #neutral (grey) coloring
                         99, #key type is 99, ie doesn't exist
                         # The height of the wall is the height of the total wall minus
                         # the height of the gate and the width of the map's walls,
                         # this prevents the gate entrance from being partially embedded
                         # in the ground
                         size=(size[0],size[1]-((gateHeight//2) + size[0])) 
                         )
                    )

            # Add the bottom floor level piece, used to make map corners look nice
            self._components.append(Gate((self._position[0],self._position[1]+(size[1]-size[0])),
                                          self._neutral, 99, size=(size[0],size[0])))
            
        # Add a wall with some sort of a gate
        else:
            
            variant = random.randint(1,2)
                
            # Create a wall with the gate entrance at ground level
            if variant == 1:

                # Create the top portion of the wall
                if connectionType[0] != "neutral" or connectionType[1] != "neutral" or random.random() > .5:
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
                
                # Add the left gate component unless there is a neutral connection
                if connectionType[0] != "neutral":
                    g = Gate(
                        # Start the gate at the y position just under the top section, but
                        # leave space below for the final wall piece
                        (self._position[0],self._position[1]+(size[1]-(gateHeight + size[0]))),
                        color[0], # gate color
                        connectionType[0], # key to unlock the gate
                        direction=0, # direction of the gate (vertical)
                        size=(size[0]//2,gateHeight),
                        passThrough = (False, False, False, True)) # set the size of the gate
                    self._components.append(g)

                # Add the right gate component unless there is a neutral connection
                if connectionType[1] != "neutral":
                    g = Gate(
                        # Start the gate at the y position just under the top section, but
                        # leave space below for the final wall piece
                        (self._position[0]+(size[0]//2),self._position[1]+(size[1]-(gateHeight + size[0]))),
                        color[1], # gate color
                        connectionType[1], # key to unlock the gate
                        direction=0, # direction of the gate (vertical)
                        size=(size[0]//2,gateHeight),
                        passThrough = (False, False, True, False)) # set the size of the gate
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
                if connectionType != "neutral" or random.random() > .5:
                    self._components.append(Gate(self._position,
                                                 self._neutral,
                                                 99,
                                                 size=(size[0],topHeight)
                                                 ))

                # Add the left gate component unless there's a neutral connection
                if connectionType[0] != "neutral":
                    g = Gate(
                        # Start the gate at the y position just under the top section
                        (self._position[0],self._position[1]+topHeight),
                        color[0], # gate color
                        connectionType[0], # key to unlock the gate
                        direction=0, # direction of the gate (vertical)
                        size=(size[0]//2,gateHeight),
                        passThrough = (False, False, False, True)) # set the size of the gate
                    self._components.append(g)

                # Add the right gate component unless there's a neutral connection
                if connectionType[1] != "neutral":
                    g = Gate(
                        # Start the gate at the y position just under the top section
                        (self._position[0]+(size[0]//2),self._position[1]+topHeight),
                        color[1], # gate color
                        connectionType[1], # key to unlock the gate
                        direction=0, # direction of the gate (vertical)
                        size=(size[0]//2,gateHeight),
                        passThrough = (False, False, True, False)) # set the size of the gate
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
                           


class Platform(Barrier):

    def __init__(self, pos, connectionType, color=None,
                 size=(10,120), standardUnit=None, roomHeight=None):
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
                              
            upperplatformLength = standardUnit

            # Create the gating surface
            
            # Create the left subpart
            self._components.append(Gate(
                self._position,
                self._neutral,
                99,
                direction=1,
                size=(size[0],leftEdgeLength)))

            # Create the upper gate component
            if not connectionType[0] in ["neutral"]: 
                # Create the gated opening
                self._components.append(Gate(
                    (self._position[0]+leftEdgeLength,self._position[1]),
                    color[0],
                    connectionType[0],
                    direction=1,
                    size=(size[0]//2,gateWidth),
                    passThrough=(True,False,False,False)))

            # Create the lower gate component
            if not connectionType[1] in ["neutral","double_jump"]: 
                # Create the gated opening
                self._components.append(Gate(
                    (self._position[0]+leftEdgeLength,self._position[1]+(size[0]//2)),
                    color[1],
                    connectionType[1],
                    direction=1,
                    size=(size[0]//2,gateWidth),
                    passThrough=(False,True,False,False))) 

            # Create the right subpart
            self._components.append(Gate(
                (self._position[0]+leftEdgeLength+gateWidth,self._position[1]),
                self._neutral,
                99,
                direction=1,
                size=(size[0],rightEdgeLength)))

            # Create the middle platforms
            if connectionType[1] == "double_jump":
                numOfPlatforms = int(roomHeight//(standardUnit*1.25))
                step = 2
                start = 2
            else:
                numOfPlatforms = int(roomHeight//standardUnit)
                step = 1
                start = 1
            for x in range(start, numOfPlatforms, step):
                length = random.randint(midplatformLength-(size[1]//8),
                                        midplatformLength+(size[1]//8))
                midplatformXPos = self._position[0] + ((size[1] // 2) - (length // 2)) + \
                                  random.randint(-standardUnit,standardUnit)
                self._components.append(Gate(
                    ((midplatformXPos, self._position[1]+(x*standardUnit))),
                    self._neutral,
                    99,
                    direction=1,
                    size=(size[0],length),
                    passThrough=(True,False,False,False)))
