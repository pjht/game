import pygame
import os
import lib.constants as constants
from lib.gameregistry import GameRegistry
from lib.block import Block
from lib.inventory import Inventory

def make_block(klass_name,name,clear=False,drops=False):
  def blk_init():
    pass
  def init(self,x,y,screen):
    Block.__init__(self,x,y,screen)
    self.setTextureName(name)
    self.clear=clear
    self.drops=drops
    self.unlocalisedName=name
  attr_table={
    "unlocalisedName":name,
    "__init__":init,
    "init":blk_init,
  }
  klass=type(klass_name,(Block,),attr_table)
  GameRegistry.registerBlock(klass,name)
  Block.registerTexture(name)
  glob=globals()
  glob[klass_name]=klass
  return klass

make_block("BlockStone","stone")
make_block("BlockTree","tree",False,("wood",8))
make_block("BlockGrass","grass",True)
make_block("BlockWood","wood")

class BlockDoor(Block):
  unlocalisedName="door"
  openDoor=pygame.image.load(os.path.join("tiles","door_open.jpeg"))

  @classmethod
  def init(cls):
    GameRegistry.registerBlock(cls,cls.unlocalisedName)
    Block.registerTexture(cls.unlocalisedName)

  def __init__(self,x,y,screen):
    Block.__init__(self,x,y,screen)
    self.setTextureName(BlockDoor.unlocalisedName)
    self.unlocalisedName=BlockDoor.unlocalisedName

  def interact(self,inv):
    self.clear=not self.clear
    pygame.mixer.Sound("door.ogg").play().set_volume(0.2)

  def getTexture(self):
    if self.clear:
      return BlockDoor.openDoor
    else:
      return False

class BlockWorkbench(Block):
  unlocalisedName="workbench"

  @classmethod
  def init(cls):
    GameRegistry.registerBlock(cls,cls.unlocalisedName)
    Block.registerTexture(cls.unlocalisedName)

  def __init__(self,x,y,screen):
    Block.__init__(self,x,y,screen)
    self.setTextureName(BlockWorkbench.unlocalisedName)
    self.unlocalisedName=BlockWorkbench.unlocalisedName
    self.inv=Inventory()

  def interact(self,inv):
    selected=inv.selected
    if selected!="":
      inv.remove(selected)
      self.inv.addTile(selected,1)
    else:
      if self.inv.inv in GameRegistry.recipes.values():
        out=""
        for outp,reqs in GameRegistry.recipes.items():
          if self.inv.inv==reqs:
            out=outp
            break
        inv.addTile(out,1)
        self.inv.clear()
