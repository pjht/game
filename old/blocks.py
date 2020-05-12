import pygame
import os
import lib.constants as constants
from lib.gameregistry import GameRegistry
from lib.block import Block
from lib.inventory import Inventory
dy_blocks={}

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
  global dy_blocks
  dy_blocks[klass_name]=name
  return klass

make_block("BlockStone","stone")
make_block("BlockTree","tree",False,("wood",8))
make_block("BlockGrass","grass",True)
make_block("BlockWood","wood")
make_block("BlockCoal","coal_ore")
GameRegistry.registerFuel("coal_ore",8)
make_block("BlockIron","iron_ore")
make_block("ItemIronIngot","iron_ingot",False)
#make_block("ItemCoal","coal",False)
class BlockDoor(Block):
  unlocalisedName="door"
  openDoor=pygame.image.load(os.path.join("tiles","door_open.png"))

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

  def interactData(self):
    return {"clear":self.clear}

  def loadData(self,data):
    self.clear=data["clear"]

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

  def interactData(self):
    return {"inv":self.inv}

  def loadData(self,data):
    self.inv=data["inv"]

class BlockFurnace(Block):
  unlocalisedName="furnace"
  frames=[]

  @classmethod
  def init(cls):
    GameRegistry.registerBlock(cls,cls.unlocalisedName)
    Block.registerTexture(cls.unlocalisedName)
    for i in range(3):
      path=os.path.join("animation",cls.unlocalisedName,"{}.png".format(i))
      img=pygame.image.load(path)
      cls.frames.append(img)

  def __init__(self,x,y,screen):
    Block.__init__(self,x,y,screen)
    self.setTextureName(BlockFurnace.unlocalisedName)
    self.unlocalisedName=BlockFurnace.unlocalisedName
    self.frameno=0
    self.forward=True
    self.burn=False
    self.count=0
    self.inp=""
    self.inp_amount=0
    self.outp=""
    self.outp_amount=0
    self.fuel=""
    self.fuel_amount=0
    self.fuel_num=0
    self.originator=True

  def interact(self,inv):
    sel=inv.selected
    if sel!="":
      if sel in GameRegistry.fuels.keys():
        if self.fuel!="" and sel!=self.fuel:
          return
        self.fuel=sel
        self.fuel_num=GameRegistry.fuels[sel]
        self.fuel_amount+=1
        if self.inp!="":
          if self.burn==False:
            self.fuel_amount-=1
            self.burn=True
      else:
        if self.inp!="" and sel!=self.inp:
          return
        if not sel in GameRegistry.smelting.keys():
          return
        self.inp_amount+=1
        self.inp=sel
        if self.burn==False and self.fuel!="":
          self.fuel_amount-=1
          self.burn=True
      inv.remove(sel)
    else:
      if self.outp!="":
        inv.addTile(self.outp,self.outp_amount)
        self.outp=""
        self.outp_amount=0
    self.originator=True

  def getTexture(self):
    if self.burn:
      self.count+=1
      if self.count==10:
        self.update()
        self.count=0
      img=BlockFurnace.frames[self.frameno]
      if self.forward:
        self.frameno+=1
        if self.frameno>2:
          self.frameno=1
          self.forward=False
      else:
        self.frameno-=1
        if self.frameno<0:
          self.frameno=1
          self.forward=True
      return img
    else:
      return False
    self.mp_upd=True

  def update(self):
    self.fuel_num-=1
    if self.inp=="":
      self.burn=False
      return
    if self.fuel_num<=0:
      if self.fuel_amount<=0:
        self.burn=False
        self.fuel=""
        return
      else:
        self.fuel_amount-=1
        self.fuel_num=GameRegistry.fuels[self.fuel]
    if self.inp!="":
      if self.inp in GameRegistry.smelting:
        self.inp_amount-=1
        self.outp=GameRegistry.smelting[self.inp]
        self.outp_amount+=1
        if self.inp_amount<=0:
          self.inp=""
    if self.originator:
      self.mp_upd=True

  def loadData(self,data):
    self.frameno=data["frameno"]
    self.forward=data["forward"]
    self.burn=data["burn"]
    self.count=data["count"]
    self.inp=data["inp"]
    self.inp_amount=data["inp_amount"]
    self.outp=data["outp"]
    self.outp_amount=data["outp_amount"]
    self.fuel=data["fuel"]
    self.fuel_amount=data["fuel_amount"]
    self.fuel_num=data["fuel_num"]
    self.originator=False

  def interactData(self):
    self.mp_upd=False
    return {
      "frameno":self.frameno,
      "forward":self.forward,
      "burn":self.burn,
      "count":self.count,
      "inp":self.inp,
      "inp_amount":self.inp_amount,
      "outp":self.outp,
      "outp_amount":self.outp_amount,
      "fuel":self.fuel,
      "fuel_amount":self.fuel_amount,
      "fuel_num":self.fuel_num
    }
