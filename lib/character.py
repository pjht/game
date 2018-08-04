from pygame.sprite import Sprite
import pygame.image
import os
from . import constants
class Character(Sprite):
  @staticmethod
  def loadFrames(type):
    frames={}
    dirs=["up","down","left","right"]
    num_frames=3
    for dir in dirs:
      frame_array=[0,0,0]
      i=0
      while i<num_frames:
        img_name="{}_{}.png".format(dir,i)
        frame_array[i]=pygame.image.load(os.path.join("sprites",type,img_name))
        i+=1
      frames[dir]=frame_array
    return frames

  def __init__(self,x,y,type,map,screen,*groups):
    super().__init__(groups)
    self.x=x
    self.y=y
    self.screen=screen
    self.frames=self.loadFrames(type)
    self.frame=1
    self.dir="right"
    self.map=map

  def draw(self):
    img=self.frames[self.dir][self.frame]
    self.screen.blit(img,(self.x,self.y))
    pygame.display.flip()

  def move(self,dir):
    old_x=self.x
    old_y=self.y
    self.dir=dir
    if dir=="up":
      self.y-=constants.PLAYER_MOVE
    elif dir=="down":
      self.y+=constants.PLAYER_MOVE
    elif dir=="left":
      self.x-=constants.PLAYER_MOVE
    elif dir=="right":
      self.x+=constants.PLAYER_MOVE
    self.frame+=1
    if self.frame>2:
      self.frame=0
    if self.x>=constants.WINDWIDTH:
      self.x=old_x
    if self.x<0:
      self.x=old_x
    if self.y>=(constants.WINDHEIGHT-(constants.EXTRAROWS*constants.TILESIZE)):
      self.y=old_y
    if self.y<0:
      self.y=old_y
    tile=self.map.tileAt(self.x/constants.TILESIZE,self.y/constants.TILESIZE)
    if not tile.clear:
      self.x=old_x
      self.y=old_y
