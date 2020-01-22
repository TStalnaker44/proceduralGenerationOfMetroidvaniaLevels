"""
Author: Trevor Stalnaker
File: particletext.py

A class that models and manages text that moves and changes in opacity
"""

import pygame
from graphics import *

class ParticleText():

    def __init__(self, text, startPos, endPos, time, font, fontColor):
        """Initializes the widget with a variety of parameters"""
        self._text = text
        self._startPos = startPos
        self._endPos = endPos
        self._effectTime = time
        self._effectTimer = self._effectTime
        self._font = font
        self._fontColor = fontColor
        self._alpha = 0

        xVel = (endPos[0] - startPos[0]) // time
        yVel = (endPos[1] - startPos[1]) // time
        self._velocity = (xVel, yVel)

        self._alphaScale = (255 // time) * 2

        self._textBoxes = self.formatText()

        self._done = False
        

    def formatText(self):
        """Formats the text based on parameters passed in the init"""
        tboxes = []
        lines = self._text.split("\n")
        width = TextBox(max(lines, key=len),self._startPos,
                        self._font, self._fontColor).getWidth() + 10
        height = self._font.get_height()
        p = self._startPos
        for line in lines:
            t = TextBox(line, p, self._font, self._fontColor)
            center = width // 2 - t.getWidth() // 2
            t.setPosition((center + self._startPos[0], t.getY()+self._startPos[1]))
            tboxes.append(t)
            p = (self._startPos[0], p[1] + height)
        return tboxes

    def draw(self, surface):
        """Draws the particle text object if its animation is not finished"""
        if not self.finished():
            for t in self._textBoxes:
                t._image.set_alpha(self._alpha)
                t.draw(surface)

    def finished(self):
        """Sets done to True"""
        return self._done

    def update(self, ticks):
        """Update the attributes and position of the text based on ticks"""
        
        # Update the position of the textbox
        if self._effectTimer > 0:
            for t in self._textBoxes:
                t.setPosition((t.getX() + (self._velocity[0]*ticks),
                              t.getY() + (self._velocity[1]*ticks)))
            self._effectTimer -= ticks
        else:
            self._done = True
            
        # Update the alpha values of the textbox
        if self._effectTimer > self._effectTime // 2:
            self._alpha += (self._alphaScale * ticks)
        else:
            self._alpha -= (self._alphaScale * ticks)
        
