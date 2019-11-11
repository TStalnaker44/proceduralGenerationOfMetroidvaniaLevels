
import pygame

class Player():

    def __init__(self, pos, stepSize):
        self._width = 15
        self._height = 15
        self._image = pygame.Surface((self._width, self._height))
        self._image.fill((120,120,120))
        self._pos = pos
        self._step = stepSize
        self._keys = []

    def setPos(self, pos):
        self._pos = pos

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            print("oh yeah")
            if event.key == pygame.K_UP:
                self._pos[1] -= self._step
            elif event.key == pygame.K_DOWN:
                self._pos[1] += self._step
            elif event.key == pygame.K_LEFT:
                self._pos[0] -= self._step
            elif event.key == pygame.K_RIGHT:
                self._pos[0] += self._step

    def draw(self, surface):
        surface.blit(self._image, self._pos)
