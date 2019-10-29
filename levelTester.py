import pygame, latticeCreator, grapher
from room import Room
from room import Connector

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

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

   colors = {"red":(255,0,0), "green":(0,255,0), "blue":(0,0,255),
             "orange":(255,165,0)}

   m = 3
   n = 2
   rooms = []
   for y in range(n):
       for x in range(m):
           rooms.append(Room(((100*x) + 25,(100*y) + 25)))
   dimensions = (m,n)
   ordering = {"red":"blue","blue":"orange","orange":"green"}
   gates = grapher.getGateOrder(ordering)
   keys = {gate:1 for gate in gates}
   g = latticeCreator.generateViableMap(dimensions, gates, keys)

   for x in range(len(rooms)):
       # Remove rooms that are not part of the graph
       if not x+1 in g:
           rooms.remove(rooms[x])
           
   lines = []
   for x in range(len(rooms)):
       for y in range(len(rooms)):
           if x != y:
               print("this is happening")
               lines.append(Connector(rooms[x], rooms[y]))
   #room = Room((100,100), (255,0,0))

   RUNNING = True

   while RUNNING:

      #Draw the background to the screen
      screen.fill((140,50,20))

      for room in rooms:
          room.draw(screen)

      for line in lines:
          line.draw(screen, (25,25))
      
      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False

   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()


