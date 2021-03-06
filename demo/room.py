
import pygame

class Room():

    def __init__(self, pos, key=None):
        self._width = 30
        self._height = 30
        self._image = pygame.Surface((self._width, self._height))
        self._image.fill((120,120,120))
        if key != None:
            self._image.fill(key)
        self._position = pos

    def getCenter(self):
        return (self._position[0] - (self._width//2) + 2,
                self._position[1] - (self._height//2) + 2)

    def color(self, color):
        self._image.fill(color)

    def draw(self, surface):
        surface.blit(self._image, self._position)

class Connector():

    def __init__(self):
        self._image = pygame.Surface((5000,5000))
        self._image.fill((0,0,0))
        self._image.set_colorkey((0,0,0))

    def addLine(self, r1, r2, color=(255,255,255), weight=2, offset=(0,0)):
        endPoint1 = (r1.getCenter()[0] + offset[0],
                     r1.getCenter()[1] + offset[1])
        endPoint2 = (r2.getCenter()[0] + offset[0],
                     r2.getCenter()[1] + offset[1])
        pygame.draw.line(self._image, color, endPoint1,
                         endPoint2, weight)

    def draw(self, surface, offset):
        surface.blit(self._image, offset)
