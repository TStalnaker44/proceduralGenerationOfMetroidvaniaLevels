"""
@authors: Trevor Stalnaker, Justin Pusztay

This file creates a linked progress bar, where an entity is
attached to the animal and it updates the progress bar based on
the entity that is attached, hence the bar being linked.
"""


import pygame
from .progressbar import ProgressBar

class LinkedProgressBar():

    def __init__(self, entity, position, length, maxStat, actStat, borderWidth=1,
                 borderColor=(0,0,0), backgroundColor=(120,120,120),
                 barColor=(255,0,0)):
        """Initializes a progress bar and links it with an entity"""

        self._progressBar = ProgressBar(position, length, maxStat, actStat,
                                        borderWidth, borderColor, backgroundColor,
                                        barColor,height = 12)
        self._entity = entity

    def update(self):
        """Update the progress bar based on the entity's stats"""
        self._progressBar.setProgress(self._entity.getHealth())

    def draw(self,screen):
        """Draws the progress bar"""
        self._progressBar.draw(screen)

    def getEntity(self):
        """Returns the entity linked to the progress bar"""
        return self._entity
        
