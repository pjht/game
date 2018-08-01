from lib import block,blockregistry
from lib.blockregistry import BlockRegistry
from lib.block import Block
import pygame

def make_block(klass_name,name,clear):
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
  BlockRegistry.registerBlock(klass,name)
  glob=globals()
  glob[klass_name]=klass
  return klass

make_block("BlockStone","stone",False)
make_block("BlockTree","tree",False)
make_block("BlockGrass","grass",True)
