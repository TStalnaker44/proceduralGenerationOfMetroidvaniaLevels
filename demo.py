"""
Author: Trevor Stalnaker
File: test_demo.py
"""

import pygame, pickle, glob
from mapdata import MapData
from key import Key
from gate import Gate
from avatar import Avatar
from wall import Wall, Platform
from key import Key
import networkx as nx
import matplotlib.pyplot as plt
import grapher, latticeCreator

n = 6
m = 4

# Dynamically determine screen size based on grid size
SCREEN_SIZE = (1200,800)
WORLD_SIZE = (500,500)

class LevelTester():

   def __init__(self, screen_size):
      self._font = pygame.font.SysFont("Times New Roman", 32)
      self._colors = {"grey":(80,80,80),"red":(255,0,0), "green":(0,255,0), "blue":(0,0,255),
             "orange":(255,165,0),"white":(255,255,255),"brown":(160,82,45),
             "purple":(128,0,128), "pink":(255,192,203),"yellow":(255,255,0)}
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
      self._startNode = None

   def makeMap(self, m, n, ordering, endNode, startNode=1):
      """Create a map with dimensions m x n, obeying the given gate ordering"""
      self._m = m
      self._n = n
      self._endNode = endNode
      self._startNode = startNode
      self._ordering = ordering
      # Create a graph model
      dimensions = (m,n)
      self._gates = grapher.getGateOrder(ordering)
      self._keys = {gate:startNode for gate in self._gates} #This provides default start for keys  
      self._g = latticeCreator.generateViableMap(dimensions, self._gates, self._keys,
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

      self._SCREEN_SIZE = (self._n*100,self._m*100)

      self.prepareMap()
      self._won = False

   def saveMap(self, fileName):
      """Save a map to file"""
      md = MapData(self._g, self._keys, self._gates, self._m, self._n, self._endNode,
                   self._ordering, self._startNode)
      with open(fileName, "wb") as pFile:
         pickle.dump(md, pFile, protocol=pickle.HIGHEST_PROTOCOL)

   def newMap(self):
      """Create a new map using the current dimensions and gate ordering"""
      self.makeMap(self._m, self._n, self._ordering, self._endNode)
      self.prepareMap()
      self._won = False

   def prepareMap(self):
      """Prepare the graphical / displayed components of the level"""

      self._connections = []
      self._physicalKeys = []
      roomDim = 120
      roomSize = (roomDim, roomDim)
      barrierWidth = 10
      barrierSize = (barrierWidth,roomDim+barrierWidth)
      startCoord = (100,100)

      # Save the coordinates for the rooms to be used by the generator
      topCorners = []
      for y in range(self._m):
         for x in range(self._n):
            topCorners.append((x,y))

      # Get all of the distinct rooms in the map
      rooms = []
      for edge in self._g.edges():
         rooms.append(edge[0])
         rooms.append(edge[1])
      rooms = set(rooms)

      # Add connections between rooms
      for edge in self._g.edges(data=True):
         gateType = self._colors[edge[2]["object"]]
         r = edge[0]
         if edge[1] == r+1:
            r_pos = topCorners[r-1]
            x_pos = ((r_pos[0]+1) * roomSize[0]) + startCoord[0]
            y_pos = (r_pos[1] * roomSize[1]) + startCoord[1]
            #self._connections.append(Gate((x_pos, y_pos),gateType, None, 0, (10,100)))
            self._connections.append(Wall((x_pos, y_pos), gateType, gateType, size=barrierSize))
         elif edge[1] == r+n:
            r_pos = topCorners[r-1]
            x_pos = (r_pos[0] * roomSize[0]) + startCoord[0]
            y_pos = ((r_pos[1]+1) * roomSize[1]) + startCoord[1]
            self._connections.append(Platform((x_pos, y_pos), gateType, gateType, size=barrierSize))
            #self._connections.append(Gate((x_pos, y_pos),gateType, None, 1, (10,100)))

      #Iterate through the rooms to add the edge walls
      for r in rooms:
         
         #Add barriers to the tops of rooms
         if r <= n:
            x_pos = (topCorners[r-1][0]*roomSize[0]) + startCoord[0]
            y_pos = (topCorners[r-1][1]*roomSize[1]) + startCoord[1]
            self._connections.append(Platform((x_pos, y_pos), 0, size=barrierSize))
            #self._connections.append(Gate((x_pos, y_pos),(120,120,120), None, 1, (10,100)))
         elif not (r-n, r) in self._g.edges:
            r_pos = topCorners[(r-n)-1]
            x_pos = (r_pos[0] * roomSize[0]) + startCoord[0]
            y_pos = ((r_pos[1]+1) * roomSize[1]) + startCoord[1]
            self._connections.append(Platform((x_pos, y_pos), 0, size=barrierSize))
            #self._connections.append(Gate((x_pos, y_pos),(120,120,120), None, 1, (10,100)))
            
         #Add barriers to the bottoms of rooms
         if r > ((m-1)*n):
            x_pos = (topCorners[r-1][0]*roomSize[0]) + startCoord[0]
            y_pos = ((topCorners[r-1][1]+1)*roomSize[1]) + startCoord[1]
            self._connections.append(Platform((x_pos, y_pos), 0, size=barrierSize))
            #self._connections.append(Gate((x_pos, y_pos),(120,120,120), None, 1, (10,100)))
         elif not (r, r+n) in self._g.edges:
            r_pos = topCorners[r-1]
            x_pos = (r_pos[0] * roomSize[0]) + startCoord[0]
            y_pos = ((r_pos[1]+1) * roomSize[1]) + startCoord[1]
            self._connections.append(Platform((x_pos, y_pos), 0, size=barrierSize))
            #self._connections.append(Gate((x_pos, y_pos),(120,120,120), None, 1, (10,100)))
            
         #Add barriers to the lefts of rooms
         if r % n == 1:
            x_pos = (topCorners[r-1][0]*roomSize[0]) + startCoord[0]
            y_pos = ((topCorners[r-1][1])*roomSize[1]) + startCoord[1]
            self._connections.append(Wall((x_pos, y_pos), 0, size=barrierSize))
            #self._connections.append(Gate((x_pos, y_pos),(120,120,120), None, 0, (10,100)))
         elif not (r-1, r) in self._g.edges():
            r_pos = topCorners[r-2]
            x_pos = ((r_pos[0]+1) * roomSize[0]) + startCoord[0]
            y_pos = (r_pos[1] * roomSize[1]) + startCoord[1]
            self._connections.append(Wall((x_pos, y_pos), 0, size=barrierSize))
            #self._connections.append(Gate((x_pos, y_pos),(120,120,120), None, 0, (10,100)))
            
         #Add barriers to the rights of rooms
         if r % n == 0:
            x_pos = ((topCorners[r-1][0]+1)*roomSize[0]) + startCoord[0]
            y_pos = ((topCorners[r-1][1])*roomSize[1]) + startCoord[1]
            self._connections.append(Wall((x_pos, y_pos), 0, size=barrierSize))
            #self._connections.append(Gate((x_pos, y_pos),(120,120,120), None, 0, (10,100)))
         elif not (r, r+1) in self._g.edges():
            r_pos = topCorners[r-1]
            x_pos = ((r_pos[0]+1) * roomSize[0]) + startCoord[0]
            y_pos = (r_pos[1] * roomSize[1]) + startCoord[1]
            self._connections.append(Wall((x_pos, y_pos), 0, size=barrierSize))
            #self._connections.append(Gate((x_pos, y_pos),(120,120,120), None, 0, (10,100)))
         
      # Color rooms with keys
      for key in self._keys.keys():
         print(self._keys[key])
         rCoord = topCorners[self._keys[key]]
         midCoord = (((rCoord[0]*roomSize[0]) - roomSize[0]//2)+startCoord[0],
                     ((rCoord[1]*roomSize[1]) + roomSize[1]//2)+startCoord[1])
         self._physicalKeys.append(Key(midCoord, self._colors[key], self._colors[key]))
##         for i, room in enumerate(self._rooms):
##            if self._keys[key] == i+1:
##               room.color(self._colors[key])
##               break


         

      # Create a copy of the list to allow mutations without error
##      roomCopy = copy.copy(self._rooms)
##      for x in range(len(roomCopy)):
##          # Remove rooms that are not part of the graph
##          if not x+1 in self._g:
##              self._rooms.remove(roomCopy[x])

      # Create a player object
##      startPos = self._rooms[0].getCenter()
##      self._player = Player([startPos[0]+20,startPos[1]+20], 100, (self._m,self._n))

   def draw(self, screen):
      """Draw the level to the screen"""
      for gate in self._connections:
         gate.draw(screen)

      for key in self._physicalKeys:
         key.draw(screen)
##      # Draw the rooms to the screen
##      for room in self._rooms:
##          room.draw(screen)
##
##      # Draw the connections between the rooms
##      self._lines.draw(screen, (25,25))
##
##      # Draw the player to the screen
##      self._player.draw(screen)
##      
##      # Draw the players collected keys to the screen
##      r = 10 # Radius of orbs
##      for i, orb in enumerate(self._player.getKeys()):
##         pygame.draw.circle(screen, self._colors[orb], ((i+1) * int(2.5 * r) ,self._SCREEN_SIZE[1]-25), r)
##
##      # If the game has been won, display winning message to the screen
##      if self._won:
##         screen.blit(self._font.render("You Have Won", False, (0,0,0)),
##                     (35*self._n,44*self._m))

   def handleEvent(self, event):
      """Handle events for the level"""
##      if not self._won:
##         # Determine which squares are reachable from current grid
##         # position and over which gating types
##         connections = {}
##         for edge in self._g.edges(data=True):
##            if edge[0] == self._player.getCurrentSquare()+1:
##               connections[edge[1]] = edge[2]["object"]
##            elif edge[1] == self._player.getCurrentSquare()+1:
##               connections[edge[0]] = edge[2]["object"]
##         self._player.handleEvent(event, connections)

      if event.type == pygame.KEYDOWN:   
         if event.key == pygame.K_p:
            self.plot()
         elif event.key == pygame.K_s:
            sfile = input("Name the file to be saved: ")
            self.saveMap("maps\\" + sfile + ".mapdat")
         elif event.key == pygame.K_l:
            print("Files:", [x[5:][:-7] for x in glob.glob("maps/*")])
            lfile = input("File to load: ")
            self.loadMap("maps\\" + lfile + ".mapdat")
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

   font = pygame.font.SysFont("Times New Roman", 32)

   #Update the title for the window
   pygame.display.set_caption('Level Tester')
   
   #Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   gameClock = pygame.time.Clock()

   avatar = Avatar((100,100))

   level = LevelTester(SCREEN_SIZE)
   ordering = {"red":"green","green":"blue","blue":"white",}
   #ordering = {"grey":["red","orange"],"red":"green","green":"blue",
   #            "orange":["yellow","white"],"yellow":"purple"}
   
   endNode   = n*m
   startNode = 1
   assert 0 < endNode <= n*m
   assert 0 < startNode <= n*m
   assert startNode != endNode
   level.makeMap(m,n,ordering,endNode,startNode)
   level.prepareMap()


   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

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

         avatar.move(event)
         level.handleEvent(event)

      #Calculate ticks
      ticks = gameClock.get_time() / 1000
      
      #avatar.update(WORLD_SIZE, ticks, platforms, walls)

      # Allow the avatar to collect keys
##      for key in keys:
##        if key.getCollideRect().colliderect(avatar.getCollideRect()):
##            avatar.giveKey(key.getType())
##            key.collect()
##            print(avatar._keys)

      # Remove keys that have been collected
      #keys = [key for key in keys if not key.collected()]

   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()




