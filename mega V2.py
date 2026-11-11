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
  global past,chrono,level,pourcent
  pourcent,centre_x=int((past/((len(level)-48)//2))*100),160+(160-ball[0])//6
  unpack()
  for step in range(steps):
    offset=step/steps 
    for i in range(len(terrain)):
      position_virtuelle,tronc=i-offset,"0"*2+terrain[i]+"0"*2
      if position_virtuelle<0:continue
      echelle=1.0/(1.0+position_virtuelle*0.3)
      largeur_case,hauteur_tranche,y_ecran=int(52*echelle),int(11*echelle),int(85+130*echelle)
      largeur_totale=largeur_case*12
      x=centre_x-(largeur_totale//2)
      for rang in tronc:
        rect(x,y_ecran,largeur_case,hauteur_tranche,c if rang=="1" else bg)
        x+=largeur_case
    player()
    if fall():break
    if key(17):
      mn=monotonic()
      draw(" paused ",120,0,c_ball,c),stopall(17),rect(120,0,80,18,bg)
      chrono+=monotonic()-mn
  past+=1

def player():
  global a,b,ball,jump,imunimate,steps,FRAMES,frm
  circle(ball[0],ball[1]-12,12,bg)
  a+=0.3 if jump else 0
  if ball[1]>=y0 and get(ball[0],ball[1]+1)!=bg:jump=False
  if key(4) and not jump:jump,a=True,-4
  b=limits(b+(key(3)-key(0))+(0.4 if b<0 else -0.4 if b>0 else 0),-4,4)
  ball[0],ball[1]=limits(ball[0]+int(b),26,320-26),limits(ball[1]+int(a),0,y0)
  circle(ball[0],ball[1]-12,12,c_ball2 if imunimate else c_ball)
  FRAMES+=1
  sleep(0.002)

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
  global level,mode,idx
  if mode==0:
    char,level="0123456789abcdef","f"*10
    for i in range(octets):level+=choice(char)
    level+="f"*48
  if mode==1:
    level=levels[idx][6:]
  return level

image=["111011101110111101010001000101101011001010111101010001010101101011101110101"]

def IMG(N,x,y,ln,c):
  ln=15
  for i in range(len(image[N])):
    if image[N][i]=="1":set(x+i%ln,y+i//ln,c)

def init():
  global octets,idx,mode,theme,thm,c,c_ball,c_ball2,bg,FRAMES,frm
  FRAMES,frm=0,0
  release(4),background(bg),draw(" NUMBALL  ",110,72,bg,c),draw(" by VPROG ",110,92,c,bg),IMG(0,190,75,13,c_ball),rect(0,135,320,30,c)
  while not key(4):
    if key(12):
      thm=passlimits(thm+1,0,len(theme)-1)
      c,bg,c_ball,c_ball2=theme[thm]
      background(bg),draw(" NUMBALL  ",110,72,bg,c),draw(" by VPROG ",110,92,c,bg),IMG(0,190,75,13,c_ball),rect(0,135,320,30,c)
    mode=passlimits(mode+key(16),0,1)
    if mode==0:octets,sz=passlimits(octets+(key(3)-key(0))*2+(key(1)-key(2))*50,0,9001),"    < SIZE: "+str(octets)+" >    "
    if mode==1:
      try:
        from numball_seed import *
        if levels:idx,sz=passlimits(idx+key(3)-key(0),0,len(levels)-1),"    < INDEX: "+str(levels[idx][:5])+" >    "
      except:mode=0
    draw(sz,160-5*len(sz),141,c_ball,c),draw(">PRESS OK TO START<",65,198,fadetime(bg,c),bg),sleep(0.1+0.1*(key(16)+key(12)))
  release(4),background(bg),seed(octets if mode==0 else idx),background(bg)

x0,y0,mn,pourcent,past,steps,a,b,jump,imunimate,deaths,octets,idx,mode,thm=160,190,0,0,0,14,0,0,False,0,0,150,0,0,0
ball,terrain,chrono=[x0,y0],[],monotonic()

theme=[
[(255,255,255),(0,0,255),(255,0,0),(255,180,180)],
[(255,255,255),(215,120,50),(0,0,255),(180,180,255)],
[(0,4,0),(0,150,150),(255,0,0),(255,180,180)],
]

c,bg,c_ball,c_ball2=theme[0]

FRAMES,frm=0,0
init()
chrono=monotonic()

while True:
#  if monotonic()>frm:
#    draw(str(FRAMES)+"fps",0,20,(255,255,255),(0,0,0))
#    frm,FRAMES=monotonic()+1,0
  DRAW_3D()
  draw(" "+str(pourcent)+"% ",13-5*len(str(pourcent)),0,c,bg)
  if WIN() or key(26):
    init()
    mn,pourcent,past,steps,a,b,jump,imunimate,deaths,ball,terrain,chrono=0,0,0,14,0,0,False,0,0,[x0,y0],[],monotonic()
  steps=limits(steps+(key(2)*2-(key(1)*steps/10))*3,4,30)
  if monotonic()>imunimate:imunimate=0
  else:steps=14
    
