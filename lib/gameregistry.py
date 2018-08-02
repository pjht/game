class GameRegistry:
  block_classes={}

  @classmethod
  def registerBlock(cls,klass,name):
    if not klass in cls.block_classes:
      cls.block_classes[name]=klass
