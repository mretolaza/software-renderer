import libs 
import struct
import os 
from libs import Bitmap
from libs import word

#Objet to draw 
img = None

#Constructor 
def glInit():
    return None

#Init FrameBuffer
def glCreateWindow(width, height):
    global img 
    img = Bitmap(width,height) 

#Delete actual image 
def glClear(): 
    img.clear()
#Image area can draw
def glViewPort(x,y,widht, height):
    img.viewPort(x,y,widht, height)

#Get Color 
def glColor(r,g,b):
    img.color(r,g,b)

#Init canvas with new color 
def glClearColor(r,g,b):
    img.clearColor(0,0,0) 

#Get new x,y points 
def glVertex(x,y):
    img.vertex(x,y)

def glLine (x1,y1, x2,y2):
    img.line(x1, y1, x2, y2)

#Show new image 
def glFinish():
    img.writeFile("img.bmp")

glCreateWindow(800,400)
glViewPort(0,0,300,300)
glClear()
glColor(1, 0, 0)
glVertex(0,0)
glLine(299,200,100,100)
glFinish()