import pygame
import random
from pygame.sprite import Group
from . import block,gameregistry
from . import constants
from .gameregistry import GameRegistry
from .block import Block
import pickle
class Map:
  def __init__(self,screen,sock=None):
    super().__init__()
    self.tiles={}
    self.screen=screen
    self.sock=sock

  def send_str(self,str):
    self.sock.send((str+"\n").encode("utf-8"))

  def recvall(self):
    BUFF_SIZE=4096
    data=b''
    while True:
      part=self.sock.recv(BUFF_SIZE)
      data+=part
      if len(part)<BUFF_SIZE:
        break
    return data


  def addTile(self,tname,x,y):
    klass=GameRegistry.block_classes[tname]
    tile=klass(x,y,self.screen)
    self.tiles[(x,y)]=tile
  
  def generateTile(self,x,y):
    num=random.randint(0,101)
    if num<5:
      num=random.randint(0,101)
      if num<50:
        self.addTile("tree",x,y)
      else:
        self.addTile("stone",x,y)
    else:
      self.addTile(constants.BACKGROUND,x,y)
      
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
        self.send_str("BLOCK_AT_POS")
        self.send_str(str(x))
        self.send_str(str(y))
        data=self.recvall()
        block=pickle.loads(data)
        block.screen=self.screen
        self.tiles[(x,y)]=block
      else:
        self.generateTile(x,y)
      return self.tiles[(x,y)]
