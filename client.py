import pygame
import os
import random
import recipes
import sys
import select
import blocks
import socket
import pickle
import math
import lib.constants as constants
from lib.gameregistry import GameRegistry
from lib.map import Map
from lib.character import Character
from lib.block import Block
from player import *
from player_img import *
from time import sleep

def recv_str(sock,print_str=True):
  str=""
  ch=""
  while True:
    ch=sock.recv(1).decode("utf-8")
    if ch=="\n":
      break
    str+=ch
  # if print_str:
  #   print(str)
  return str

def send_str(sock,str):
  # print(str)
  sock.send((str+"\n").encode("utf-8"))

def recv_hash(sock):
  hash={}
  len=int(recv_str(sock,False))
  for _ in range(len):
    key=recv_str(sock,False)
    val=recv_str(sock,False)
    hash[key]=val
    # print(hash)
  return hash

def recvall(sock):
  BUFF_SIZE=4096
  data=b''
  while True:
    part=sock.recv(BUFF_SIZE)
    data+=part
    if len(part)<BUFF_SIZE:
      break
  return data

UNAME=input("UNAME:")
pygame.init()
Block.init()
recipes.init()
pygame.display.set_caption(UNAME)
screen=pygame.display.set_mode((constants.WINDWIDTH,constants.WINDHEIGHT))
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost",2000))
send_str(sock,"ADD_USR")
send_str(sock,UNAME)
my_uid=int(recv_str(sock))
uid_map={}
send_str(sock,"GET_MAP")
data=recvall(sock)
map=pickle.loads(data)
# The server's generated map does not have a screen. We fix that here.
map.screen=screen
for s in map.sprites():
  s.screen=screen
send_str(sock,"GET_POS_FOR_UID")
send_str(sock,str(my_uid))
x=int(recv_str(sock))*constants.TILESIZE
y=int(recv_str(sock))*constants.TILESIZE
fac=recv_str(sock)
player=Player(x,y,map,screen,UNAME,"player_local")
player.inv.addTile("workbench",1)
player.dir=fac
others={}
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
  send_str(sock,"GET_UID_MAP")
  uid_map=recv_hash(sock)
  # Will be filled with usernames of connected players
  connected=[]
  for uname,uid in uid_map.items():
    if uname!=UNAME:
      send_str(sock,"GET_POS_FOR_UID")
      send_str(sock,uid)
      x=int(recv_str(sock))*constants.TILESIZE
      y=int(recv_str(sock))*constants.TILESIZE
      fac=recv_str(sock)
      if uname in others:
        others[uname].x=x
        others[uname].y=y
      else:
        others[uname]=PlayerImg(x,y,screen,"player")
      others[uname].dir=fac
      connected.append(uname)
  # Remove all disconnected players
  others_copy=others.copy()
  for uname,uid in others_copy.items():
    if not uname in connected:
      del others[uname]
  send_str(sock,"GET_CHANGES_FOR")
  send_str(sock,str(my_uid))
  data=recvall(sock)
  changes=pickle.loads(data)
  for change in changes:
    if change["type"]=="break":
      x=change["x"]
      y=change["y"]
      tile=map.tileAt(x,y)
      name=tile.unlocalisedName
      if name=="grass":
        continue
      map.remove(tile)
      map.addTile("grass",x,y)
    if change["type"]=="place":
      x=change["x"]
      y=change["y"]
      block=change["block"]
      tile=map.tileAt(x,y)
      map.remove(tile)
      map.addTile(block,x,y)
    if change["type"]=="interact":
      x=change["x"]
      y=change["y"]
      block_data=change["block_data"]
      tile=map.tileAt(x,y)
      tile.loadData(block_data)
  for s in map.sprites():
    if s.mp_upd:
      data=s.interactData()
      send_str(sock,"INTERACT_BLOCK_AT")
      send_str(sock,str(my_uid))
      send_str(sock,str(math.floor(s.x)))
      send_str(sock,str(math.floor(s.y)))
      data_string=pickle.dumps(data)
      sock.send(data_string)
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
        coords=player.facingTile()
        if coords!=False:
          tile=map.tileAt(coords[0],coords[1])
          name=tile.unlocalisedName
          if name=="grass":
            to_place=player.inv.selected
            if to_place!="":
              send_str(sock,"PLACE_BLOCK_AT")
              send_str(sock,str(my_uid))
              send_str(sock,str(math.floor(coords[0])))
              send_str(sock,str(math.floor(coords[1])))
              send_str(sock,str(to_place))
              player.interact()
          else:
            player.interact()
            tile=map.tileAt(coords[0],coords[1])
            data=tile.interactData()
            if data!=None:
              send_str(sock,"INTERACT_BLOCK_AT")
              send_str(sock,str(my_uid))
              send_str(sock,str(math.floor(coords[0])))
              send_str(sock,str(math.floor(coords[1])))
              data_string=pickle.dumps(data)
              sock.send(data_string)
      if event.key==pygame.K_SLASH:
        player.attack()
        facing=player.facingTile()
        if facing!=False:
          x=facing[0]
          y=facing[1]
          send_str(sock,"BREAK_BLOCK_AT")
          send_str(sock,str(my_uid))
          send_str(sock,str(math.floor(x)))
          send_str(sock,str(math.floor(y)))
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
      elif event.key in key_to_dir.keys():
        move=True
        dir=key_to_dir[event.key]
    elif event.type==pygame.KEYUP:
      move=False
      player.frame=1
  if move:
    player.move(dir)
    send_str(sock,"SET_POS_FOR_UID")
    send_str(sock,str(my_uid))
    send_str(sock,str(math.floor(player.x/constants.TILESIZE)))
    send_str(sock,str(math.floor(player.y/constants.TILESIZE)))
    send_str(sock,player.dir)
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
    for uname,other in others.items():
      other.draw()
    pygame.display.flip()
    sleep(0.1)
send_str(sock,"CLOSE")
send_str(sock,UNAME)
sock.close()
