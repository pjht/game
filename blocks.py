import pygame
import os
import lib.constants as constants
from lib.gameregistry import GameRegistry
from lib.block import Block

def make_block(klass_name,name,clear=False):
  def blk_init():
    pass
  def init(self,x,y,screen):
    Block.__init__(self,x,y,screen)
    self.setTextureName(name)
    self.clear=clear
    self.unlocalisedName=name
  attr_table={
    "unlocalisedName":name,
    "__init__":init,
    "init":blk_init,
  }
  klass=type(klass_name,(Block,),attr_table)
  GameRegistry.registerBlock(klass,name)
  glob=globals()
  glob[klass_name]=klass
  return klass

make_block("BlockStone","stone")
make_block("BlockTree","tree")
make_block("BlockGrass","grass",True)

class BlockDoor(Block):
  unlocalisedName="door"
  openDoor=pygame.image.load(os.path.join("tiles","door_open.jpeg"))

  @classmethod
  def init(cls):
    GameRegistry.registerBlock(cls,cls.unlocalisedName)

  def __init__(self,x,y,screen):
    Block.__init__(self,x,y,screen)
    self.setTextureName(BlockDoor.unlocalisedName)

  def interact(self):
    self.clear=not self.clear
    pygame.mixer.Sound("door.ogg").play().set_volume(0.2)

  def getTexture(self):
    if self.clear:
      return BlockDoor.openDoor
    else:
      return False
