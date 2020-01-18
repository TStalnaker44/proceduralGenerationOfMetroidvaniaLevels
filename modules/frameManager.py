
from pygame import image, Surface, Rect
from os.path import join


class FrameManager(object):
   """A singleton factory class to create and store frames on demand."""
   
   # The singleton instance variable
   _INSTANCE = None
   
   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._FM()
      
      return cls._INSTANCE
   
   # Do not directly instantiate this class!
   class _FM(object):
      """An internal FrameManager class to contain the actual code. Is a private class."""
      
      # Folder in which images are stored
      _IMAGE_FOLDER = "images"
      
      # Static information about the frame sizes of particular image sheets.
      _FRAME_SIZES = {
         "faces.png":(32,32),
         "starAnim.png" : (32,32),
         "flowers-color-key.png" :  (114,116),
         "rose-anim.png" :  (114,116),
         "water-lilly.png" : (47,49),
         "tempSquirrel.png" : (128,128),
         "background.png" : (2400,500),
         "tempChipmunk.png":(128,128),
         "tempFox.png":(128,128),
         "turtle.png":(128,128),
         "tempBear.png":(128,128),
         "tempSnake.png":(128,128),
         "tempDeer.png":(128,128),
         "tempRabbit.png":(128,128),
         "shmoo.png":(32,32),
         "tempHedgeHog.png":(128,128),
         "cow.png":(128,128),
         "combatBackground":(1200,500),
         "acorn.png":(32,32),
         "dirtpile.png":(32,32),
         "tradeDesk.png":(750,422),
         "squirrel.png":(32,32),
         "merchant.png":(64,64),
         "tree.png":(128,128),
         "rocks.png":(32,32),
         "new_squirrel.png":(32,32),
         "sword.png":(32,32),
         "spear.png":(32,32),
         "stick.png":(32,32),
         "hide_armor.png":(32,32),
         "leather_armor.png":(32,32),
         "iron_armor.png":(32,32),
         "berries.png":(32,32),
         "nutsoup.png":(32,32),
         "pecanpie.png":(32,32),
         "shovel.png":(32,32),
         "pickax.png":(32,32),
         "crowbar.png":(32,32),
         "healthpotion.png":(32,32),
         "new_fox.png":(48,34),
         "new_rabbit.png":(40,40),
         "new_bear.png":(64,64),
         "new_deer.png":(72,75),
         "face_0.png":(32,32),
         "face_1.png":(32,32),
         "face_2.png":(32,32),
         "face_3.png":(32,32),
         "face_4.png":(32,32),
         "title.png":(1280,720),
         "new_chipmunk.png":(32,25),
         "new_hedgehog.png":(34,32)
      }
      
      # A default frame size
      _DEFAULT_FRAME = (32,32)
      
      # A list of images that require to be loaded with transparency
      _TRANSPARENCY = []
      
      # A list of images that require to be loaded with a color key
      _COLOR_KEY = ["tempSquirrel.png", "tempChipmunk.png","tempFox.png",
                    "tempBear.png","turtle.png", "tempSnake.png", "tempDeer.png",
                    "tempRabbit.png", "shmoo.png","tempHedgeHog.png","tradeDesk.png",
                    "acorn.png", "dirtpile.png","cow.png","squirrel.png",
                    "squirrel_walk_cycle.png","merchant.png","tree.png",
                    "rocks.png","new_squirrel.png","sword.png","spear.png",
                    "stick.png","hide_armor.png","leather_armor.png",
                    "iron_armor.png","berries.png","nutsoup.png","shovel.png",
                    "pickax.png","crowbar.png","healthpotion.png","pecanpie.png",
                    "new_fox.png","new_rabbit.png","new_bear.png","new_deer.png",
                    "ally_state.png","face_0.png","face_1.png","face_2.png","face_3.png",
                    "face_4.png","new_chipmunk.png","new_hedgehog.png"]
      
      
      
      def __init__(self):
         # Stores the surfaces indexed based on file name
         # The values in _surfaces can be a single Surface
         #  or a two dimentional grid of surfaces if it is an image sheet
         self._surfaces = {}
      
      
      def __getitem__(self, key):
         return self._surfaces[key]
   
      def __setitem__(self, key, item):
         self._surfaces[key] = item
      
      
      def getFrame(self, fileName, offset=None):
         # If this frame has not already been loaded, load the image from memory
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, offset != None)
         
         # If this is an image sheet, return the correctly offset sub surface
         if offset != None:
            return self[fileName][offset[1]][offset[0]]
         
         # Otherwise, return the sheet created
         return self[fileName]
      
      def _loadImage(self, fileName, sheet=False):
         # Load the full image
         fullImage = image.load(join(FrameManager._FM._IMAGE_FOLDER, fileName))
         
         # Look up some information about the image to be loaded
         transparent = fileName in FrameManager._FM._TRANSPARENCY
         colorKey = fileName in FrameManager._FM._COLOR_KEY
         
         # Detect if a transparency is needed
         if transparent:
            fullImage = fullImage.convert_alpha()
         else:
            fullImage = fullImage.convert()
         
         # If the image to be loaded is an image sheet, split it up based on the frame size
         if sheet:
               
            self[fileName] = []
            spriteSize = FrameManager._FM._FRAME_SIZES.get(fileName, FrameManager._FM._DEFAULT_FRAME)
            
            sheetDimensions = fullImage.get_size()
            
            for y in range(0, sheetDimensions[1], spriteSize[1]):
               self[fileName].append([])
               for x in range(0, sheetDimensions[0], spriteSize[0]):
                  
                  # If we need transparency
                  if transparent:
                     frame = Surface(spriteSize, pygame.SRCALPHA, 32)
                  else:
                     frame = Surface(spriteSize)
                     
                  frame.blit(fullImage, (0,0), Rect((x,y), spriteSize))
                  
                  # If we need to set the color key
                  if colorKey:
                     frame.set_colorkey(frame.get_at((0,0)))
                  
                  self[fileName][-1].append(frame)
         else:
            
            self[fileName] = fullImage
               
            # If we need to set the color key
            if colorKey:
               self[fileName].set_colorkey(self[fileName].get_at((0,0)))
               
            
         
         
# Set up an instance for others to import         
FRAMES = FrameManager.getInstance()
