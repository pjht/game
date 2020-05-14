import pygame
import os
import random
import sys
import select
import socket
import pickle
import lib.constants as constants
from lib.gameregistry import GameRegistry
from lib.map import Map
from lib.character import Character
from lib.block import Block
from lib.player import Player
from lib.player_img import PlayerImg
from time import sleep
import pprint
import blocks

pp=pprint.PrettyPrinter(indent=2)

def recv_str(sock,print_str=True):
  str=""
  ch=""
  while True:
    ch=sock.recv(1).decode("utf-8")
    if ch=="\n":
      break
    str+=ch
  if print_str:
    pass
    # print("Got string: "+str)
  return str

def send_str(sock,str):
  # print("Sending string: "+str)
  sock.send((str+"\n").encode("utf-8"))

def recv_hash(sock):
  hash={}
  len=int(recv_str(sock,False))
  for _ in range(len):
    key=recv_str(sock,False)
    val=recv_str(sock,False)
    hash[key]=val
  # print("Got hash: "+pp.pformat(hash))
  return hash

def recvall(sock):
  BUFF_SIZE=4096
  data=b''
  while True:
    part=sock.recv(BUFF_SIZE)
    data+=part
    if len(part)<BUFF_SIZE:
      break
  # print("Got data: "+pp.pformat(pickle.loads(data)))
  return data


UNAME=input("UNAME:")
pygame.init()
pygame.display.set_caption(UNAME)
screen=pygame.display.set_mode((constants.WINDWIDTH,constants.WINDHEIGHT))

running=True
move=False
direction=None
key_to_dir={
  pygame.K_UP:"up",
  pygame.K_DOWN:"down",
  pygame.K_LEFT:"left",
  pygame.K_RIGHT:"right"
}

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost",30000))
send_str(sock,UNAME)
send_str(sock,"GET_POS")
x=int(recv_str(sock))
y=int(recv_str(sock))
fac=recv_str(sock)
map=Map(screen,sock)
map.tiles={}
player=Player(x,y,map,screen,"PJHT","player_local")
player.direction=fac


while running:
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      running=False
    if event.type==pygame.KEYDOWN:
      if event.key in key_to_dir.keys():
        move=True
        direction=key_to_dir[event.key]
    elif event.type==pygame.KEYUP:
      move=False
      player.frame=1
      key_states = pygame.key.get_pressed()
      if key_states[pygame.K_UP]==1:
        move=True
        direction="up"
      elif key_states[pygame.K_DOWN]==1:
        move=True
        direction="down"
      elif key_states[pygame.K_LEFT]==1:
        move=True
        direction="left"
      elif key_states[pygame.K_RIGHT]==1:
        move=True
        direction="right"
  if move:
    player.move(direction)
  send_str(sock,"SET_POS")
  send_str(sock,str(player.x))
  send_str(sock,str(player.y))
  send_str(sock,player.direction)
  screen.fill([0,0,0])
  map.draw(player.x,player.y)
  player.draw()
  send_str(sock,"GET_POS_MAP")
  pos_map=recv_hash(sock)
  print(pos_map)
  for uname,pos in pos_map.items():
    if uname==UNAME:
      continue
    pos=eval(pos) # FIXME: Eval is dangerous
    char=PlayerImg(screen,"player")
    char.direction=pos[2]
    offsetx=pos[0]-player.x
    offsety=pos[1]-player.y
    char.draw(constants.CENTERX+offsetx,constants.CENTERY+offsety)
  pygame.display.flip()
  sleep(0.1)
  
send_str(sock,"CLOSE")
sock.close()
