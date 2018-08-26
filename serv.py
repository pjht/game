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
import lib.constants as constants
from lib.gameregistry import GameRegistry
from lib.map import Map
from lib.character import Character
from lib.block import Block
from player import *
from time import sleep
uid_map={}
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

def on_new_client(sock):
    global uid_map
    global next_uid
    while True:
        msg=recv_str(sock)
        if msg=="CLOSE":
          uname=recv_str(sock)
          del uid_map[uname]
        elif msg=="ADD_USR":
          uname=recv_str(sock)
          uid_map[uname]=next_uid
          resp=str(next_uid)
          send_str(sock,resp)
          next_uid+=1
        elif msg=="GET_UID_MAP":
          send_hash(sock,uid_map)
        elif msg=="GET_MAP":
          data_string=pickle.dumps(map)
          sock.send(data_string)
        elif msg=="GET_POS_FOR_UID":
          uid=recv_str(sock)
          send_str(sock,uid)
          send_str(sock,"0")
    clientsocket.close()

map=Map(None)
global s
s=socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host="localhost"
port=2000
s.bind((host, port))
s.listen(5)
while True:
   c,addr=s.accept()
   _thread.start_new_thread(on_new_client,(c,))
s.close()
