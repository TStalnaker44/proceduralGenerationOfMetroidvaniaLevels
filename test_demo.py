"""
Author: Trevor Stalnaker
File: test_demo.py
"""

import pygame
from key import Key
from gate import Gate
from avatar import Avatar
from wall import Wall

# Dynamically determine screen size based on grid size
SCREEN_SIZE = (500,500)
WORLD_SIZE = (500,500)

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

   avatar = Avatar((0,0))

   keys = [Key((200,200),(255,0,0),0), Key((300,300),(0,255,0),1)]

   temp = [Wall((100,450),1,0), Wall((200,400),1,0), Wall((0,100),1,0)]
   platforms = [Gate((300,450),(0,255,0),1,1),
                Gate((100,100),(0,255,0),1,1)]
   for t in temp:
      platforms += t.getComponents()

   walls = [Gate((400,400),(255,0,0),0),Gate((100,100),(0,255,0),1)]

##   ws = [Wall((100,60),0,0), Wall((100,140),0,0), Wall((100,60),1,0),
##         Wall((70,60),1,0)]

   comps = []

##   for w in ws:
##      comps += w.getComponents()

   greenGate = [Gate((300,200),(0,255,0),1),
             Gate((300,160),(120,120,120),99),
             Gate((300,240),(120,120,120),99)]

   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      #Draw the background to the screen
      screen.fill((255,255,255))

      for key in keys:
          key.draw(screen)

      for wall in walls:
          wall.draw(screen)

      avatar.draw(screen)
      
      for w in platforms:
         w.draw(screen)

      for c in greenGate:
         c.draw(screen)
      
      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            
            # change the value to False, to exit the main loop
            RUNNING = False

         avatar.move(event)

      #Calculate ticks
      ticks = gameClock.get_time() / 1000
      
      avatar.update(WORLD_SIZE, ticks, platforms, walls)

      # Allow the avatar to collect keys
      for key in keys:
        if key.getCollideRect().colliderect(avatar.getCollideRect()):
            avatar.giveKey(key.getType())
            key.collect()
            print(avatar._keys)

      # Remove keys that have been collected
      keys = [key for key in keys if not key.collected()]

   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()




