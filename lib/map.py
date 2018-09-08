import pygame
import random
from pygame.sprite import Group
from . import block,gameregistry
from . import constants
from .gameregistry import GameRegistry
from .block import Block
class Map:
  def __init__(self,screen):
    super().__init__()
    self.tiles={}
    self.screen=screen
    self.generate()

  def addTile(self,tname,x,y):
    klass=GameRegistry.block_classes[tname]
    tile=klass(x,y,self.screen)
    self.tiles[(x,y)]=tile

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

  def draw(self,centerx,centery):
    topleftx=centerx-constants.CENTERX
    toplefty=centery-constants.CENTERY
    x=topleftx
    y=toplefty
    while True:
      tile=self.tileAt(x,y)
      if tile:
        tile.draw(x-topleftx,y-toplefty)
      x+=1
      if x==topleftx+constants.PORTWIDTH:
        x=topleftx
        y+=1
        if y==toplefty+constants.PORTHEIGHT:
          break
    pygame.display.flip()

  def tileAt(self,x,y):
    try:
      return self.tiles[(x,y)]
    except KeyError as e:
      return None
