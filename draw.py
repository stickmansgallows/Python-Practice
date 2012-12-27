#!/usr/bin/python

from Tkinter import *
import math

SCALE = 1
EDGE = 45.0*SCALE #Edge of hex (mm)
ROOT = math.sqrt(3)
GAP = 5.0*SCALE #Gap between hexes
XD = (ROOT*EDGE+GAP)/2.0 #x interval
YD = (3.0*EDGE+ROOT*GAP)/2.0 #y interval
OFFSET = 1 #Screen offset so hexes don't fall off
NIB = 8 #Nib size

def onehex(x,y): #gets 6 points for hex
    x0=x
    y0=y
    x1=x0+ROOT*EDGE/2.0
    y1=y0+EDGE/2.0
    x2=x1
    y2=y1+EDGE
    x3=x0
    y3=y0+EDGE*2.0
    x4=x0-ROOT*EDGE/2.0
    y4=y2
    x5=x4
    y5=y1
    
    shape=[x0,y0,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5]
    return shape
    
def makeNIB(x,y): #gets 9 points for nib
    a=ROOT*GAP/2
    x0=x
    y0=y
    x3=x0+GAP/2
    y3=y0+a
    x6=x0-GAP/2
    y6=y3
    x4=x3
    y4=y3+NIB
    x5=x6
    y5=y4
    
    x7=x6-NIB*ROOT/2
    y7=y6-NIB/2
    x8=x0-NIB*ROOT/2
    y8=y0-NIB/2
    x1=x0+NIB*ROOT/2
    y1=y8
    x2=x3+NIB*ROOT/2
    y2=y7
    
    shape=[x0,y0,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8]
    return shape
    
def makeNIB2(x,y): #gets 9 points for nib (inverted)
    a=ROOT*GAP/2
    x0=x
    y0=y
    x3=x0+GAP/2
    y3=y0-a
    x6=x0-GAP/2
    y6=y3
    x4=x3
    y4=y3-NIB
    x5=x6
    y5=y4
    
    x7=x6-NIB*ROOT/2
    y7=y6+NIB/2
    x8=x0-NIB*ROOT/2
    y8=y0+NIB/2
    x1=x0+NIB*ROOT/2
    y1=y8
    x2=x3+NIB*ROOT/2
    y2=y7
    
    shape=[x0,y0,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8]
    return shape
    
    
hexes=[] #each hex is an array of 6 x,y coordinates
nibs=[]
hexsets = [[3],[2,4],[1,3,5],[0,2,4,6],[1,3,5],[0,2,4,6],[1,3,5],[0,2,4,6],[1,3,5],[2,4],[3]]
nibset1 = [[],[2],[1,3],[0,2,4],[1,3,5],[0,2,4],[1,3,5],[0,2,4],[1,3],[2]]
nibset2 = [[],[4],[5,3],[6,4,2],[5,3,1],[6,4,2],[5,3,1],[6,4,2],[5,3],[4]]

i=0
for x in range(11):
    for y in hexsets[x]:
        hexes.append(onehex((x+OFFSET)*XD,(y+OFFSET)*YD))
        
for x in range(1,10):
    for y in nibset1[x]:
        nibs.append(makeNIB((x+OFFSET)*XD,(y+OFFSET)*YD+2*EDGE))

for x in range(1,10):
    for y in nibset2[x]:
        nibs.append(makeNIB2((x+OFFSET)*XD,(y+OFFSET)*YD))

master = Tk()

w = Canvas(master, width=800, height=800)
w.pack()


i=0
cL = ["blue", "red", "green", "yellow", "magenta", "orange", "brown", "cyan", "violet"]
for poly in hexes:
    w.create_polygon(poly, fill=cL[i])
    if i >= 8:
        i=0
    else:
        i=i+1

for i in nibs:
    w.create_polygon(i)



mainloop()




from pylab import *

# statements...
 
# Set appropriate figure width/height
#figure(figsize=(2.75, 1.75))
 
# Set appropriate margins, these values are normalized into the range [0, 1]
#subplots_adjust(left = 0.21, bottom = 0.22, right = 0.95, top = 0.95, wspace = 0.1, hspace = 0.1)
 
# Plot something in the figure
# See http://matplotlib.sourceforge.net/ for more plotting functions

hold(True)
for poly in hexes:
    x=[]
    y=[]
    for i in range(0,12,2):
        x.append(poly[i])
        y.append(poly[i+1])
        
    x.append(poly[0])
    y.append(poly[1])
    scatter(x,y)
    #hold(False)



#scatter(data_x, data_y, marker='o', linewidth=1.4, color="white", s=9, edgecolors='black')
 
# Show legends in the figure. We can use legend() to let matplotlib decide a good position for legends
#legend(loc = 'upper left')
 
# Set labels for axes
#xlabel('x-label')
#ylabel('y-label')
 
# Use log-scale in y-axis
#gca().set_yscale('log')
 
# Set the ranges
#xlim(10, 100)
#ylim(10, 1e5)
 
# Save the figure into .eps file
savefig('figure.eps', format='eps')
show()
exit(0)


"""
import Image
import PSDraw

# fns for measurement conversion    
PTS = lambda x:  1.00 * x    # points
INS = lambda x: 72.00 * x    # inches-to-points
CMS = lambda x: 28.35 * x    # centimeters-to-points

outputFile = 'myfilename.ps'
outputFileTitle = 'Wheel Tag 36147'

myf = open(outputFile,'w')
ps = PSDraw.PSDraw(myf)
ps.begin_document(outputFileTitle)

for poly in hexes:
    for i in range(6):
        lineFrom = (poly[i*2],poly[i*2+1])
        if i==5:
            i=-1
        lineTo   = (poly[(i+1)*2],poly[(i+1)*2+1])
        ps.line( lineFrom, lineTo )

for poly in nibs:
    for i in range(9):
        lineFrom = (poly[i*2],poly[i*2+1])
        if i==8:
            i=-1
        lineTo   = (poly[(i+1)*2],poly[(i+1)*2+1])
        ps.line( lineFrom, lineTo )
        
ps.end_document()
"""
#myf.close()

