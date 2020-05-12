import pygame
import random
from pygame.sprite import Group
from . import block,gameregistry
from . import constants
from .gameregistry import GameRegistry
from .block import Block
import pickle
class Map:
  def __init__(self,screen,sock=None,uid=None):
    super().__init__()
    self.tiles={}
    self.screen=screen
    self.sock=sock
    self.uid=uid
    self.generate()

  def send_str(self,sock,str):
    # print(str)
    sock.send((str+"\n").encode("utf-8"))

  def recvall(self,sock):
    BUFF_SIZE=4096
    data=b''
    while True:
      part=sock.recv(BUFF_SIZE)
      data+=part
      if len(part)<BUFF_SIZE:
        break
    #print(pickle.loads(data))
    return data


  def addTile(self,tname,x,y):
    klass=GameRegistry.block_classes[tname]
    tile=klass(x,y,self.screen)
    self.tiles[(x,y)]=tile

  def generate(self):
    y=0
    while y<constants.MAPHEIGHT:
      x=0
      while x<constants.MAPWIDTH:
        num=random.randint(0,101)
        if num<5:
          num=random.randint(0,101)
          if num<50:
            self.addTile("tree",x,y)
          else:
            self.addTile("stone",x,y)
        else:
          self.addTile(constants.BACKGROUND,x,y)
        x+=1
      y+=1

  def draw(self,centerx,centery):
    topleftx=centerx-constants.CENTERX
    toplefty=centery-constants.CENTERY
    x=topleftx
    y=toplefty
    while True:
      tile=self.tileAt(x,y)
      if tile:
        tile.draw(x-topleftx,y-toplefty)
      x+=1
      if x==topleftx+constants.PORTWIDTH:
        x=topleftx
        y+=1
        if y==toplefty+constants.PORTHEIGHT:
          break

  def tileAt(self,x,y):
    try:
      return self.tiles[(x,y)]
    except KeyError as e:
      if self.sock:
        self.send_str(self.sock,"BLOCK_AT_POS")
        self.send_str(self.sock,str(x))
        self.send_str(self.sock,str(y))
        data=self.recvall(self.sock)
        block=pickle.loads(data)
        if block==None:
          name=""
          num=random.randint(0,101)
          if num<5:
            num=random.randint(0,101)
            if num<50:
              name="tree"
              self.addTile("tree",x,y)
            else:
              name="stone"
              self.addTile("stone",x,y)
          else:
            name=constants.BACKGROUND
            self.addTile(constants.BACKGROUND,x,y)
          self.send_str(self.sock,"PLACE_BLOCK_AT")
          self.send_str(self.sock,str(self.uid))
          self.send_str(self.sock,str(x))
          self.send_str(self.sock,str(y))
          self.send_str(self.sock,str(name))
        else:
          block.screen=self.screen
          self.tiles[(x,y)]=block
      else:
        print("Cannot contact server. Exiting")
        exit(1)
      return self.tiles[(x,y)]
