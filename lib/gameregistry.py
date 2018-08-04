class GameRegistry:
  block_classes={}
  recipes={}

  @classmethod
  def registerBlock(cls,klass,name):
    if not klass in cls.block_classes.keys():
      cls.block_classes[name]=klass

  @classmethod
  def registerCrafting(cls,reqs,result):
    if not result in cls.recipes.keys():
      cls.recipes[result]=reqs
