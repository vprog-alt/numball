from bprg import *
conv={"0":"0"*4,"1":"0001","2":"0010","3":"0011","4":"0100","5":"0101","6":"0110","7":"0111","8":"1000","9":"1001","a":"1010","b":"1011","c":"1100","d":"1101","e":"1110","f":"1"*4}

def RENDER(past,u):
  return level[past*2:][:u*2]
def CTRL(f,s=""):
  for rang in f:s+=conv[rang]
  return s
def unpack():
  global terrain
  lv_segment,terrain=RENDER(past,21),[]
  for l in range(len(lv_segment)//2):
    n=lv_segment[l*2:][:2]
    terrain.append(CTRL(n))
  
def DRAW_3D():
  global past,chrono,pourcent,level
  pourcent,centre_x=int((past/((len(level)-48)//2))*100),160+(160-ball[0])//6
  unpack(),draw(str(pourcent)+"%",23-5*len(str(pourcent)),0,c,bg)
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
    player(),sleep(0.001)
    if fall():break
    if key(17):
      mn=monotonic()
      draw(" paused ",120,0,c_ball,c),stopall(17),rect(120,0,80,18,bg)
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

def fall():
  global past,level,imunimate,deaths
  if get(ball[0],ball[1]+1)!=c and ball[1]==y0 and not imunimate and past>=1:
    past,ball[1],imunimate,deaths=limits(past-35,0,len(level)//2),y0,monotonic()+1.5,deaths+1
    rect(0,0,140,20,bg)
    return True

def WIN():
  global pourcent,chrono,deaths
  if pourcent>=100:
    tm="virtual time: {} min {}s".format(int(round(monotonic()-chrono,3)//60),round(round(monotonic()-chrono,3)%60,3))
    print(tm),background(bg),rect(0,80,320,62,c),draw("YOU WIN",125,82,bg,c),draw(tm,160-5*len(tm),102,c_ball,c),draw("deaths: "+str(deaths),120-5*len(str(deaths)),122,bg,c),stopall(4)
    return True

def seed(octets):
  global level
  char,level="0123456789abcdef","f"*10
  for i in range(octets):level+=choice(char)
  level+="f"*48
  return level

image=["10001011101111000100100100100010010011010001001001001110100100111"]

def IMG(N,x,y,ln,c):
  for i in range(len(image[N])):
    if image[N][i]=="1":set(x+i%ln,y+i//ln,c)

def init():
  global octets
  release(4),background(bg),draw(" NUMBALL  ",110,72,bg,c),draw(" by VPROG ",110,92,c,bg),IMG(0,190,75,13,c_ball),rect(0,135,320,30,c)
  while not key(4):
    octets,sz=limits(octets+(key(3)-key(0))*2+(key(1)-key(2))*50,0,9000)," < SIZE: "+str(octets)+" > "
    draw(">PRESS OK TO START<",65,198,fadetime(bg,c),bg),draw(sz,160-5*len(sz),141,c_ball,c),sleep(0.1)
  release(4),background(bg),seed(octets)

x0,y0,mn,pourcent,past,steps,a,b,jump,imunimate,deaths,octets=160,190,0,0,0,14,0,0,False,0,0,150
ball,terrain,chrono,theme=[x0,y0],[],monotonic(),[[(255,255,255),(50,120,255),(255,0,0),(255,180,180)],[(255,255,255),(210,120,50),(0,0,255),(180,180,255)]]
c,bg,c_ball,c_ball2=theme[1]
init()
chrono=monotonic()

while True:
  DRAW_3D()
  if WIN() or key(26):
    init()
    mn,pourcent,past,steps,a,b,jump,imunimate,deaths,ball,terrain,chrono=0,0,0,14,0,0,False,0,0,[x0,y0],[],monotonic()
  steps=limits(steps+(key(2)*2-(key(1)*steps/10))*3,4,30)
  if monotonic()>imunimate:imunimate=0
  else:steps=14
  
