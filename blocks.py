from lib import block,blockregistry
from lib.blockregistry import BlockRegistry
from lib.block import Block

class BlockStone(Block):
  @classmethod
  def init(cls):
    BlockRegistry.registerBlock(cls,"stone")

  def __init__(self,x,y,screen):
    super().__init__(x,y,screen)
    super().setTextureName("stone")

class BlockTree(Block):
  @classmethod
  def init(cls):
    BlockRegistry.registerBlock(cls,"tree")

  def __init__(self,x,y,screen):
    super().__init__(x,y,screen)
    super().setTextureName("tree")

class BlockGrass(Block):
  @classmethod
  def init(cls):
    BlockRegistry.registerBlock(cls,"grass")

  def __init__(self,x,y,screen):
    super().__init__(x,y,screen)
    super().setTextureName("grass")
    self.clear=True
