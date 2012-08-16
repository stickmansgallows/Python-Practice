#!/usr/bin/python
#Enemy and Defender Simulator
#10-03-2011
import time
import random
from Tkinter import *

def saturate(v, lim):
    if v > lim:
        v=lim
    elif v < -lim:
        v=-lim
    return v
    
def key(event):     #Catches keystrokes
    x=event.char
    global restart
    global l
    global playon
    global next_p
    if x == ' ':
         restart=False
    if x == '+':
         l=l+1
         restart=False
    if x == '-':
         if l > 3:
            l=l-1
         restart=False
    if x == 'q' or x == 'Q':
         restart=False
         playon=False
    if x == 'n' or x == 'N':
        next_p = next_p+1
        if next_p >= l:
            next_p = -1


l=10        #Number of players
step=.01    #Step size
xmin=0      #Window min 
xmax=1000   #Window max
ymin=0      #Window min 
ymax=600    #Window max
vmax=2000   #Max velocity
amax=5000   #Max accel
size=4      #Size of player
buff=8      #Buffer distance to hide behind defender

#Characteristic equation: a = ac*a+dis*v+r*p or a = ac+dis*s+r*s^2
r=60        #Position gain
dis=-15     #Velocity gain
ac=.6       #Accel gain
pl=-1       #Debugging graph. -1 to disable

if pl != -1:
    import pylab
cL = ["blue", "red", "green", "yellow", "magenta", "orange", "brown", "cyan", "violet"]

player=[]
savex=[]
savey=[]
master = Tk()
w = Canvas(master, width=xmax, height=ymax)
w.pack()
playon = True
next_p = -1

while playon:
    full = range(l)
    w.delete(ALL)
    master.title("N = "+str(l))
    for i in full:                      #Setup
        player.append({})
        player[i]['x']=random.uniform(xmin,xmax)    #Initial position
        player[i]['y']=random.uniform(ymin,ymax)
        player[i]['vx']=0               #Initial velocity
        player[i]['vy']=0
        player[i]['ay']=0               #Initial acceleration
        player[i]['ax']=0
        
        choose = range(l-1)
        for j in choose:
            if choose[j] >= i:
                choose[j] = choose[j]+1

        pick2 = random.sample(choose, 2)
        player[i]['enemy']=pick2[0]
        player[i]['defender']=pick2[1]
        
        col = random.choice(cL)
        player[i]['dot']=(w.create_oval(int(player[i]['x']-size), int(player[i]['y']-size), int(player[i]['x']+size), int(size+player[i]['y']), width=0, fill=col))

    restart=True
    ret = 0
    master.bind_all('<Key>', key)
    while restart:
        
        if (next_p == -1 and ret == 1):     #Return to random colors
            for i in full:
                w.itemconfig(player[i]['dot'], fill=random.choice(cL))
                ret = 0
        elif next_p != -1:                  #Turn the other players black
            for i in full:
                w.itemconfig(player[i]['dot'], fill='black')
                
        for i in full:                      #Turn the current player blue and highlight his enemy in red and his defender in green
            if next_p == i:
                w.itemconfig(player[i]['dot'], fill='blue')
                w.itemconfig(player[player[i]['enemy']]['dot'], fill='red')
                w.itemconfig(player[player[i]['defender']]['dot'], fill='green')
                ret = 1
            
            player[i]['vx'] = saturate(player[i]['vx'] + player[i]['ax']*step, vmax)
            player[i]['vy'] = saturate(player[i]['vy'] + player[i]['ay']*step, vmax)
            player[i]['x'] = player[i]['x'] + player[i]['vx']*step #Movement
            player[i]['y'] = player[i]['y'] + player[i]['vy']*step
            
            e = player[i]['enemy']
            d = player[i]['defender']
            m = (player[e]['y']-player[d]['y']+1e-12)/(player[e]['x']-player[d]['x']+1e-12) #Enemy/defender slope
            b = player[d]['y']-m*player[d]['x']                 #Enemy/defender y-intercept
            x0 = (m*player[i]['y']+player[i]['x']-m*b)/(m**2+1) #Nearest point on enemy/defender line
            y0 = m*x0+b

            d0 = player[e]['x']-x0 
            d1 = player[d]['x']-x0
                           
            if ((d0 > 0 and d1 > 0) or (d0 < 0 and d1 < 0)) and (abs(d0) > abs(d1)):
                pass
            else: #Tells the player to get to the defender because the enemy is closer
                s = d1/abs(d1)
                if m > 1:
                    x0=player[d]['x']+s*buff*size/m
                    y0=player[d]['y']+s*buff*size
                else:
                    x0=player[d]['x']+s*buff*size
                    y0=player[d]['y']+s*m*buff*size

            if i == pl:
                x0=100
                y0=100
                savex.append(x0-player[pl]['x'])
                savey.append(y0-player[pl]['y'])
                            
            player[i]['ax'] = saturate(ac*player[i]['ax']+dis*player[i]['vx']+r*(x0-player[i]['x']), amax) #New accel   
            player[i]['ay'] = saturate(ac*player[i]['ay']+dis*player[i]['vy']+r*(y0-player[i]['y']), amax) #New accel
    
            #Swap to the other side
            if player[i]['x'] < xmin:
                player[i]['x']=xmax-.1
            elif player[i]['x'] > xmax:
                player[i]['x']=xmin+.1
            if player[i]['y'] < ymin:
                player[i]['y']=ymax-.1
            elif player[i]['y'] > ymax:
                player[i]['y']=ymin+.1
            
            
            w.coords(player[i]['dot'], int(player[i]['x']-size), int(player[i]['y']-size), int(player[i]['x']+size), int(size+player[i]['y']))
        time.sleep(.025)
        w.update()
            
master.destroy()
if pl != -1:
    pylab.plot(savex)
    pylab.show()
#mainloop()
