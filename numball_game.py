from bprg import *
from numball_seed import *

g=[(49,49,200),(49,49,49)]
g2=[(255,255,255),(255,255,255)]
c,bg=g2[0],g[0]
c_ball=(255,0,0)
c_ball2=fade(1.4,2,c_ball,(255,255,255))
terrain=[]

##### SEEDER #####
def seed(octets):
  global level,gamemode
  char,level="0123456789abcdef","f"*10
  for i in range(octets):level+=choice(char)
  level+="f"*40
  
##### UNPACK #####
conv={"0":"0"*4,"1":"0001","2":"0010","3":"0011","4":"0100","5":"0101","6":"0110","7":"0111","8":"1000","9":"1001","a":"1010","b":"1011","c":"1100","d":"1101","e":"1110","f":"1"*4}
def RENDER(past,u):
  return level[past*2:][:u*2]
def CTRL(f,s=""):
  for rang in f:s+=conv[rang]
  return s
def unpack():
  global terrain,gamemode
  lv_segment=RENDER(past,24)
  terrain=[]
  for l in range(len(lv_segment)//2):
    n=lv_segment[l*2:][:2]
    terrain.append(CTRL(n))

##### MENU #####
modes=["NORMAL","HARDCORE"]
def MENU():
  global chx,octets,levels,level,idx,modes,gamemode,mdx,g,g2,bg,c
  c,bg=g2[0],g[0]
  background(bg)
  if levels:
    draw(" NEW SEED ",55,102,bg,c),draw(" READ SEED ",165,102,bg,c)
    for i in range(10):rect(45+i,111-i,1,i*2,c),rect(284-i,111-i,1,i*2,c)
    while not key(0) and not key(3):""
  else:
    draw(" NEW SEED ",110,102,bg,c)
    for i in range(10):rect(100+i,111-i,1,i*2,c),rect(219-i,111-i,1,i*2,c)
    wait(4)
  chx=0 if key(0) or not levels else 1
  release(0),release(3),release(4),background(bg)
  if not chx:
    rect(100,102,130,18,c)
    draw(" SIZE: ",100,102,bg,c),draw(str(octets),180,102,bg,c)
    for i in range(10):rect(90+i,111-i,1,i*2,c),rect(239-i,111-i,1,i*2,c)
    while not key(4):
      octets=passlimits(octets+(key(3)-key(0))*2+(key(1)-key(2))*50,1,4000)
      for k in (0,1,2,3):
        if key(k):
          rect(170,102,50,18,c),draw(str(octets),195-5*len(str(octets)),102,bg,c),sleep(0.1)
  elif chx:
    rect(95,102,135,18,c),draw(" INDEX: ",95,102,bg,c),draw(str(levels[idx][:5]),195-5*len(str(levels[idx][:5])),102,bg,c)
    for i in range(10):rect(85+i,111-i,1,i*2,c),rect(239-i,111-i,1,i*2,c)
    while not key(4):
      idx=passlimits(idx+key(3)-key(0),0,len(levels)-1)
      for k in (0,3):
        if key(k):rect(170,102,50,18,c),draw(str(levels[idx][:5]),195-5*len(str(levels[idx][:5])),102,bg,c),sleep(0.2)
    level=levels[idx][6:]
  release(4),background(bg),rect(55,102,210,18,c),draw(" GAMEMODE : ",55,102,bg,c),draw(str(modes[mdx]),210-5*len(str(modes[mdx])),102,bg,c)
  for i in range(10):rect(45+i,111-i,1,i*2,c),rect(274-i,111-i,1,i*2,c)
  while not key(4):
    mdx=passlimits(mdx+(key(3)-key(0)),0,len(modes)-1)
    for k in (0,3):
      if key(k):rect(165,102,100,18,c),draw(str(modes[mdx]),210-5*len(str(modes[mdx])),102,bg,c),sleep(0.2)
  gamemode=modes[mdx]
  release(4),background(bg),draw(" PRESS OK TO START ",65,102,bg,c)
  for i in range(10):rect(55+i,111-i,1,i*2,c),rect(264-i,111-i,1,i*2,c)
  if chx==0:
    draw("please wait...",2,202,c,bg)
    seed(octets)
    rect(2,202,140,18,bg)
  if octets<=1000 and not chx:
    for i in range(0,len(level)/150,1):print(("'{}.".format(hex(randint(69905,1048575))[2:]) if i==0 else "")+level[i*150:][:150]+("',\n" if i>=len(level)/150-1 else ""))
  stopall(4)
  bg,c=g[0] if gamemode=="NORMAL" else g[1],g2[0] if gamemode=="NORMAL" else g2[1]

##### 3D TERRAIN #####    
def DRAW_TERRAIN():
  global past,terrain,ball,steps,chrono,mn,deaths
  unpack()
  centre_x=160+(160-ball[0])//6
  for step in range(steps):
    offset=step/steps 
    for i in range(len(terrain)):
      position_virtuelle,tronc=i-offset,"0"*3+terrain[i]+"0"*3
      if position_virtuelle<0:continue
      echelle=1.0/(1.0+position_virtuelle*0.3)
      largeur_case,hauteur_tranche,y_ecran=int(52*echelle),int(11*echelle),int(85+130*echelle)
      largeur_totale=largeur_case*14
      x=centre_x-(largeur_totale//2)
      for rang in tronc:
        rect(x,y_ecran,largeur_case,hauteur_tranche,c if rang=="1" else bg)
        x+=largeur_case
    aff()
    if fall():break
    if key(17):
      mn=monotonic()
      draw(" paused ",120,0,bg,c)
      stopall(17)
      chrono+=monotonic()-mn
      rect(120,0,80,18,bg),icons()
  past+=1
  rect(0,0,120,18,bg)

##### THINGS ON SCREEN #####
def aff():
  global past,level,pourcent
  player()
  pourcent=int((past/((len(level)-40)//2))*100)
  draw(str(pourcent)+"%",23-5*len(str(pourcent)),0,c,bg)
  sleep(0.002)

##### IMAGES #####
img=["011111011111111011101111011101111100101010","011011011111111111111011111000111000001000","111011101000100011100001010001000101110111"]

def IMG(N,x,y,lx,c):
  for i in range(len(str(img[N]))):
    if int(img[N][i]):set(x+i%lx,y+i//lx,c)
def icons():
  if gamemode=="HARDCORE":IMG(0,157,2,7,c_ball)

##### IF FALL #####
def fall():
  global ball,jump,past,level,steps,imunimate,deaths,gamemode,ad_falled
  if get(ball[0],ball[1]+1)!=c and ball[1]==y0 and not imunimate and past>=1:
    if gamemode!="HARDCORE":
      circle(ball[0],ball[1]-12,12,c_ball2)
      past,ball[1]=limits(past-35,0,len(level)//2),y0
      ball[1],imunimate,deaths=y0,monotonic()+1.5,deaths+1
      rect(0,0,320,40,bg),icons()
    if gamemode=="HARDCORE":
      GAMEOVER()
    return True
  else:return False

##### STOP #####
def GAMEOVER():
  global tm,pourcent,chrono
  tm=round(monotonic()-chrono,3)
  tm="{} min {}s".format(int(tm//60),round(tm%60,3))
  background(bg),sleep(0.03),rect(0,80,320,62,c),draw("YOU DIED",120,82,bg,c),draw(str(pourcent)+"%",155-5*len(str(pourcent)),102,bg,c),draw(tm,160-5*len(tm),122,bg,c)
  sleep(0.2),stopall(4)
  __init__()

##### IF WIN ####
def WIN():
  global pourcent,tm,chrono,deaths
  if pourcent>=100:
    tm=round(monotonic()-chrono,3)
    tm="virtual time: {} min {}s".format(int(tm//60),round(tm%60,3))
    print(tm)
    background(bg)
    rect(0,80,320,62,c)
    if gamemode=="NORMAL":draw("YOU WIN",125,82,bg,c),draw(tm,160-5*len(tm),102,bg,c),draw("deaths: "+str(deaths),120-5*len(str(deaths)),122,bg,c)
    if gamemode=="HARDCORE":draw("YOU WIN",125,82,c_ball,c),draw(str(pourcent)+"%",155-5*len(str(pourcent)),102,bg,c),draw(tm,160-5*len(tm),122,bg,c)
    sleep(0.2),stopall(4)
    __init__()
    
##### DRAW PLAYER #####
def player():
  global a,b,ball,jump,imunimate,steps
  circle(ball[0],ball[1]-12,12,bg)
  a+=0.3 if jump else 0
  if ball[1]>=y0 and get(ball[0],ball[1]+1)!=bg:jump=False
  if key(4) and not jump:jump,a=True,-4
  b=limits(b+(key(3)-key(0))+(0.4 if b<0 else -0.4 if b>0 else 0),-4,4)
  ball[0],ball[1]=limits(ball[0]+int(b),26,320-26),limits(ball[1]+int(a),0,y0)
  circle(ball[0],ball[1]-12,12,c_ball2 if imunimate else c_ball)

def __init__():
  global pourcent,imunimate,steps,past,a,b,jump,m,mn,deaths,chrono,octets,chx,idx,mdx,level,gamemode,ball
  pourcent,imunimate,steps,past,a,b,jump,m,mn,deaths=0,0,14,0,0,0,False,0,0,0
  terrain=[]
  ball=[160,y0]
  MENU(),background(bg),icons()
  chrono=monotonic()

y0,pourcent,imunimate,steps,past,a,b,jump,m,mn,deaths=190,0,0,14,0,0,0,False,0,0,0
ball=[160,y0]
terrain=[]
octets,chx,idx,mdx=300,0,0,0
level=gamemode=""

MENU(),background(bg),icons()

chrono=monotonic()

while True:
  DRAW_TERRAIN()
  WIN()
  chrono-=0.012
  steps=limits(steps+(key(2)*2-(key(1)*steps/10))*3,4,30)
  if monotonic()>imunimate:imunimate=0
  else:steps=14
  if key(23):__init__()
