#!/usr/apps/bin/python

#09-28-2011
from math import *
import time
import random
from tkinter import *

def key(event):		#Catches keystrokes
        x=event.char
        global exit
        if x == ' ':
                exit=False


step = .1	#Step size
tmin = 0	#Start time
tmax = 50	#End time
l = 100		#Number of objects
ax = 0.0	#x acceleration
ay = -9.8	#y acceleration
vmax = 100	#Max velocity
vmin = -100	#Min velocity
xmin = 0	#Window min
xmax = 400	#Window max
ymin = 0	#Window min
ymax = 400	#Window max
r = .4		#Elasticity (1=Elastic, 0=Inelastic, 0.5=Halfway)
size = 4	#Object size
cL = ["blue", "red", "green", "yellow", "magenta", "orange"]

full = list(range(l))
master = Tk()

#Create empty arrays
dot = [] #color
x = [] #position
y = []
vx = [] #velocity
vy = []
m = [] #mass
aa = []
ay = -ay

w = Canvas(master, width=xmax, height=ymax)
w.pack()

count=0
ycount=0
for i in list(range(l)):
	m.append(1)
	aa.append(1)
	x.append(random.uniform(xmin,xmax))
	y.append(random.uniform(ymin,ymax))
	vx.append(random.uniform(vmin,vmax))
	vy.append(random.uniform(vmin,vmax))
	
	#vx[i]=0
	#vy[i]=0
	#x[i]= 400+count*size*2
	#y[i]=size+ycount*size*2+200
	#count=count+1
	#if count > 5:
	#	count = 0
	#	ycount = ycount + 1
		
	y[i] = ymax - y[i]
	vy[i] = -vy[i]

	#Coloring according to mass
	if m[i] < 1/6.0:
		col =cL[0]
	elif m[i] < 1/3.0:
		col =cL[1]
	elif m[i] < 1/2.0:
		col =cL[2]
	elif m[i] < 2/3.0:
		col =cL[3]
	elif m[i] < 5/6.0:
		col =cL[4]
	else:
		col =cL[5]
	col = random.choice(cL)
	dot.append(w.create_oval(int(x[i]-size), int(y[i]-size), int(x[i]+size), int(size+y[i]), width=0, fill=col))
	

x[-1]=0
y[-1]=ymax
vx[-1]=100
vy[-1]=100
m[-1]=1

master.bind_all('<Key>', key)
exit=True
while exit:
        for i in full: #for each particle
                x[i] = x[i] + vx[i]*step #update movement
                y[i] = y[i] + vy[i]*step
                vx[i] = vx[i] + ax*step*aa[i]
                vy[i] = vy[i] + ay*step*aa[i]
                aa[i]=1

                #Edge conditions
                if x[i]+size >= xmax:
                        vx[i] = -vx[i]*r
                        x[i] = xmax-size
                if x[i]-size <= xmin:
                        vx[i] = -vx[i]*r
                        x[i] = xmin+size
                if y[i]+size >= ymax:
                        vy[i] = -vy[i]*r
                        y[i] = ymax-size
                if y[i]-size <= ymin:
                        vy[i] = -vy[i]*r
                        y[i] = ymin+size

                for j in list(range(0,i)): #Check for collisions
                        if sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)/2 <= size:
                                m21=m[j]/m[i]
                                x21 = x[j]-x[i]+random.uniform(1e-12,1e-2)
                                y21 = y[j]-y[i]
                                vx21 = vx[j]-vx[i]
                                vy21 = vy[j]-vy[i]
                                a = y21/x21
                                vx_cm = (m[i]*vx[i]+m[j]*vx[j])/(m[i]+m[j]) 
                                vy_cm = (m[i]*vy[i]+m[j]*vy[j])/(m[i]+m[j])
                                if (vx21*x21 + vy21*y21) >= 0:
                                        continue
                                dvx2 = -2*(vx21 +a*vy21)/((1+a*a)*(1+m21))
                                vx[j]=vx[j]+dvx2;
                                vy[j]=vy[j]+a*dvx2;
                                vx[i]=vx[i]-m21*dvx2;
                                vy[i]=vy[i]-a*m21*dvx2;

                                 
                                vx[i]=(vx[i]-vx_cm)*r + vx_cm
                                vy[i]=(vy[i]-vy_cm)*r + vy_cm
                                vx[j]=(vx[j]-vx_cm)*r + vx_cm
                                vy[j]=(vy[j]-vy_cm)*r + vy_cm	
                                aa[i]=0
                                aa[j]=0

							
                w.coords(dot[i], int(x[i]-size), int(y[i]-size), int(x[i]+size), int(size+y[i]))
		
        #time.sleep(0.025)
    	
        w.update()
	



master.destroy()
#mainloop()
