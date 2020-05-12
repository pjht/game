from pygame.sprite import Sprite
import pygame.image
import os
from time import sleep
from . import constants
class Block(Sprite):
  textures={}
  background=pygame.image.load(os.path.join("tiles","{}.png".format(constants.BACKGROUND)))
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
    self.drops=False
    self.mp_upd=False

  def draw(self,x,y):
    if self.tname==None:
      raise Exception("No texture name for block. Did you forget to call setTextureName()?".format())
    self.screen.blit(Block.background,(x*constants.TILESIZE,y*constants.TILESIZE))
    texture=self.getTexture()
    if texture==False:
      texture=Block.textures[self.tname]
    self.screen.blit(texture,(x*constants.TILESIZE,y*constants.TILESIZE))
  def setTextureName(self,name):
    if not name in Block.textures.keys():
      raise Exception("{} is not a valid texture. Did you forget to call registerTexture(\"{}\")?".format(name,name))
    self.tname=name

  @classmethod
  def registerTexture(cls,name):
    Block.textures[name]=pygame.image.load(os.path.join("tiles","{}.png".format(name)))

  def interact(self,inv):
    pass

  def getTexture(self):
    return False

  def interactData(self):
    return None

  def loadData(self,data):
    pass
