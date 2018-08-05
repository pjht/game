class GameRegistry:
  block_classes={}
  recipes={}
  smelting={}
  fuels={}

  @classmethod
  def registerBlock(cls,klass,name):
    if not klass in cls.block_classes.keys():
      cls.block_classes[name]=klass

  @classmethod
  def registerCrafting(cls,reqs,result):
    if not result in cls.recipes.keys():
      cls.recipes[result]=reqs

  @classmethod
  def registerSmelting(cls,inp,outp):
    if not inp in cls.smelting.keys():
      cls.smelting[inp]=outp

  @classmethod
  def registerFuel(cls,name,amount):
    if not name in cls.fuels.keys():
      cls.fuels[name]=amount
