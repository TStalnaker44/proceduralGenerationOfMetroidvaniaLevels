"""
Author: Trevor Stalnaker
File: levelDemo
Description:
    Provides a visual, interactive way to experiment with generated
    metroidvannia style mappings
"""

import pygame, copy, random, pickle, glob
import graph_generation.latticeCreator as latticeCreator
import graph_generation.grapher as grapher
from demo.room import Room
from demo.room import Connector
from mapdata import MapData
from demo.player import Player
import networkx as nx
import matplotlib.pyplot as plt
from graphics import *

m = 3#random.randint(5,8) # number of rows
n = 4#random.randint(5,8) # number of columns

# Dynamically determine screen size based on grid size
SCREEN_SIZE = (n*100,m*100)

class LevelTester():

   def __init__(self, screen_size):
      self._font = pygame.font.SysFont("Times New Roman", 32)
      self._colors = {"grey":(80,80,80),"red":(255,0,0), "green":(0,255,0), "blue":(0,0,255),
             "orange":(255,165,0),"white":(255,255,255),"brown":(160,82,45),
             "purple":(128,0,128), "pink":(255,192,203),"yellow":(255,255,0),
             "double_jump":(255,97,50),"shrink":(120,120,45),
             "neutral":(10,10,10)}
      self._SCREEN_SIZE = screen_size
      self._won      =  False
      self._player   =  None
      self._g        =  None
      self._keys     =  None
      self._gates    =  None
      self._m        =  None
      self._n        =  None
      self._endNode  =  None
      self._ordering =  None

   def makeMap(self, m, n, ordering, h_mapping, v_mapping, endNode, startNode=1):
      """Create a map with dimensions m x n, obeying the given gate ordering"""
      self._m = m
      self._n = n
      self._endNode = endNode
      self._startNode = startNode
      self._ordering = ordering
      self._weightedNeutral = .5
      # Create a graph model
      dimensions = (m,n)
      self._gates = grapher.getGateOrder(ordering)
      self._h_mapping = grapher.getDirectionalMapping(h_mapping)
      self._v_mapping = grapher.getDirectionalMapping(v_mapping)
      self._mappings = (self._h_mapping, self._v_mapping)
      self._keys = {gate:startNode for gate in self._gates} #This provides default start for keys  
      self._g = latticeCreator.generateViableMap(dimensions, self._gates, self._keys, self._mappings,
                                                 .5, endNode, startNode)

   def loadMap(self, fileName):
      """Load a map saved to file"""
      with open(fileName, "rb") as pFile:
         md = pickle.load(pFile)
      self._g        =  md._g
      self._keys     =  md._keys
      self._gates    =  md._gates
      self._m        =  md._m
      self._n        =  md._n
      self._endNode  =  md._endNode
      self._ordering =  md._ordering
      try:
         self._startNode = md._startNode
      except:
         self._startNode = 1

      self._SCREEN_SIZE = (self._n*100,self._m*100)

      self.prepareMap()
      self._won = False

   def saveMap(self, fileName):
      """Save a map to file"""
      md = MapData(self._g, self._keys, self._gates, self._m, self._n, self._endNode,
                   self._ordering, self._startNode, self._weightedNeutral,
                   self._h_mapping, self._v_mapping)
      with open(fileName, "wb") as pFile:
         pickle.dump(md, pFile, protocol=pickle.HIGHEST_PROTOCOL)

   def newMap(self):
      """Create a new map using the current dimensions and gate ordering"""
      self.makeMap(self._m, self._n, self._ordering, self._endNode, self._startNode)
      self.prepareMap()
      self._won = False

   def prepareMap(self):
      """Prepare the graphical / displayed components of the level"""
      # Create rooms based on the model
      self._rooms, c = [], 0
      for y in range(self._m):
          for x in range(self._n):
            key =  None
            self._rooms.append(Room(((100*x) + 25,(100*y) + 25), (c,0,0)))
            c+=1

      # Color rooms with keys
      for key in self._keys.keys():
         for i, room in enumerate(self._rooms):
            if self._keys[key] == i+1:
               room.color(self._colors[key])
               break

      # Add connections between rooms
      self._lines = Connector()
      for edge in self._g.edges(data=True):
         lineColor = self._colors[edge[2]["object"]]
         if edge[0] > edge[1]:
            self._lines.addLine(self._rooms[edge[0]-1], self._rooms[edge[1]-1],
                                lineColor, 3, offset=(-5,-5))
         else:
            self._lines.addLine(self._rooms[edge[0]-1], self._rooms[edge[1]-1],
                                lineColor, 3, offset=(5,5))

      # Create a copy of the list to allow mutations without error
      roomCopy = copy.copy(self._rooms)
      for x in range(len(roomCopy)):
          # Remove rooms that are not part of the graph
          if not x+1 in self._g:
              self._rooms.remove(roomCopy[x])

      # Create a player object
      startPos = self._rooms[self._startNode-1].getCenter()
      self._player = Player([startPos[0]+20,startPos[1]+20], 100, (self._m,self._n),
                            self._startNode)

   def draw(self, screen):
      """Draw the level to the screen"""
      # Draw the rooms to the screen
      for room in self._rooms:
          room.draw(screen)

      # Draw the connections between the rooms
      self._lines.draw(screen, (25,25))

      # Draw the player to the screen
      self._player.draw(screen)
      
      # Draw the players collected keys to the screen
      r = 10 # Radius of orbs
      for i, orb in enumerate(self._player.getKeys()):
         pygame.draw.circle(screen, self._colors[orb], ((i+1) * int(2.5 * r) ,self._SCREEN_SIZE[1]-25), r)

      # If the game has been won, display winning message to the screen
      if self._won:
         screen.blit(self._font.render("You Have Won", False, (0,0,0)),
                     (35*self._n,44*self._m))

   def handleEvent(self, event):
      """Handle events for the level"""
      if not self._won:
         # Determine which squares are reachable from current grid
         # position and over which gating types
         connections = {}
         for edge in self._g.edges(data=True):
            if edge[0] == self._player.getCurrentSquare()+1:
               connections[edge[1]] = edge[2]["object"]
         self._player.handleEvent(event, connections)

      if event.type == pygame.KEYDOWN:   
         if event.key == pygame.K_p:
            self.plot()
         elif event.key == pygame.K_s:
            sfile = input("Name the file to be saved: ")
            self.saveMap("saves\\templates\\" + sfile + ".mapdat")
         elif event.key == pygame.K_l:
            print("Files:", [x[5:][:-7] for x in glob.glob("saves/templates/*")])
            lfile = input("File to load: ")
            self.loadMap("saves\\templates\\" + lfile + ".mapdat")
         elif event.key == pygame.K_n:
            self.newMap()

   def update(self):
      """Update the level state and display"""
      if not self._won:
         # Give the player the key in the current room
         # if they don't already have it
         currentSquare = self._player.getCurrentSquare()+1
         if currentSquare in self._keys.values():
            for key in self._keys.keys():
               if key not in self._player.getKeys() and \
                  self._keys[key] == currentSquare:
                  self._player.giveKey(key)
                  break

         # If the player reaches the winning square,
         # set game to won
         if currentSquare == self._endNode:
            self._won = True

   def plot(self):
      """Generate a network x plot for the level"""
      # Create a color mapping to visualize key locations
      color_map = []
      for node in self._g:
          for gate in self._gates:
              if self._keys[gate] == node and gate in self._colors.keys():
                  if gate in ["double_jump","shrink","neutral"]:
                     color_map.append("grey")
                  else:
                     color_map.append(gate)
                  break
          else:
              color_map.append("grey")

      #Display the graph
      pos = nx.spring_layout(self._g)
      #nx.draw_planar(self._g, with_labels=True, font_weight='bold')
      nx.draw(self._g, pos, node_color=color_map, with_labels=True, font_weight='bold')
      edge_labels = nx.get_edge_attributes(self._g,'object')
      nx.draw_networkx_edge_labels(self._g, pos, edge_labels = edge_labels)
      plt.show()


def main():
   """
   Main loop for the program
   """
   
   #Initialize the module
   pygame.init()
   pygame.font.init()

   #Update the title for the window
   pygame.display.set_caption('Level Tester')
   
   #Create the Level Tester object
   level = LevelTester(SCREEN_SIZE)
##   ordering = {"red":"green","green":["blue","orange"],"blue":"white","orange":"grey"}
##   #ordering = {"grey":["red","orange"],"red":"green","green":"blue",
##   #            "orange":["yellow","white"],"yellow":"purple"}
##
##   # The starter gate type and all potential end types need to be included in these lists,
##   # otherwise a crash could occur
##   h_mapping = ["red",("blue", "green"),"blue","white","grey"]
##   v_mapping = ["red",("green","blue"),"orange","white","grey"]

##   ordering = {"pink":["red","orange"],"red":"green",
##               "orange":"grey","green":"blue","blue":"white",}
##   h_mapping = ["pink",("red","blue"),"green","blue","white","grey"]
##   v_mapping = ["pink","red",("green","pink"),"blue","white","grey",
##                ("orange","blue")]

##   ordering = {"neutral":["red","blue"],"red":["green","orange"],"blue":"white"}
##
##   h_mapping = ["neutral","red","blue","green",("orange","blue"),"white"]
##   v_mapping = ["neutral","red","green",("orange","blue"),"white"]

   ordering = {"neutral":"red","red":"green"}

   h_mapping = ["neutral","red","green"]
   v_mapping = ["neutral","red","green"]
   
   endNode   = n*m
   startNode = 1
   assert 0 < endNode <= n*m
   assert 0 < startNode <= n*m
   assert startNode != endNode
   level.makeMap(m,n,ordering,h_mapping,v_mapping,endNode,startNode)
   level.prepareMap()
           
   RUNNING = True

   while RUNNING:

      #Get the screen, allowing for dynamic sizing
      screen = pygame.display.set_mode(level._SCREEN_SIZE)

      #Draw the background to the screen
      screen.fill((140,50,20))

      level.draw(screen)
      
      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            
            # change the value to False, to exit the main loop
            RUNNING = False

         level.handleEvent(event)

      level.update()

   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()


