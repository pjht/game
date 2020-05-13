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


pygame.init()
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

map=Map(screen,None,0)
map.tiles={}
player=Player(0,0,map,screen,"PJHT","player_local")
player.direction="up"

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
  screen.fill([0,0,0])
  map.draw(player.x,player.y)
  player.draw()
  pygame.display.flip()
  sleep(0.1)
