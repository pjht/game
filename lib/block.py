from pygame.sprite import Sprite
import pygame.image
import os
from . import constants
class Block(Sprite):
  textures={}
  background=pygame.image.load(os.path.join("tiles","{}.jpeg".format(constants.BACKGROUND)))
  @classmethod
  def init(cls):
    subclasses=cls.__subclasses__()
    for klass in subclasses:
      klass.init()

  def __init__(self,x,y,screen):
    super().__init__()
    self.x=x
    self.y=y
    self.screen=screen
    self.tname=None
    self.clear=False
    self.unlocalisedName=""
    self.customDraw=False

  def draw(self):
    if self.tname==None:
      raise Exception("No texture name for block. Did you forget to call setTextureName?")
    self.screen.blit(Block.background,(self.x*constants.TILESIZE,self.y*constants.TILESIZE))
    texture=self.getTexture()
    if texture==False:
      texture=Block.textures[self.tname]
    self.screen.blit(texture,(self.x*constants.TILESIZE,self.y*constants.TILESIZE))

  def setTextureName(self,name):
    if not name in Block.textures.keys():
      Block.textures[name]=pygame.image.load(os.path.join("tiles","{}.jpeg".format(name)))
    self.tname=name

  def interact(self):
    pass

  def getTexture(self):
    return False