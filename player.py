
import pygame

class Player():

    def __init__(self, pos, stepSize, gridSize):

        # Create the square image of the player
        self._width = 15
        self._height = 15
        self._image = pygame.Surface((self._width, self._height))
        self._image.fill((120,120,120))

        # Set the player's initial position
        self._pos = pos

        # Set the player's step size (used for graphics)
        self._step = stepSize

        # Set the initial grid position of the player (row x column)
        self._gridPos = [0,0]

        # Save an internal datastructure containing the external grid size
        self._gridSize = gridSize

        # Instantiate a list for the player's collected keys
        self._keys = []

    def setPos(self, pos):
        """Set the player's position"""
        self._pos = pos

    def getCurrentSquare(self):
        """Return the players current position in the grid"""
        return (self._gridSize[1] * self._gridPos[0]) + self._gridPos[1]

    def giveKey(self, key):
        """Give the player a key upon its collection"""
        self._keys.append(key)

    def getKeys(self):
        """Get the player's current key collection"""
        return self._keys

    def handleEvent(self, event, connections):

        # Create a list of nodes connected to the node at the player's
        # current position (list of connections from mainloop)
        connectedNodes = [conn-1 for conn in connections.keys()]

        # If keydown event detected
        if event.type == pygame.KEYDOWN:

            # If the up arrow is pressed, the current row is greater than 0,
            # the above square is in the list of connected nodes, and
            # the key required to cross that gate is in the player's key collection
            if event.key == pygame.K_UP and \
               self._gridPos[0]-1 >= 0 and \
               self.getCurrentSquare() - self._gridSize[1] in connectedNodes and \
               connections[(self.getCurrentSquare() - self._gridSize[1])+1] in self._keys:

                # Change the player's position by the stepsize in the y-direction
                self._pos[1] -= self._step

                # Update the player's current grid position (row-1)
                self._gridPos[0] -= 1

            # If the down arrow is pressed, the current row is less than the number of columns,
            # the below square is in the list of connected nodes, and
            # the key required to cross that gate is in the player's key collection
            elif event.key == pygame.K_DOWN and \
                 self._gridPos[0]+1 < self._gridSize[1] and \
                 self.getCurrentSquare() + self._gridSize[1] in connectedNodes and \
                 connections[(self.getCurrentSquare() + self._gridSize[1])+1] in self._keys:

                # Change the player's position by the stepsize in the y-direction
                self._pos[1] += self._step

                # Update the player's current grid position (row+1)
                self._gridPos[0] += 1

            # If the left arrow is pressed, the current column is greater than 0,
            # the square to the left is in the list of connected nodes, and
            # the key required to cross that gate is in the player's key collection
            elif event.key == pygame.K_LEFT and \
                 self._gridPos[1]-1 >= 0 and \
                 self.getCurrentSquare() - 1 in connectedNodes and \
                 connections[self.getCurrentSquare()] in self._keys:

                # Change the player's position by the stepsize in the x-direction
                self._pos[0] -= self._step

                # Update the player's current grid position (column-1)
                self._gridPos[1] -= 1

            # If the right arrow is pressed, the current row is less than the number of rows,
            # the square to the right is in the list of connected nodes, and
            # the key required to cross that gate is in the player's key collection
            elif event.key == pygame.K_RIGHT and \
                 self._gridPos[1]+1 < self._gridSize[1] and \
                 self.getCurrentSquare() + 1 in connectedNodes and \
                 connections[self.getCurrentSquare() + 2] in self._keys:

                # Change the player's position by the stepsize in the x-direction
                self._pos[0] += self._step

                # Update the player's current gird position (column+1)
                self._gridPos[1] += 1

            # Code for testing   
            elif event.key == pygame.K_a: print(self._gridPos)
            elif event.key == pygame.K_s: print(connections)
            elif event.key == pygame.K_d: print(self.getCurrentSquare())

    def draw(self, surface):
        """Draw the player on the screen"""
        surface.blit(self._image, self._pos)
