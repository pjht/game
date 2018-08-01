import pygame
import os
import random
from lib import *
import lib.constants as constants
from lib.map import Map
from lib.character import Character
from blocks import *
from player import *
from time import sleep
DELAY=0.1
pygame.init()
block.Block.init()
pygame.display.set_caption("game")
screen=pygame.display.set_mode((constants.WINDWIDTH,constants.WINDHEIGHT))
map=Map(screen)
player=Player(0,0,map,screen)
if __name__ == '__main__':
  running=True
  move=False
  key_to_dir={
    pygame.K_UP:"up",
    pygame.K_DOWN:"down",
    pygame.K_LEFT:"left",
    pygame.K_RIGHT:"right"
  }
  while running:
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        running=False
      elif event.type==pygame.KEYDOWN:
        if event.key==pygame.K_PERIOD:
          player.interact()
        if event.key==pygame.K_SLASH:
          player.attack()
        if event.key in key_to_dir.keys():
          move=True
          dir=key_to_dir[event.key]
      elif event.type==pygame.KEYUP:
        move=False
        player.frame=1
    if move:
      player.move(dir)
    map.draw()
    player.draw()
    sleep(DELAY)
