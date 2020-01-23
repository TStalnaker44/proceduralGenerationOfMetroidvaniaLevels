import pygame, latticeCreator, grapher, copy, random
from room import Room
from room import Connector
from player import Player
import networkx as nx
import matplotlib.pyplot as plt
from graphics import *

m = 4#random.randint(5,8) # number of rows
n = 4#random.randint(5,8) # number of columns

# Dynamically determine screen size based on grid size
SCREEN_SIZE = (n*100,m*100)

class LevelTester():

   def __init__(self, screen_size):
      self._font = pygame.font.SysFont("Times New Roman", 32)
      self._colors = {"grey":(80,80,80),"red":(255,0,0), "green":(0,255,0), "blue":(0,0,255),
             "orange":(255,165,0),"white":(255,255,255),"brown":(160,82,45),
             "purple":(128,0,128), "pink":(255,192,203)}
      self._SCREEN_SIZE = screen_size
      self._won     =  False
      self._player  =  None
      self._g       =  None
      self._keys    =  None
      self._gates   =  None
      self._m       =  None
      self._n       =  None
      self._endNode =  None

   def makeMap(self, m, n, ordering):
      self._m = m
      self._n = n
      self._endNode = n*m
      # Create a graph model
      dimensions = (m,n)
      self._gates = grapher.getGateOrder(ordering)
      self._keys = {gate:1 for gate in self._gates}   
      self._g = latticeCreator.generateViableMap(dimensions, self._gates, self._keys, .5)

   def prepareMap(self):
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
         self._lines.addLine(self._rooms[edge[0]-1], self._rooms[edge[1]-1], lineColor, 3)

      # Create a copy of the list to allow mutations without error
      roomCopy = copy.copy(self._rooms)
      for x in range(len(roomCopy)):
          # Remove rooms that are not part of the graph
          if not x+1 in self._g:
              self._rooms.remove(roomCopy[x])

      # Create a player object
      startPos = self._rooms[0].getCenter()
      self._player = Player([startPos[0]+20,startPos[1]+20], 100, (self._m,self._n))

   def draw(self, screen):
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
      if not self._won:
         # Determine which squares are reachable from current grid
         # position and over which gating types
         connections = {}
         for edge in self._g.edges(data=True):
            if edge[0] == self._player.getCurrentSquare()+1:
               connections[edge[1]] = edge[2]["object"]
            elif edge[1] == self._player.getCurrentSquare()+1:
               connections[edge[0]] = edge[2]["object"]
         self._player.handleEvent(event, connections)

      if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
         self.plot()

   def update(self):
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
      # Create a color mapping to visualize key locations
      color_map = []
      for node in self._g:
          for gate in self._gates:
              if self._keys[gate] == node:
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
   
   #Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   #Create the Level Tester object
   level = LevelTester(SCREEN_SIZE)
   #ordering = {"grey":["red","white"],"red":"green","green":"blue","blue":"purple"}
   ordering = {"red":"green","green":"blue"}
   level.makeMap(m,n,ordering)
   level.prepareMap()
           
   RUNNING = True

   while RUNNING:

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


