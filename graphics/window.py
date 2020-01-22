"""
Author: Trevor Stalnaker
File window.py

An abstract class containing methods for basic windows
"""

class Window():

    def __init__(self):
        """Initializes the window"""
        self._display = True

    def close(self):
        """Closes the window"""
        self._display = False

    def display(self):
        """Opens the window"""
        self._display = True

    def getDisplay(self):
        """Returns true if the window is displayed, false otherwise"""
        return self._display
