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
    for dir in dirs:
      frame_array=[0,0,0]
      i=0
      while i<num_frames:
        img_name="{}_{}.png".format(dir,i)
        frame_array[i]=pygame.image.load(os.path.join("sprites",type,img_name))
        i+=1
      frames[dir]=frame_array
    return frames

  def __init__(self,x,y,screen,type,*groups):
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
