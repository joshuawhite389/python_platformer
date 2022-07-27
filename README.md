# python_platformer

## Basics of Pygame platformer:

  There is a surface with tile sprites, player sprite, enemy sprites drawn onto it
  
  The collision of these sprites make up the basic mechanics of the game
  
  What remains is art work, polish, and "fun"
  
  *Below, "customizable code" refers to parts of the code that might be reasonably easy or fun to modify*
  
## main.py

  Draw a surface and set the framerate with pygame.time.Clock()
  
  Main game loop - this listens to events with pygame.event.get()- pygame.QUIT
  The surace we initiate here is populated with everything on level.py
  
## level.py

  This is where the bulk of the game resides
  
  We use the level class to call all of our other classes- player, enemy, tiles, etc.
  
  ### Customizable code:
  
    world_shift, scroll_x: we can change how the camera changes with the player
    
    if changing graphics or sprites, most of this will have to be re-written as much of it is hardcoded for he images currently being used
    
## player.py

Contains everything needed to render player outside of context of the level

level.py contains animations for jumping particles effects (they are needed only in the context of ground)

  ### Customizable code:
    
    key input can be changed to use different keys on keyboard or we can set up a controller to be used
    
    gravity and jump mechanic can be altered here - apply_gravity, self.gravity, self.jump_speed
    
    change how fast the character runs - self.speed
    
    change the animation rate
    
    import a different character sprite - import_character_assets

## enemy.py

## tiles.py

## support.py

## settings.py

## decoration.py

## dust_particles.py

## game_data.py
