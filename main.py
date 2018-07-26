import pygame
import os
import random
import math
from time import sleep
frames={}
tiles={}
tmap=[]
inventory={}
drops={"tree":(8,"wood")}
solid=["bed_top","bed_bot","tree"]
player_info={"frame":1,"direction":"right","x":0,"y":0}
BACKGROUND="grass"
TILESIZE=16
MAPWIDTH=32
MAPHEIGHT=32
WINDWIDTH=MAPWIDTH*TILESIZE
WINDHEIGHT=MAPHEIGHT*TILESIZE
PLAYER_MOVE=TILESIZE
DELAY=0.08
def load_frames():
  directions=["up","down","left","right"]
  num_frames=3
  for direction in directions:
    frame_array=[0,0,0]
    i=0
    while i<num_frames:
      img_name="{}_{}.png".format(direction,i)
      frame_array[i]=pygame.image.load(os.path.join("sprites","player",img_name))
      i+=1
    frames[direction]=frame_array

def load_tiles():
  directory=os.fsencode("tiles")
  for file in os.listdir(directory):
    filename=os.fsdecode(file)
    if filename.endswith(".jpeg"):
      name=os.path.splitext(filename)[0]
      glob=globals()
      glob[name.upper()]=name
      tiles[name]=pygame.image.load(os.path.join("tiles", filename))

def generate_world():
  global tmap
  tmap=[]
  y=0
  while y<MAPHEIGHT:
    x=0
    tmap.append([])
    while x<MAPWIDTH:
      num=random.randint(0,101)
      if num<5:
        tmap[y].append(TREE)
      else:
        tmap[y].append(GRASS)
      x+=1
    y+=1
def refresh_screen():
  y=0
  while y<MAPHEIGHT:
    x=0
    while x<MAPWIDTH:
      screen.blit(tiles[BACKGROUND],(x*TILESIZE,y*TILESIZE))
      x+=1
    y+=1
  y=0
  while y<MAPHEIGHT:
    x=0
    while x<MAPWIDTH:
      screen.blit(tiles[tmap[y][x]],(x*TILESIZE,y*TILESIZE))
      x+=1
    y+=1
  dir=player_info["direction"]
  frame=player_info["frame"]
  x=player_info["x"]
  y=player_info["y"]
  player_img=frames[dir][frame]
  screen.blit(player_img,(x,y))
  pygame.display.flip()

def get_facing_tile():
  x=math.floor(player_info["x"]/16)
  y=math.floor(player_info["y"]/16)
  dir=player_info["direction"]
  if dir=="up":
    y-=1
  elif dir=="down":
    y+=1
  elif dir=="left":
    x-=1
  elif dir=="right":
    x+=1
  if x>31:
    return False
  if x<0:
    return False
  if y>31:
    return False
  if y<0:
    return False
  return (x,y)

def handle_break(tile):
    if tile in drops.keys():
      count=drops[tile][0]
      name=drops[tile][1]
      if name in inventory.keys():
        numb=inventory[name]
        inventory[name]=numb+count
      else:
        inventory[name]=count

def break_block():
  coords=get_facing_tile()
  if coords==False:
    return
  x=coords[0]
  y=coords[1]
  tile=tmap[y][x]
  handle_break(tile)
  tmap[y][x]=BACKGROUND

def hande_key(key):
  global inventory
  global inv
  global move
  global move_key
  move_keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]
  if key==pygame.K_SPACE:
    inventory={}
    generate_world()
    refresh_screen()
  elif key==pygame.K_SLASH:
    break_block()
  elif key==pygame.K_e:
    inv=not inv
    if inv:
      move=False
  elif key in move_keys:
    move=True
    move_key=key

def show_inv():
  global inv
  screen.fill([255,255,255])
  string=""
  print(string)
  for item, count in inventory.items():
    string+="{} {}\n".format(count,item)
  text=helvetica_neue.render(string, False, (0, 0, 0))
  screen.blit(text,(0,0))
  pygame.display.flip()
def main():
  pygame.init()
  pygame.display.set_caption("game")
  global screen
  screen=pygame.display.set_mode((WINDWIDTH,WINDHEIGHT))
  global helvetica_neue
  helvetica_neue=pygame.font.SysFont('Helvetica Neue', 30)
  running=True
  load_frames()
  load_tiles()
  generate_world()
  refresh_screen()
  global move
  global inv
  global move_key
  move=False
  inv=False
  move_key=0
  while running:
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        running=False
      elif event.type==pygame.KEYDOWN:
        hande_key(event.key)
      elif event.type==pygame.KEYUP:
        move=False
        player_info["frame"]=1
      if inv:
        show_inv()
    if move:
      old_x=player_info["x"]
      old_y=player_info["y"]
      if move_key==pygame.K_UP:
        player_info["direction"]="up"
        player_info["y"]-=PLAYER_MOVE
      elif move_key==pygame.K_DOWN:
        player_info["direction"]="down"
        player_info["y"]+=PLAYER_MOVE
      elif move_key==pygame.K_LEFT:
        player_info["direction"]="left"
        player_info["x"]-=PLAYER_MOVE
      elif move_key==pygame.K_RIGHT:
        player_info["direction"]="right"
        player_info["x"]+=PLAYER_MOVE
      player_info["frame"]+=1
      if player_info["frame"]>2:
        player_info["frame"]=0
      if player_info["x"]>=WINDWIDTH:
        player_info["x"]=old_x
      if player_info["x"]<0:
        player_info["x"]=old_x
      if player_info["y"]>=WINDHEIGHT:
        player_info["y"]=old_y
      if player_info["y"]<0:
        player_info["y"]=old_y
      tile=tmap[math.floor(player_info["y"]/TILESIZE)][math.floor(player_info["x"]/TILESIZE)]
      if tile in solid:
        player_info["x"]=old_x
        player_info["y"]=old_y
    if not inv:
      refresh_screen()
      sleep(DELAY)
main()
