# python_platformer

##Basics of Pygame platformer:

  There is a surface with tile sprites, player sprite, enemy sprites drawn onto it
  
  The collision of these sprites make up the basic mechanics of the game
  
  What remains is art work, polish, and "fun"
  
##main.py

  Draw a surface and set the framerate with pygame.time.Clock()
  
  Main game loop - this listens to events with pygame.event.get() and the surace we initiate here is populated with everything on level.py
  
##level.py

  This is where the bulk of the game resides
  
  We use the level class to call all of our other classes- player, enemy, tiles, etc.
  
  ###Customizable code:
  
    world_shift, scroll_x: we can change how the camera changes with the player
    
