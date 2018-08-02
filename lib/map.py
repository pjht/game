import pygame
import random
from pygame.sprite import Group
from . import block,gameregistry
from . import constants
from .gameregistry import GameRegistry
from .block import Block
class Map(Group):
  def __init__(self,screen):
    super().__init__()
    self.screen=screen
    self.generate()

  def addTile(self,tname,x,y):
    klass=GameRegistry.block_classes[tname]
    tile=klass(x,y,self.screen)
    super().add(tile)

  def generate(self):
    y=0
    while y<constants.MAPHEIGHT:
      x=0
      while x<constants.MAPWIDTH:
        num=random.randint(0,101)
        if num<5:
          num=random.randint(0,101)
          if num<50:
            self.addTile("tree",x,y)
          else:
            self.addTile("stone",x,y)
        else:
          self.addTile(constants.BACKGROUND,x,y)
        x+=1
      y+=1

  def draw(self):
    for s in self.sprites():
      s.draw()
    pygame.display.flip()

  def tileAt(self,x,y):
    tile=None
    for s in self.sprites():
      if s.x==x and s.y==y:
        tile=s
        break
    return tile
