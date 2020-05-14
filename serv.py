import pygame
import sys
def my_load(path):
  return None
mod=sys.modules["pygame.image"]
mod.load=my_load
sys.modules["pygame.image"]=mod
import os
import random
import select
import socket
import _thread
import pickle
import signal
import glob
import os.path
import lib.constants as constants
from lib.gameregistry import GameRegistry
from lib.map import Map
from lib.character import Character
from lib.block import Block
from lib.player import Player
from time import sleep
import blocks
import pprint
player_map={}
pos_map={}
map_changes={}
next_x=0

def recv_str(sock):
  str=""
  ch=""
  while True:
    ch=sock.recv(1).decode("utf-8")
    if ch=="\n":
      break
    str+=ch
  # print("Got string: "+str)
  return str

def send_str(sock,str,print_str=True):
  if print_str:
    pass
    # print("Sending string: "+str)
  sock.send((str+"\n").encode("utf-8"))

def send_hash(sock,hash):
  # print("Sending hash: "+pp.pformat(hash))
  send_str(sock,str(len(hash)),False)
  for key,val in hash.items():
    send_str(sock,str(key),False)
    send_str(sock,str(val),False)

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
  
def on_new_client(sock):
    global player_map
    global pos_map
    global map
    global map_changes
    global next_x
    username=recv_str(sock)
    player_map[username]=sock
    pos_map[username]=(next_x,0,"down")
    map_changes[username]=[]
    next_x+=1
    while True:
      msg=recv_str(sock)
      if msg=="CLOSE":
        del player_map[username]
        del pos_map[username]
        del map_changes[username]
      elif msg=="GET_POS_MAP":
        send_hash(sock,pos_map)
      elif msg=="GET_POS":
        send_str(sock,str(pos_map[username][0]))
        send_str(sock,str(pos_map[username][1]))
        send_str(sock,pos_map[username][2])
      elif msg=="SET_POS":
        pos_map[username]=(int(recv_str(sock)),int(recv_str(sock)),recv_str(sock))
      elif msg=="BLOCK_AT_POS":
        x=int(recv_str(sock))
        y=int(recv_str(sock))
        sock.send(pickle.dumps(map.tileAt(x,y)))
def handle_cmds():
  while True:
    if select.select([sys.stdin],[],[],0.0)[0]:
      cmd=input()
      cmd=cmd.split()
      if len(cmd)>0:
        if cmd[0]=="stop":
          s.close()
          f=open("worlds/map_{}.pkl".format(map_name),"wb")
          pickle.dump(map,f)
          f.close()
          exit(1)

def exit_cleanup(signal,frame):
  s.close()
  f=open("worlds/map_{}.pkl".format(map_name),"wb")
  pickle.dump(map,f)
  f.close()
  
Block.init()
files=glob.glob("worlds/map_*.pkl")
if len(files)==0:
  new="y"
else:
  new=input("New world?").lower()
if new=="n" or new=="no":
  i=1
  map_map=[]
  for name in files:
    name=name.split("_")
    name.pop(0)
    name="_".join(name)
    name,_=os.path.splitext(name)
    print("{}. {}".format(i,name))
    map_map.append(name)
    i+=1
  map_name=map_map[int(input("Which world?"))-1]
  f=open("worlds/map_{}.pkl".format(map_name),"rb")
  map=pickle.load(f)
  f.close()
else:
  map_name=input("World name:")
  map=Map(None)

s=socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host="localhost"
port=30000
s.bind((host, port))
s.listen(5)
_thread.start_new_thread(handle_cmds,())
signal.signal(signal.SIGINT, exit_cleanup)
while True:
   c,addr=s.accept()
   _thread.start_new_thread(on_new_client,(c,))
