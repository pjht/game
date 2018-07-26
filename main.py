import pygame
import os
import random
import math
from time import sleep
player_frames={}
tiles={}
tmap=[]
inventory={}
selected=""
drops={
  "tree":(8,"wood"),
  "floor_vert":(1,"wood"),
  "floor_horiz":(1,"wood"),
  "cobblestone":(8,"cobblestone")
}
item_to_block={
  "wood":("floor_vert","floor_vert","floor_horiz","floor_horiz"),
  "cobblestone":("cobblestone","cobblestone","cobblestone","cobblestone")
}
solid=["bed_top","bed_bot","tree","cobblestone","door"]
player_info={"frame":1,"direction":"right","x":0,"y":0}
BACKGROUND="grass"
TILESIZE=16
MAPWIDTH=32
MAPHEIGHT=32
FONTSIZE=30
WINDWIDTH=MAPWIDTH*TILESIZE
WINDHEIGHT=(MAPHEIGHT+1)*TILESIZE
PLAYER_MOVE=TILESIZE
DELAY=0.1

class Animation:
  def __init__(self,frame_array,n_frames,name,screen):
   self.frame_array=frame_array
   self.x=0
   self.y=0
   self.screen=screen
   self.frame=0
   self.n_frames=n_frames
   self.name=name
  def draw(self):
    if self.frame+1>self.n_frames:
      self.frame=0
      return False
    img=self.frame_array[self.frame]
    self.screen.blit(tiles[BACKGROUND],(self.x*TILESIZE,self.y*TILESIZE))
    self.screen.blit(img,(self.x*TILESIZE,self.y*TILESIZE))
    pygame.display.flip()
    self.frame+=1
    return True


def load_player_frames():
  directions=["up","down","left","right"]
  num_frames=3
  for direction in directions:
    frame_array=[0,0,0]
    i=0
    while i<num_frames:
      img_name="{}_{}.png".format(direction,i)
      frame_array[i]=pygame.image.load(os.path.join("sprites","player",img_name))
      i+=1
    player_frames[direction]=frame_array

def load_anim(name,num_frames):
  frames=[]
  i=0
  while i<num_frames:
    img_name="{}.png".format(i)
    frames.append(pygame.image.load(os.path.join("animation",name,img_name)))
    i+=1
  anim=Animation(frames,num_frames,name,screen)
  return anim

def load_reverse_anim(name,num_frames):
  frames=[]
  i=num_frames-1
  while i>=0:
    img_name="{}.png".format(i)
    frames.append(pygame.image.load(os.path.join("animation",name,img_name)))
    i-=1
  anim=Animation(frames,num_frames,name,screen)
  return anim

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
        num=random.randint(0,101)
        if num<50:
          tmap[y].append(TREE)
        else:
          tmap[y].append(COBBLESTONE)
      else:
        tmap[y].append(GRASS)
      x+=1
    y+=1
  tmap[4][3]=DOOR
def refresh_screen():
  y=0
  while y<MAPHEIGHT:
    x=0
    while x<MAPWIDTH:
      for anim in anims:
        if anim.x==x and anim.y==y:
          x+=1
          continue
      screen.blit(tiles[BACKGROUND],(x*TILESIZE,y*TILESIZE))
      x+=1
    y+=1
  y=0
  while y<MAPHEIGHT:
    x=0
    while x<MAPWIDTH:
      for anim in anims:
        if anim.x==x and anim.y==y:
          x+=1
          continue
      screen.blit(tiles[tmap[y][x]],(x*TILESIZE,y*TILESIZE))
      x+=1
    y+=1
  dir=player_info["direction"]
  frame=player_info["frame"]
  x=player_info["x"]
  y=player_info["y"]
  player_img=player_frames[dir][frame]
  screen.blit(player_img,(x,y))
  if selected!="":
    texture=item_to_block[selected][0]
    screen.blit(tiles[texture],(0*TILESIZE,32*TILESIZE))
  pygame.display.flip()

def get_facing_tile():
  x=math.floor(player_info["x"]/TILESIZE)
  y=math.floor(player_info["y"]/TILESIZE)
  dir=player_info["direction"]
  if dir=="up":
    y-=1
  elif dir=="down":
    y+=1
  elif dir=="left":
    x-=1
  elif dir=="right":
    x+=1
  if x>MAPWIDTH-1:
    return False
  if x<0:
    return False
  if y>MAPHEIGHT-1:
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
      global selected
      selected=name

def break_block():
  coords=get_facing_tile()
  if coords==False:
    return
  x=coords[0]
  y=coords[1]
  tile=tmap[y][x]
  handle_break(tile)
  tmap[y][x]=BACKGROUND

def place_block():
  global selected
  if selected:
    if not selected in inventory.keys():
      return
    coords=get_facing_tile()
    if coords==False:
      return
    x=coords[0]
    y=coords[1]
    tile=tmap[y][x]
    if tile in item_to_block[selected]:
      return
    if not tile==BACKGROUND:
      return
    count=inventory[selected]
    count=count-1
    inventory[selected]=count
    if count==0:
      del inventory[selected]
    to=item_to_block[selected]
    if player_info["direction"]=="up":
      tmap[y][x]=to[0]
    elif player_info["direction"]=="down":
      tmap[y][x]=to[1]
    elif player_info["direction"]=="left":
      tmap[y][x]=to[2]
    elif player_info["direction"]=="right":
      tmap[y][x]=to[3]
    if count==0:
      selected=""

def select_next():
  global selected
  newsel=""
  ok_next=False
  for item, count in inventory.items():
    if ok_next:
      newsel=item
      break
    if item==selected:
      ok_next=True
  if newsel!="":
    selected=newsel

def select_prev():
  global selected
  newsel=""
  for item, count in inventory.items():
    if item==selected:
      break
    newsel=item
  if newsel!="":
    selected=newsel

def interact():
  coords=get_facing_tile()
  if coords==False:
    return
  x=coords[0]
  y=coords[1]
  tile=tmap[y][x]
  if tile==BACKGROUND:
    place_block()
  elif tile==DOOR:
    anim=load_anim("door",4)
    anim.name="door_open"
    anim.x=x
    anim.y=y
    anims.append(anim)
  elif tile==DOOR_OPEN:
    anim=load_reverse_anim("door",4)
    anim.name="door_close"
    anim.x=x
    anim.y=y
    anims.append(anim)
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
  elif key==pygame.K_PERIOD:
    interact()
  elif key==pygame.K_n:
    select_next()
  elif key==pygame.K_p:
    select_prev()
  elif key==pygame.K_e:
    inv=not inv
    if inv:
      move=False
    else:
      screen.fill([0,0,0])
      refresh_screen()
  elif key in move_keys:
    move=True
    move_key=key

def show_inv():
  global inv
  screen.fill([255,255,255])
  text=[]
  label=[]
  for item, count in inventory.items():
    text.append("{} {}".format(count,item))
  for line in text:
    label.append(helvetica_neue.render(line, True, (0,0,0)))
  for line in range(len(label)):
    screen.blit(label[line],(1,(line*FONTSIZE)+(2*line)))
  pygame.display.flip()

def main():
  pygame.init()
  pygame.display.set_caption("game")
  global screen
  screen=pygame.display.set_mode((WINDWIDTH,WINDHEIGHT))
  global helvetica_neue
  helvetica_neue=pygame.font.SysFont('Helvetica Neue', FONTSIZE)
  running=True
  load_player_frames()
  global anims
  anims=[]
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
      i=0
      for anim in anims:
        keep=anim.draw()
        if not keep:
          if anim.name=="door_open":
            x=anim.x
            y=anim.y
            tmap[y][x]=DOOR_OPEN
            screen.blit(tiles[tmap[y][x]],(x*TILESIZE,y*TILESIZE))
            pygame.display.flip()
          if anim.name=="door_close":
            x=anim.x
            y=anim.y
            tmap[y][x]=DOOR
            screen.blit(tiles[tmap[y][x]],(x*TILESIZE,y*TILESIZE))
            pygame.display.flip()
          del anims[i]
        i+=1
      refresh_screen()
      sleep(DELAY)
main()
