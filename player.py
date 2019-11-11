
import pygame

class Player():

    def __init__(self, pos, stepSize, gridSize):
        self._width = 15
        self._height = 15
        self._image = pygame.Surface((self._width, self._height))
        self._image.fill((120,120,120))
        self._pos = pos
        self._step = stepSize
        self._gridPos = [0,0]
        self._gridSize = gridSize
        self._keys = []

    def setPos(self, pos):
        self._pos = pos

    def getCurrentSquare(self):
        return (self._gridSize[0] * self._gridPos[1]) + self._gridPos[0]

    def handleEvent(self, event, connections):
        connectedNodes = [conn[0]-1 for conn in connections]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and \
               self._gridPos[1]-1 >= 0 and \
               self.getCurrentSquare() - self._gridSize[1] in connectedNodes:
                self._pos[1] -= self._step
                self._gridPos[1] -= 1
            elif event.key == pygame.K_DOWN and \
                 self._gridPos[1]+1 < self._gridSize[1] and \
                 self.getCurrentSquare() + self._gridSize[1] in connectedNodes:
                self._pos[1] += self._step
                self._gridPos[1] += 1
            elif event.key == pygame.K_LEFT and \
                 self._gridPos[0]-1 >= 0 and \
                 self.getCurrentSquare() - 1 in connectedNodes:
                self._pos[0] -= self._step
                self._gridPos[0] -= 1
            elif event.key == pygame.K_RIGHT and \
                 self._gridPos[0]+1 < self._gridSize[0] and \
                 self.getCurrentSquare() + 1 in connectedNodes:
                self._pos[0] += self._step
                self._gridPos[0] += 1

    def draw(self, surface):
        surface.blit(self._image, self._pos)
