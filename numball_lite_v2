from math import *
from random import *
from kandinsky import fill_rect as rect, draw_string as draw, get_pixel as get, set_pixel as set
from ion import keydown as key
from time import *
def background(bg):rect(0,0,320,222,bg)
def circle(cx,cy,r,color):
  for y in range(-r,r+1):
    dx=int((r*r-y*y)**0.5)
    rect(cx-dx,cy+y,2*dx,1,color)
def fadetime(*colors):
  step,segments=abs(sin(monotonic())),1
  n=len(colors)-1
  if n==0:return colors[0]
  i=min(int((step/segments)*n),n-1)
  return tuple(int(a+(b-a)*(((step/segments)*n)-i)) for a,b in zip(colors[i],colors[i+1]))
def release(k):
  while key(k):pass
def wait(k):
  while not key(k):""
def stopall(k):release(k),wait(k),release(k)
def limits(nb,mi,ma):return min(max(nb,mi),ma)




conv={"A":"0"*4,"B":"0001","C":"0010","D":"0011","E":"0100","F":"0101","G":"0110","H":"0111","I":"1000","J":"1001","K":"1010","L":"1011","M":"1100","N":"1101","O":"1110","P":"1"*4}

def RENDER(past,u):
  return level[past*2:][:u*2]
def CTRL(f,s=""):
  for rang in f:s+=conv[rang]
  return s
def unpack():
  global terrain
  lv_segment=RENDER(past,21)
  terrain=[]
  for l in range(len(lv_segment)//2):
    n=lv_segment[l*2:][:2]
    terrain.append(CTRL(n))
  
def DRAW_3D():
  global steps,ball,past,mn,chrono
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
      draw(" paused ",120,0,bg,c),stopall(17),rect(120,0,80,18,bg)
      chrono+=monotonic()-mn
  past+=1

def player():
  global a,b,ball,jump,imunimate,steps
  circle(ball[0],ball[1]-12,12,bg)
  a+=0.3 if jump else 0
  if ball[1]>=y0 and get(ball[0],ball[1]+1)!=bg:jump=False
  if key(4) and not jump:jump,a=True,-4
  b=limits(b+(key(3)-key(0))+(0.4 if b<0 else -0.4 if b>0 else 0),-4,4)
  ball[0],ball[1]=limits(ball[0]+int(b),26,320-26),limits(ball[1]+int(a),0,y0)
  circle(ball[0],ball[1]-12,12,c_ball2 if imunimate else c_ball)

def aff():
  global past,level,pourcent
  pourcent=int((past/((len(level)-40)//2))*100)
  player(),draw(str(pourcent)+"%",23-5*len(str(pourcent)),0,c,bg),sleep(0.002)

def fall():
  global ball,past,level,imunimate,deaths
  if get(ball[0],ball[1]+1)!=c and ball[1]==y0 and not imunimate and past>=1:
    past,ball[1],imunimate,deaths=limits(past-35,0,len(level)//2),y0,monotonic()+1.5,deaths+1
    rect(0,0,160,20,bg)
    return True

def WIN():
  global pourcent,chrono,deaths
  if pourcent>=100:
    tm="virtual time: {} min {}s".format(int(round(monotonic()-chrono,3)//60),round(round(monotonic()-chrono,3)%60,3))
    print(tm),background(bg),rect(0,80,320,62,c),draw("YOU WIN",125,82,bg,c),draw(tm,160-5*len(tm),102,bg,c),draw("deaths: "+str(deaths),120-5*len(str(deaths)),122,bg,c),stopall(4)
    return True

def seed(octets):
  global level
  char,level="ABCDEFGHIJKLMNOP","P"*10
  for i in range(octets):level+=choice(char)
  level+="P"*40
  return level

x0,y0,mn,pourcent,past,steps,a,b,jump,imunimate,deaths,octets=160,190,0,0,0,14,0,0,False,0,0,int(input("SIZE: "))
ball,terrain=[x0,y0],[]
c,bg,c_ball,c_ball2=(255,255,255),(0,210,120),(120,120,255),(255,120,120)

seed(octets),background(bg),draw(" NUMBALL ",115,92,bg,c),draw(" by VPROG ",110,112,c,bg),release(4)
while not key(4):draw(">PRESS OK TO START<",65,198,fadetime(bg,c),bg)
release(4),background(bg)

chrono=monotonic()

while True:
  DRAW_3D()
  if WIN():break
  chrono-=0.012
  steps=limits(steps+(key(2)*2-(key(1)*steps/10))*3,4,30)
  if monotonic()>imunimate:imunimate=0
  else:steps=14
