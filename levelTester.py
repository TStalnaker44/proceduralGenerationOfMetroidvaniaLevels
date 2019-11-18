import pygame, latticeCreator, grapher, copy
from room import Room
from room import Connector
from player import Player


m = 6
n = 6

SCREEN_SIZE = (n*100,m*100)

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

   colors = {"grey":(80,80,80),"red":(255,0,0), "green":(0,255,0), "blue":(0,0,255),
             "orange":(255,165,0),"white":(255,255,255)}

   won = False

   # Create a graph model
   dimensions = (m,n)
   ordering = {"grey":"red","red":"blue","blue":["orange","white"],"orange":"green"}
   gates = grapher.getGateOrder(ordering)
   keys = {gate:1 for gate in gates}
   g = latticeCreator.generateViableMap(dimensions, gates, keys, .5)

   # Create rooms based on the model
   rooms, c = [], 0
   for y in range(m):
       for x in range(n):
         key =  None
         rooms.append(Room(((100*x) + 25,(100*y) + 25), (c,0,0)))
         c+=1

   # Color rooms with keys
   for key in keys.keys():
      for i, room in enumerate(rooms):
         if keys[key] == i+1:
            room.color(colors[key])
            break

   # Add connections between rooms
   lines = Connector()
   for edge in g.edges(data=True):
      lineColor = colors[edge[2]["object"]]
      lines.addLine(rooms[edge[0]-1], rooms[edge[1]-1], lineColor, 3)

   # Create a copy of the list to allow mutations without error
   roomCopy = copy.copy(rooms)
   for x in range(len(roomCopy)):
       # Remove rooms that are not part of the graph
       if not x+1 in g:
           rooms.remove(roomCopy[x])

   # Create a player object
   startPos = rooms[0].getCenter()
   player = Player([startPos[0]+20,startPos[1]+20], 100, (m,n))
           
   RUNNING = True

   while RUNNING:

      #Draw the background to the screen
      screen.fill((140,50,20))

      for room in rooms:
          room.draw(screen)

      lines.draw(screen, (25,25))

      player.draw(screen)

      r = 10
      for i, orb in enumerate(player.getKeys()):
         pygame.draw.circle(screen, colors[orb], ((i+1) * int(2.5 * r) ,SCREEN_SIZE[1]-25), r)

      if won:
         screen.blit(font.render("You Have Won", False, (0,0,0)),
                     (35*n,44*m))
      
      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False

         if not won:
            # Determine which square are reachable from current grid
            # position and over which gating types
            connections = {}
            for edge in g.edges(data=True):
               if edge[0] == player.getCurrentSquare()+1:
                  connections[edge[1]] = edge[2]["object"]
               elif edge[1] == player.getCurrentSquare()+1:
                  connections[edge[0]] = edge[2]["object"]
            player.handleEvent(event, connections)

      if not won:
         currentSquare = player.getCurrentSquare()+1
         if currentSquare in keys.values():
            for key in keys.keys():
               if key not in player.getKeys() and \
                  keys[key] == currentSquare:
                  player.giveKey(key)
                  break

         if currentSquare == m*n:
            won = True

   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()


