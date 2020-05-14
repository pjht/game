from pygame.sprite import Sprite
import pygame.image
import os
import lib.constants as constants
class PlayerImg(Sprite):
  @staticmethod
  def loadFrames(type):
    frames={}
    dirs=["up","down","left","right"]
    num_frames=3
    for direction in dirs:
      frame_array=[0,0,0]
      i=0
      while i<num_frames:
        img_name="{}_{}.png".format(direction,i)
        frame_array[i]=pygame.image.load(os.path.join("sprites",type,img_name))
        i+=1
      frames[direction]=frame_array
    return frames

  def __init__(self,screen,type,*groups):
    super().__init__(groups)
    self.screen=screen
    self.frames=self.loadFrames(type)
    self.frame=1
    self.direction="right"
    self.map=map

  def draw(self,x,y):
    img=self.frames[self.direction][self.frame]
    self.screen.blit(img,(x*constants.TILESIZE,y*constants.TILESIZE))
