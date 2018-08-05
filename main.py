import pygame
import os
import random
import recipes
import sys
import select
import blocks
import lib.constants as constants
from lib.gameregistry import GameRegistry
from lib.map import Map
from lib.character import Character
from lib.block import Block
from player import *
from time import sleep
DELAY=0.1
pygame.init()
Block.init()
recipes.init()
pygame.display.set_caption("game")
screen=pygame.display.set_mode((constants.WINDWIDTH,constants.WINDHEIGHT))
map=Map(screen)
player=Player(0,0,map,screen)
player.inv.addTile("workbench",1)
if __name__ == '__main__':
  running=True
  move=False
  inv=False
  helvetica_neue=pygame.font.SysFont('Helvetica Neue',constants.FONTSIZE)
  key_to_dir={
    pygame.K_UP:"up",
    pygame.K_DOWN:"down",
    pygame.K_LEFT:"left",
    pygame.K_RIGHT:"right"
  }
  while running:
    if select.select([sys.stdin],[],[],0.0)[0]:
      cmd=input()
      cmd=cmd.split()
      if cmd[0]=="give":
        if len(cmd)==2:
          item=cmd[1]
          player.inv.addTile(item,1)
        elif len(cmd)==3:
          item=cmd[1]
          count=int(cmd[2])
          player.inv.addTile(item,count)
        else:
          print("give <item> [count]")
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        running=False
      elif event.type==pygame.KEYDOWN:
        if event.key==pygame.K_PERIOD:
          player.interact()
        if event.key==pygame.K_SLASH:
          player.attack()
        if event.key==pygame.K_j:
          player.inv.selPrev()
        if event.key==pygame.K_k:
          player.inv.clearSel()
        if event.key==pygame.K_l:
          player.inv.selNext()
        if event.key==pygame.K_e:
          inv=not inv
        if event.key==pygame.K_i:
          dy_blocks=blocks.dy_blocks
          Block.textures={}
          Block.init()
          for klass,unName in dy_blocks.items():
            Block.registerTexture(unName)
        if event.key in key_to_dir.keys():
          move=True
          dir=key_to_dir[event.key]
      elif event.type==pygame.KEYUP:
        move=False
        player.frame=1
    if move:
      player.move(dir)
    if inv:
      screen.fill([255,255,255])
      text=[]
      label=[]
      for item, count in player.inv.inv.items():
        text.append("{} {}".format(count,item))
      for line in text:
        label.append(helvetica_neue.render(line, True, (0,0,0)))
      for line in range(len(label)):
        screen.blit(label[line],(1,(line*constants.FONTSIZE)+(2*line)))
      pygame.display.flip()
    else:
      screen.fill([0,0,0])
      map.draw()
      player.draw()
      selected=player.inv.selected
      if selected!="":
        texture=Block.textures[selected]
        screen.blit(texture,(0*constants.TILESIZE,32*constants.TILESIZE))
      pygame.display.flip()
      sleep(DELAY)
