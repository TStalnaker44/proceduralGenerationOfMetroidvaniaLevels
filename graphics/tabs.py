"""
Author: Trevor Stalnaker
File: tabs.py

Contains classes that model and manage tabs and groups of tabs
"""

from modules.drawable import Drawable
from graphics.textbox import TextBox
import pygame

class Tabs(Drawable):

    def __init__(self, text, position, font, color, backgroundColor,
                 dimensions, activeBackgroundColor, activeFontColor,
                 borderColor=(0,0,0), borderWidth=1, defaultActive=0):
        """Initializes the widget with a variety of parameters"""
        
        super().__init__("", position, worldBound=False)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._font = font
        self._fontColor = color
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._tabs = []
        self._active = defaultActive
        
        tabCount = len(text)
        tabWidth = self._width // tabCount
        tabXPos = 0
        for t in text:
            self._tabs.append(Tab(t, (tabXPos,0), font, color, backgroundColor,
                                  activeFontColor, activeBackgroundColor,
                                  (tabWidth,self._height), (0,0,0), 1))
            tabXPos += tabWidth

        self._tabs[self._active].setActive()
        self.updateTabs()

    def getActive(self):
        """Returns the current active tab"""
        return self._active

    def getTabs(self):
        """Returns all of the tabs in the grouping"""
        return self._tabs

    def handleEvent(self, event, offset=(0,0)):
        """Handle events on all tabs"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.getCollideRect().collidepoint(event.pos):
                for tab in self._tabs:
                    rect = tab.getCollideRect().move(self._position[0], self._position[1])
                    rect = rect.move(offset[0], offset[1])
                    if rect.collidepoint(event.pos):
                        self._active = self._tabs.index(tab)
                        tab.setActive() 
                    else:
                        tab.setNotActive()
                self.updateTabs()
            
    def updateTabs(self):
        """Update all the tabs"""
        surfBack = pygame.Surface((self._width+(self._borderWidth*2),
                                           (self._height+(self._borderWidth*2))))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width, self._height))
        for tab in self._tabs:
            tab.draw(surf)
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
        

class Tab(Drawable):

    def __init__(self, text, position, font, color, backgroundColor,
                 activeFontColor, activeBackgroundColor, dimensions,
                 borderColor=(0,0,0), borderWidth=0):
        """Initializes a tab instance"""
        super().__init__("", position, worldBound=False)
        self._fontColor = color
        self._font = font
        self._backgroundColor = backgroundColor
        self._text = text
        self._height = dimensions[1]
        self._width = dimensions[0]
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._active = False

        self._activeFontColor = activeFontColor
        self._activeBackgroundColor = activeBackgroundColor
        self.updateTab()

    def getText(self):
        """Returns the text of the tab"""
        return self._text

    def isActive(self):
        """Returns true if the tab is active false otherwise"""
        return self._active

    def setActive(self):
        """Sets the tab to active"""
        self._active = True
        self.updateTab()

    def setNotActive(self):
        """Sets the tab to not active"""
        self._active = False
        self.updateTab()

    def updateTab(self):
        """Updates the tab based on changes in attributes"""
        surfBack = pygame.Surface((self._width+(self._borderWidth*2),
                                       (self._height+(self._borderWidth*2))))
        surfBack.fill(self._borderColor)
        surf = pygame.Surface((self._width, self._height))
        t = None
        if self.isActive():
            surf.fill(self._backgroundColor)
            t = TextBox(self._text, (0,0), self._font, self._fontColor)
        else:
            surf.fill(self._activeBackgroundColor)
            t = TextBox(self._text, (0,0), self._font, self._activeFontColor)
        y_pos = (self._height // 2) - (t.getHeight() // 2)
        x_pos = (self._width // 2) - (t.getWidth() // 2)
        t.setPosition((x_pos, y_pos))
        t.draw(surf)
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
            
        
            
            
    
