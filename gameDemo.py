"""
Author: Trevor Stalnaker
File: gameDemo.py
"""

import pygame, pickle, glob, random
from mapdata import MapData, GeneratedMap
from platformer.key import Key
from platformer.gate import Gate
from platformer.avatar import Avatar
from platformer.wall import Wall, Platform
from platformer.key import Key
import networkx as nx
import matplotlib.pyplot as plt
import graph_generation.grapher as grapher
import graph_generation.latticeCreator as latticeCreator
from graphics import MySurface
from platformer.menu import Menu

n = 6#random.randint(4,10)#6
m = 6#random.randint(4,10)#4

# Dynamically determine screen size based on grid size
SCREEN_SIZE = (1000,625)
WORLD_SIZE = (10000,10000)

class LevelTester():

   def __init__(self, screen_size, world_size, roomDims):
      self._font = pygame.font.SysFont("Times New Roman", 32)
      self._colors = {"grey":(80,80,80),"red":(255,0,0), "green":(0,255,0), "blue":(0,0,255),
             "orange":(255,165,0),"white":(255,255,255),"brown":(160,82,45),
             "purple":(128,0,128), "pink":(255,192,203),"yellow":(255,255,0),
             "double_jump":(255,97,50),"shrink":(120,120,45)}
      self._SCREEN_SIZE = screen_size
      self._WORLD_SIZE = world_size
      self._won             = False
      self._player          = None
      self._g               = None
      self._keys            = None
      self._gates           = None
      self._m               = None
      self._n               = None
      self._endNode         = None
      self._ordering        = None
      self._startNode       = None
      self._weightedNeutral = None
      self._showMiniMap     = False

      ## Variables used in the creation of the minimap

      # Create a standard unit for creation of map
      self._u = Avatar((0,0)).getHeight()*1.5

      # Dimensions of the rooms in the world
      self._roomHeight = roomDims[1] * self._u #standard units
      self._roomWidth = roomDims[0] * self._u #standard units

      # Dimensions of the rooms on the minimap
      self._miniRoomWidth = 50
      self._miniRoomHeight = 30

      temp = pygame.Surface((10,10))
      temp.fill((0,0,0))
      self._pointer = MySurface(temp, (0,0))

   def makeMap(self, m, n, ordering, h_mapping, v_mapping,
               endNode, startNode=1, weightedNeutral=0.5):
      """Create a map with dimensions m x n, obeying the given gate ordering"""
      self._m = m
      self._n = n
      self._endNode = endNode
      self._startNode = startNode
      self._ordering = ordering
      self._h_mapping = grapher.getDirectionalMapping(h_mapping)
      self._v_mapping = grapher.getDirectionalMapping(v_mapping)
      self._mappings = (self._h_mapping, self._v_mapping)
      self._gates = grapher.getGateOrder(ordering)
      self._keys = {gate:startNode for gate in self._gates} #This provides default start for keys
      self._weightedNeutral = weightedNeutral
      # Create a graph model
      dimensions = (m,n)
      self._g = latticeCreator.generateViableMap(dimensions, self._gates, self._keys,
                                                 self._mappings, weightedNeutral, endNode,
                                                 startNode)

   def loadTemplate(self, fileName):
      """Create a new map from a saved template"""
      with open(fileName, "rb") as pFile:
         md = pickle.load(pFile)
         self._g               =  md._g
         self._keys            =  md._keys
         self._gates           =  md._gates
         self._m               =  md._m
         self._n               =  md._n
         self._endNode         =  md._endNode
         self._ordering        =  md._ordering

         try:
            self._weightedNeutral = md._weightedNeutral
         except:
            self._weightedNeutral = 0.5

         try:
            self._startNode = md._startNode
         except:
            self._startNode = 1

         try:
            self._h_mapping = md._h_mapping
            self._v_mapping = md._v_mapping
         except:
            self._h_mapping = grapher.getDirectionalMapping(md._ordering)
            self._v_mapping = grapher.getDirectionalMapping(md._ordering)

      # Prepare a map with the above settings
      self.prepareMap()

      # Set the game state to unwon
      self._won = False

   def loadMap(self, fileName):
      """Load in a previously saved map"""
      with open(fileName, "rb") as pFile:
         md = pickle.load(pFile)
         self._g               =  md._templateData._g
         self._keys            =  md._templateData._keys
         self._gates           =  md._templateData._gates
         self._m               =  md._templateData._m
         self._n               =  md._templateData._n
         self._endNode         =  md._templateData._endNode
         self._ordering        =  md._templateData._ordering
         self._weightedNeutral =  md._templateData._weightedNeutral
         self._startNode       =  md._templateData._startNode
         try:
            self._h_mapping    =  md._templateData._h_mapping
            self._v_mapping    =  md._templateData._v_mapping
         except:
            self._h_mapping = grapher.getDirectionalMapping(md._templateData._gates)
            self._v_mapping = grapher.getDirectionalMapping(md._templateData._gates)
         self._finish          =  md._finish
         self._walls           =  md._walls
         self._platforms       =  md._platforms
         self._physicalKeys    =  md._physicalKeys
         self._player          =  Avatar(md._playerStart)
         self._backupKeys      = [k for k in self._physicalKeys]
         try:
            self._roomHeight   = md._roomDims[1]
            self._roomWidth    = md._roomDims[0]
         except:
            self._roomHeight = None
            self._roomWidth  = None
         for k in self._physicalKeys: k._collected = False

      # Convert the drawable objects back to a drawable form
      self._finish.undoPickleSafe()
      for wall in self._walls: wall.undoPickleSafe()
      for plat in self._platforms: plat.undoPickleSafe()
      for key in self._physicalKeys: key.undoPickleSafe()

      # If the saved map predates the saving of room dimension info,
      # extract that information from the physical platforms
      # (Used for making the minimap function properly)
      if self._roomHeight == None:
         for wall in self._walls:
            if wall._type == 0:
               self._roomHeight = wall.getComponents()[0].getHeight()
               break
         print(self._roomHeight)
         for platform in self._platforms:
            if platform._type == 0:
               self._roomWidth  = platform.getComponents()[0].getWidth()
               break
         print(self._roomWidth)
      
      # Separate the platforms and walls into their components (for collision detection)
      self._platformParts = []
      for p in self._platforms:
         self._platformParts.extend(p.getComponents())
      self._wallParts = []
      for w in self._walls:
         self._wallParts.extend(w.getComponents())

      # Set the game state to unwon
      self._won = False

      # Create a crude minimap of the world
      self._miniMap = self.createMiniMap()

   def restart(self):
      """Restart the current map"""
      self._player =  Avatar(self._playerStart)
      self._physicalKeys = [k for k in self._backupKeys]
      for k in self._physicalKeys:
         k._collected = False
      self._won = False

   def saveTemplate(self, fileName):
      """Save a map template to file"""
      md = MapData(self._g, self._keys, self._gates, self._m, self._n, self._endNode,
                   self._ordering, self._startNode, self._weightedNeutral,
                   self._h_mapping, self._v_mapping)
      with open(fileName, "wb") as pFile:
         pickle.dump(md, pFile, protocol=pickle.HIGHEST_PROTOCOL)

   def saveMap(self, fileName):
      """Save a map to file"""
      md = MapData(self._g, self._keys, self._gates, self._m, self._n, self._endNode,
                   self._ordering, self._startNode, self._weightedNeutral,
                   self._h_mapping, self._v_mapping)
      for wall in self._walls: wall.makePickleSafe()
      for platform in self._platforms: platform.makePickleSafe()
      for key in self._backupKeys: key.makePickleSafe()
      self._finish.makePickleSafe()
      gm = GeneratedMap(md, self._finish, self._walls, self._platforms,
                        self._backupKeys, self._playerStart,
                        (self._roomWidth,self._roomHeight))
      with open(fileName, "wb") as pFile:
         pickle.dump(gm, pFile, protocol=pickle.HIGHEST_PROTOCOL)

      self._finish.undoPickleSafe()
      for wall in self._walls: wall.undoPickleSafe()
      for plat in self._platforms: plat.undoPickleSafe()
      for key in self._backupKeys: key.undoPickleSafe()

   def newMap(self):
      """Create a new map using the current dimensions and gate ordering"""
      self.makeMap(self._m, self._n, self._ordering, self._h_mapping, self._v_mapping,
                   self._endNode, self._startNode, self._weightedNeutral)
      self.prepareMap()
      self._won = False

   def createMiniMap(self):
      """Create a minimap for the player"""

      startCoords = (20, self._SCREEN_SIZE[1]-(self._miniRoomHeight*(self._m+1)))

      # Get the top corners for each position in the grid
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

      miniRooms = []
      for r in rooms:
         tempSurf = pygame.Surface((self._miniRoomWidth, self._miniRoomHeight))
         if r == self._endNode:
            tempSurf.fill((135,206,250))
         elif r == self._startNode:
            tempSurf.fill((0,255,0))
         else:
            tempSurf.fill((255,255,255))
         x,y = topCorners[r-1]
         pos = ((x * (self._miniRoomWidth+2)) + startCoords[0],
                (y * (self._miniRoomHeight+2)) + startCoords[1])
         miniRooms.append(MySurface(tempSurf, pos))

      return miniRooms

   def updateMiniMap(self):
      """Update the player's position on the minimap"""
      play_x = ((self._player.getX() + (self._player.getWidth()//2) - 100) * \
                (self._miniRoomWidth / (self._roomWidth))) + 20
      play_y = ((self._player.getY() + self._player.getHeight() - 100) * \
                (self._miniRoomHeight / (self._roomHeight))) + \
               self._SCREEN_SIZE[1]-(self._miniRoomHeight*(self._m+1))
      for room in self._miniMap:
         if room.getCollideRect().collidepoint((play_x, play_y)):
            posx = room.getX() + (room.getWidth()//2) - (self._pointer.getWidth()//2)
            posy = room.getY() + (room.getHeight()//2) - (self._pointer.getHeight()//2)
            self._pointer.setPosition((posx,posy))
      

   def prepareMap(self):
      """Prepare the graphical / displayed components of the level"""

      # Create a standard unit for creation of map
      u = self._u

      # Initialize visual attributes
      self._walls = []
      self._platforms = []
      self._physicalKeys = []
      roomHeight = self._roomHeight
      roomWidth = self._roomWidth
      roomSize = (roomWidth, roomHeight)
      barrierWidth = (1/4) * u
      wallSize = (barrierWidth, roomHeight + barrierWidth)
      platformSize = (barrierWidth, roomWidth + barrierWidth) 
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


      # Split the edges of the graph into two types
      # forward edges and backwards edges and create a
      # mapping between the two
      forwardEdges = [edge for edge in self._g.edges(data=True) if edge[0] < edge[1]]
      bEdges = [edge for edge in self._g.edges(data=True) if edge[0] > edge[1]]

      # Order the backwards edges to match with those
      # of the forward variety
      backwardEdges = []
      for x in forwardEdges:
         for y in bEdges:
            if y[0] == x[1] and y[1] == x[0]:
               backwardEdges.append(y)
               break
            
      # Enable backwards compatibility with older maps that
      # weren't bidirectional
      if type(self._g) != nx.DiGraph:
         forwardEdges = [edge for edge in self._g.edges(data=True)]
         backwardEdges = [(edge[1],edge[0],edge[2]) for edge in forwardEdges]

      # Add connections between rooms
      for i, edge in enumerate(forwardEdges):

         # Determine the types of gates present in the gateway
         gateTypeForward = edge[2]["object"]
         gateTypeBackward = backwardEdges[i][2]["object"]
         gateTypes = (gateTypeForward, gateTypeBackward)

         # Determine the colors of the gates present in the gateway
         gateColorForward = self._colors.get(edge[2]["object"], None)
         gateColorBackward = self._colors.get(backwardEdges[i][2]["object"],None)
         gateColors = (gateColorForward, gateColorBackward)
         
         r = edge[0]
         if edge[1] == r+1:
            r_pos = topCorners[r-1]
            x_pos = ((r_pos[0]+1) * roomSize[0]) + startCoord[0]
            y_pos = (r_pos[1] * roomSize[1]) + startCoord[1]
            self._walls.append(Wall((x_pos, y_pos), gateTypes, gateColors, size=wallSize, standardUnit=u))
         elif edge[1] == r+self._n:
            r_pos = topCorners[r-1]
            x_pos = (r_pos[0] * roomSize[0]) + startCoord[0]
            y_pos = ((r_pos[1]+1) * roomSize[1]) + startCoord[1]
            self._platforms.append(Platform((x_pos, y_pos), gateTypes, gateColors,
                                            size=platformSize, standardUnit=u,
                                            roomHeight=wallSize[1]))

      #Iterate through the rooms to add the edge walls
      for r in rooms:
         
         #Add barriers to the tops of rooms
         if r <= self._n:
            x_pos = (topCorners[r-1][0]*roomSize[0]) + startCoord[0]
            y_pos = (topCorners[r-1][1]*roomSize[1]) + startCoord[1]
            self._platforms.append(Platform((x_pos, y_pos), 0, size=platformSize, standardUnit=u,
                                            roomHeight=wallSize[1]))
         elif not (r-self._n, r) in self._g.edges:
            r_pos = topCorners[(r-self._n)-1]
            x_pos = (r_pos[0] * roomSize[0]) + startCoord[0]
            y_pos = ((r_pos[1]+1) * roomSize[1]) + startCoord[1]
            self._platforms.append(Platform((x_pos, y_pos), 0, size=platformSize,
                                            standardUnit=u,
                                            roomHeight=wallSize[1]))
            
         #Add barriers to the bottoms of rooms
         if r > ((self._m-1)*self._n):
            x_pos = (topCorners[r-1][0]*roomSize[0]) + startCoord[0]
            y_pos = ((topCorners[r-1][1]+1)*roomSize[1]) + startCoord[1]
            self._platforms.append(Platform((x_pos, y_pos), 0, size=platformSize,
                                            standardUnit=u, roomHeight=wallSize[1]))
         elif not (r, r+self._n) in self._g.edges:
            r_pos = topCorners[r-1]
            x_pos = (r_pos[0] * roomSize[0]) + startCoord[0]
            y_pos = ((r_pos[1]+1) * roomSize[1]) + startCoord[1]
            self._platforms.append(Platform((x_pos, y_pos), 0, size=platformSize,
                                            standardUnit=u, roomHeight=wallSize[1]))
            
         #Add barriers to the lefts of rooms
         if r % self._n == 1:
            x_pos = (topCorners[r-1][0]*roomSize[0]) + startCoord[0]
            y_pos = ((topCorners[r-1][1])*roomSize[1]) + startCoord[1]
            self._walls.append(Wall((x_pos, y_pos), 0, size=wallSize, standardUnit=u))
         elif not (r-1, r) in self._g.edges():
            r_pos = topCorners[r-2]
            x_pos = ((r_pos[0]+1) * roomSize[0]) + startCoord[0]
            y_pos = (r_pos[1] * roomSize[1]) + startCoord[1]
            self._walls.append(Wall((x_pos, y_pos), 0, size=wallSize, standardUnit=u))
            
         #Add barriers to the rights of rooms
         if r % self._n == 0:
            x_pos = ((topCorners[r-1][0]+1)*roomSize[0]) + startCoord[0]
            y_pos = ((topCorners[r-1][1])*roomSize[1]) + startCoord[1]
            self._walls.append(Wall((x_pos, y_pos), 0, size=wallSize, standardUnit=u))
         elif not (r, r+1) in self._g.edges():
            r_pos = topCorners[r-1]
            x_pos = ((r_pos[0]+1) * roomSize[0]) + startCoord[0]
            y_pos = (r_pos[1] * roomSize[1]) + startCoord[1]
            self._walls.append(Wall((x_pos, y_pos), 0, size=wallSize, standardUnit=u))
         
      # Add Keys to the Rooms
      for key in self._keys.keys():
         keyType = key
         keyColor = self._colors.get(keyType, None)
         rCoord = topCorners[self._keys[key]-1]
         midCoord = (((rCoord[0]*roomSize[0]) + roomSize[0]//2)+startCoord[0],
                     ((rCoord[1]*roomSize[1]) + (roomSize[1] - (u*1.75)))+startCoord[1])
         if key != "neutral":
            self._physicalKeys.append(Key(midCoord, keyColor, keyType))

      # Create a player object
      self._playerStart = (topCorners[self._startNode-1][0]*roomSize[0] + u + startCoord[0],
                  ((topCorners[self._startNode-1][1]*roomSize[1])+(roomSize[1]//2))+startCoord[1])
      self._player = Avatar(self._playerStart)

      # Separate the platforms and walls into their components (for collision detection)
      self._platformParts = []
      for p in self._platforms:
         self._platformParts.extend(p.getComponents())
      self._wallParts = []
      for w in self._walls:
         self._wallParts.extend(w.getComponents())

      # Create the finishing block
      s = pygame.Surface((roomSize[0]//2, roomSize[1]//2))
      s.fill((212, 175, 55))
      topCorner = topCorners[self._endNode-1]
      pos = (((topCorner[0]*roomSize[0])+(roomSize[0]//4)) + startCoord[0] + barrierWidth//2,
             ((topCorner[1]*roomSize[1])+(roomSize[1]//4)) + startCoord[1] + barrierWidth//2)
      self._finish = MySurface(s, pos)
      self._finish._worldBound = True

      # Back up the physical keys for restarting and saving
      self._backupKeys = [k for k in self._physicalKeys]

      self._miniMap = self.createMiniMap()
      
   def draw(self, screen):
      """Draw the level to the screen"""

      # Draw the finishing block to the screen
      self._finish.draw(screen)

      # Draw the vertical walls to the screen
      for gate in self._walls:
         gate.draw(screen)

      # Draw the horizontal platforms to the screen
      for gate in self._platforms:
         gate.draw(screen)

      # Draw the keys to the screen
      for key in self._physicalKeys:
         key.draw(screen)

      # Draw the player to the screen
      self._player.draw(screen)

      # Draw the players collected keys to the screen
      r = 10 # Radius of orbs
      for i, orb in enumerate(self._player.getKeys()):
         color = self._colors.get(orb, None)
         if color != None:
            pygame.draw.circle(screen, color, ((i+1) * int(2.5 * r) ,self._SCREEN_SIZE[1]-25), r)

      # If the game has been won, display winning message to the screen
      if self._won:
         screen.blit(self._font.render("You Have Won", False, (0,0,0)),
                     (self._SCREEN_SIZE[0]//2,self._SCREEN_SIZE[1]//2))

      # Draw the minimap to the screen if it should be displayed
      if self._showMiniMap:
         for room in self._miniMap:
            room.draw(screen)
         self._pointer.draw(screen)

   def handleEvent(self, event):
      """Handle events for the level"""

      # Handle the player's events based on the win condition
      if not self._won:
         self._player.move(event)
      else:
         for k in self._player._movement.keys(): self._player._movement[k] = False

   def update(self, worldsize, ticks):
      """Update the level state and display"""

      # Update the offset based on the player's location
      self._player.updateOffset(self._player, self._SCREEN_SIZE, self._WORLD_SIZE)

      # Update the player object (prevents player from phasing through walls)
      self._player.update(worldsize, ticks, self._platformParts, self._wallParts)
      
      # Allow the avatar to collect keys
      for key in self._physicalKeys:
        if key.getCollideRect().colliderect(self._player.getCollideRect()):
            self._player.giveKey(key.getType())
            key.collect()

      # Remove keys that have been collected
      self._physicalKeys = [key for key in self._physicalKeys if not key.collected()]

      # End the game when the player reaches the end node
      if self._player.getCollideRect().colliderect(self._finish.getCollideRect()):
         self._won = True

      # Update the minimap
      self.updateMiniMap()

   def plot(self):
      """Generate a network x plot for the level"""
      # Create a color mapping to visualize key locations
      color_map = []
      for node in self._g:
          for gate in self._gates:
              if self._keys[gate] == node and gate in self._colors.keys():
                  if gate in ["double_jump","shrink"]:
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

   font = pygame.font.SysFont("Times New Roman", 32)

   #Update the title for the window
   pygame.display.set_caption('Maze Game')
   
   #Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   roomDimensions = (18,6) # in units u

   level = LevelTester(SCREEN_SIZE, WORLD_SIZE, roomDimensions)
   
   ordering = {"neutral":["shrink","orange"],"shrink":"double_jump",
               "orange":"grey","double_jump":"blue","blue":"white",}

   h_mapping = ["neutral","shrink","blue","white","grey","double_jump"]
   v_mapping = ["neutral",("double_jump","neutral"),"blue","white","grey",
                ("orange","blue")]
   
   endNode   = n*m
   startNode = 1
   assert n*m > 3*len(ordering) # A reasonable assumption that will hopefully prevent an infinite loop
   assert 0 < endNode <= n*m
   assert 0 < startNode <= n*m
   assert startNode != endNode
   level.makeMap(m,n,ordering,h_mapping,v_mapping,endNode,startNode,.5)
   level.prepareMap()

   loadmenu = Menu((SCREEN_SIZE[0]//2 - 250,SCREEN_SIZE[1]//2-150),
                       (500,300), "Load")
   loadmenu.close()

   savemenu = Menu((SCREEN_SIZE[0]//2 - 250,SCREEN_SIZE[1]//2-150),
                       (500,300), "Save")
   savemenu.close()

   # Create the game clock after all of the preprocessing is done
   # This prevents initial lag from effecting the beginning of the game
   gameClock = pygame.time.Clock()

   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick(60) # Throttle the frame rate to prevent jerkiness

      #Draw the background to the screen
      screen.fill((140,50,20))

      level.draw(screen)

      if loadmenu.getDisplay():
         loadmenu.draw(screen)

      if savemenu.getDisplay():
         savemenu.draw(screen)
      
      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            
            # change the value to False, to exit the main loop
            RUNNING = False
 
         if event.type==pygame.KEYDOWN:
            # Load in a saved map when control + o is pressed
            if event.key == pygame.K_o and \
               event.mod & pygame.KMOD_CTRL:
               loadmenu.display()
            # Load in a saved map when control + o is pressed
            if event.key == pygame.K_s and \
               event.mod & pygame.KMOD_CTRL:
               savemenu.display()
            # Plot the current mapping using networkx and matplotlib
            if event.key == pygame.K_p and \
               event.mod & pygame.KMOD_CTRL:
               level.plot()
               gameClock.tick() # effectively pauses the clock
               gameClock.tick() # while the plot is displayed
            # Generate a new map when control + n is pressed 
            if event.key == pygame.K_n and \
               event.mod & pygame.KMOD_CTRL:
               level.newMap()
               gameClock.tick() # effectively pauses the clock for
               gameClock.tick() # a reload
            if event.key == pygame.K_r and \
               event.mod & pygame.KMOD_CTRL:
               level.restart()
            if event.key == pygame.K_m and \
               not loadmenu.getDisplay() and \
               not savemenu.getDisplay():
               level._showMiniMap = not level._showMiniMap

         # If not loading or saving, handle the games events
         if not loadmenu.getDisplay() and not savemenu.getDisplay():
            level.handleEvent(event)

         if loadmenu.getDisplay():
            sel = loadmenu.handleEvent(event)
            if sel != None:
               if loadmenu._tabs.getActive() == 1: 
                  level.loadTemplate("saves\\templates\\" + sel + ".mapdat")
               else:
                  level.loadMap("saves\\maps\\" + sel + ".mapfile")

         if savemenu.getDisplay():
            sel = savemenu.handleEvent(event)
            if sel != None:
               if savemenu._tabs.getActive() == 1: 
                  level.saveTemplate("saves\\templates\\" + sel + ".mapdat")
               else:
                  level.saveMap("saves\\maps\\" + sel + ".mapfile")

      #Calculate ticks
      ticks = gameClock.get_time() / 1000
      
      level.update(WORLD_SIZE, ticks)

   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()




