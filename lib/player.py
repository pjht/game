from lib.character import Character
import lib.constants as constants
from lib.inventory import Inventory
class Player(Character):
  def __init__(self,x,y,map,screen,uname,type,*groups):
    super().__init__(x,y,type,map,screen,*groups)
    self.inv=Inventory()
    self.uname=uname

  def facingTile(self):
    x=self.x
    y=self.y
    if self.dir=="up":
      y-=1
    elif self.dir=="down":
      y+=1
    elif self.dir=="left":
      x-=1
    elif self.dir=="right":
      x+=1
    if x>constants.MAPWIDTH-1:
      return False
    if x<0:
      return False
    if y>constants.MAPHEIGHT-1:
      return False
    if y<0:
      return False
    return (x,y)

  def interact(self):
    coords=self.facingTile()
    if coords==False:
      return
    tile=self.map.tileAt(coords[0],coords[1])
    name=tile.unlocalisedName
    if name=="grass":
      to_place=self.inv.selected
      if to_place=="":
        return
      self.map.tiles[coords[1]][coords[0]]=None
      self.map.addTile(to_place,coords[0],coords[1])
      self.inv.remove(to_place)
    else:
      tile.interact(self.inv)

  def attack(self):
    coords=self.facingTile()
    if coords==False:
      return
    tile=self.map.tileAt(coords[0],coords[1])
    name=tile.unlocalisedName
    if name=="grass":
      return
    self.map.tiles[coords[1]][coords[0]]=None
    self.map.addTile("grass",coords[0],coords[1])
    if tile.drops==False:
      self.inv.addTile(name,1)
    else:
      drop=tile.drops[0]
      amount=tile.drops[1]
      self.inv.addTile(drop,amount)

  def draw(self):
    oldx=self.x
    oldy=self.y
    self.x=16
    self.y=16
    super().draw()
    self.x=oldx
    self.y=oldy
