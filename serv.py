import pygame
import os
import random
import recipes
import sys
import select
import blocks
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
from player import *
from time import sleep
uid_map={}
pos_map={}
map_changes={}
next_uid=0

def recv_str(sock):
  str=""
  ch=""
  while True:
    ch=sock.recv(1).decode("utf-8")
    if ch=="\n":
      break
    str+=ch
  return str

def send_str(sock,str):
  sock.send((str+"\n").encode("utf-8"))

def send_hash(sock,hash):
  send_str(sock,str(len(hash)))
  for key,val in hash.items():
    send_str(sock,str(key))
    send_str(sock,str(val))

def recvall(sock):
  BUFF_SIZE=4096
  data=b''
  while True:
    part=sock.recv(BUFF_SIZE)
    data+=part
    if len(part)<BUFF_SIZE:
      break
  return data

def on_new_client(sock):
    global uid_map
    global next_uid
    global pos_map
    global map
    while True:
        msg=recv_str(sock)
        if msg=="CLOSE":
          uname=recv_str(sock)
          uid=uid_map[uname]
          del uid_map[uname]
          del pos_map[uid]
          del map_changes[uid]
        elif msg=="ADD_USR":
          uname=recv_str(sock)
          uid_map[uname]=next_uid
          resp=str(next_uid)
          send_str(sock,resp)
          pos_map[next_uid]=(next_uid,0,"down")
          map_changes[next_uid]=[]
          next_uid+=1
        elif msg=="GET_UID_MAP":
          send_hash(sock,uid_map)
        elif msg=="GET_MAP":
          data_string=pickle.dumps(map)
          sock.send(data_string)
        elif msg=="GET_POS_FOR_UID":
          uid=recv_str(sock)
          if not int(uid) in uid_map.values():
            print("Invalid UID {}".format(uid))
            sock.close()
            return
          pos=pos_map[int(uid)]
          send_str(sock,str(pos[0]))
          send_str(sock,str(pos[1]))
          send_str(sock,pos[2])
        elif msg=="SET_POS_FOR_UID":
          uid=int(recv_str(sock))
          if not int(uid) in uid_map.values():
            print("Invalid UID {}".format(uid))
            sock.close()
            return
          x=int(recv_str(sock))
          y=int(recv_str(sock))
          fac=recv_str(sock)
          pos_map[uid]=(x,y,fac)
        elif msg=="BREAK_BLOCK_AT":
          ch_uid=int(recv_str(sock))
          if not int(ch_uid) in uid_map.values():
            print("Invalid UID {}".format(uid))
            sock.close()
            return
          x=int(recv_str(sock))
          y=int(recv_str(sock))
          for uid,changes in map_changes.copy().items():
            if ch_uid!=uid:
              map_changes[uid].append({"type":"break","x":x,"y":y})
          tile=map.tileAt(x,y)
          name=tile.unlocalisedName
          if name=="grass":
            continue
          map.remove(tile)
          map.addTile("grass",x,y)
        elif msg=="PLACE_BLOCK_AT":
          ch_uid=int(recv_str(sock))
          if not int(ch_uid) in uid_map.values():
            print("Invalid UID {}".format(uid))
            sock.close()
            return
          x=int(recv_str(sock))
          y=int(recv_str(sock))
          block=recv_str(sock)
          for uid,changes in map_changes.copy().items():
            if ch_uid!=uid:
              map_changes[uid].append({"type":"place","x":x,"y":y,"block":block})
          tile=map.tileAt(x,y)
          map.remove(tile)
          map.addTile(block,x,y)
        elif msg=="INTERACT_BLOCK_AT":
          ch_uid=int(recv_str(sock))
          if not int(ch_uid) in uid_map.values():
            print("Invalid UID {}".format(uid))
            sock.close()
            return
          x=int(recv_str(sock))
          y=int(recv_str(sock))
          data=recvall(sock)
          block_data=pickle.loads(data)
          for uid,changes in map_changes.copy().items():
            if ch_uid!=uid:
              map_changes[uid].append({"type":"interact","x":x,"y":y,"block_data":block_data})
        elif msg=="GET_CHANGES_FOR":
          uid=int(recv_str(sock))
          if not int(uid) in uid_map.values():
            print("Invalid UID {}".format(uid))
            sock.close()
            return
          changes=map_changes[uid]
          data_string=pickle.dumps(changes)
          sock.send(data_string)
          map_changes[uid]=[]
    clientsocket.close()

def handle_cmds():
  while True:
    if select.select([sys.stdin],[],[],0.0)[0]:
      cmd=input()
      cmd=cmd.split()
      if len(cmd)>0:
        if cmd[0]=="stop":
          s.close()
          f=open("map_{}.pkl".format(map_name),"wb")
          pickle.dump(map,f)
          f.close()
          exit(1)

def exit_cleanup(signal,frame):
  s.close()
  f=open("map_{}.pkl".format(map_name),"wb")
  pickle.dump(map,f)
  f.close()

Block.init()
files=glob.glob("map_*.pkl")
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
  f=open("map_{}.pkl".format(map_name),"rb")
  map=pickle.load(f)
  f.close()
else:
  map_name=input("World name:")
  map=Map(None)

s=socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host="localhost"
port=2000
s.bind((host, port))
s.listen(5)
_thread.start_new_thread(handle_cmds,())
signal.signal(signal.SIGINT, exit_cleanup)
while True:
   c,addr=s.accept()
   _thread.start_new_thread(on_new_client,(c,))