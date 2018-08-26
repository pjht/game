import pygame
import os
import random
import recipes
import sys
import select
import blocks
import socket
import pickle
import lib.constants as constants
from lib.gameregistry import GameRegistry
from lib.map import Map
from lib.character import Character
from lib.block import Block
from player import *
from time import sleep

def recv_str(sock,print_str=True):
  str=""
  ch=""
  while True:
    ch=sock.recv(1).decode("utf-8")
    if ch=="\n":
      break
    str+=ch
  if print_str:
    print(str)
  return str

def send_str(sock,str):
  print(str)
  sock.send((str+"\n").encode("utf-8"))

def recv_hash(sock):
  hash={}
  len=int(recv_str(sock,False))
  for _ in range(len):
    key=recv_str(sock,False)
    val=recv_str(sock,False)
    hash[key]=val
  print(hash)
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
sleep(0.5)
# The server's generated map does not have a screen. We fix that here.
map.screen=screen
for s in map.sprites():
  s.screen=screen
send_str(sock,"GET_POS_FOR_UID")
send_str(sock,str(my_uid))
x=int(recv_str(sock))*constants.TILESIZE
y=int(recv_str(sock))*constants.TILESIZE
player=Player(x,y,map,screen,UNAME,"player")
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
      print("Getting {}'s position".format(uname))
      send_str(sock,"GET_POS_FOR_UID")
      send_str(sock,uid)
      x=int(recv_str(sock))*constants.TILESIZE
      y=int(recv_str(sock))*constants.TILESIZE
      if uname in others:
        others[uname].x=x
        others[uname].y=y
      else:
        others[uname]=Player(x,y,map,screen,uname,"slime")
      connected.append(uname)
  # Remove all disconnected players
  others_copy=others.copy()
  for uname,uid in others_copy.items():
    if not uname in connected:
      del others[uname]
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      running=False
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
    for uname,other in others.items():
      other.draw()
    pygame.display.flip()
    sleep(0.5)
send_str(sock,"CLOSE")
send_str(sock,UNAME)
sock.close()
