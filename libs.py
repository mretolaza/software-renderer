"""Librerías Internas 
""" 

import struct
import random
from math import sqrt
from math import ceil
from random import randint

def char(c):
    return struct.pack("=c", c.encode('ascii'))

def word(c):
    return struct.pack("=h", c)

def dword(c):
    return struct.pack("=l", c)

def getColor(r, g, b):
    return bytes([b, g, r])

class Bitmap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.r = 0
        self.g = 0
        self.b = 0 
        self.vpWidth = 0
        self.vpHeight = 0
        self.vpX = 0 
        self.vpY = 0 
        self.vr = 0
        self.vg = 0
        self.vb = 0
        self.clear()
    
    #structure image file 
    def writeFile(self, filename):
        f = open(filename, "wb")
        # estandar
        f.write(char('B'))
        f.write(char('M'))
        # file size
        f.write(dword(14 + 40 + self.width * self.height * 3))
        # reserved
        f.write(dword(0))
        # data offset
        f.write(dword(54))
        # header size
        f.write(dword(40))
        # width
        f.write(dword(self.width))
        # height
        f.write(dword(self.height))
        # planes
        f.write(word(1))
        # bits per pixel
        f.write(word(24))
        # compression
        f.write(dword(0))
        # image size
        f.write(dword(self.width * self.height * 3))
        # x pixels per meter
        f.write(dword(0))
        # y pixels per meter
        f.write(dword(0))
        # number of colors
        f.write(dword(0))
        # important colors
        f.write(dword(0))
        # image data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])
        # close file
        f.close()
    
    def setColor(self, r,g,b): 
        self.vr = r
        self.vg = g 
        self.vb = b 

    # Clear image 
    def clear(self):
        self.framebuffer = [
            [
                #show background color 
                getColor(self.r,self.g,self.b) for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    #clear the canvas with a new color 
    def clearColor(self, newR, newG, newB):
        self.r = ceil(newR*255)
        self.g = ceil(newG*255)
        self.b = ceil(newB*255) 

    # get dimension image (begin of glViewPort)
    def viewPort(self, x, y, width, height):
        if height <= 0 or width <= 0:
            print('Error, el Largo y el Ancho de la imágen deben de ser valores mayores a 0')
            input()
        elif x< 0 or y < 0 or x > self.width or y > self.height:
            print('Error, Las coordenadas ingresadas (x,y) deben de ser mayores a 0. Además deben de ser menores al ancho y largo de la imagen')
            input()
        else:  
            self.vpWidth = width
            self.vpHeight = height
            self.vpX = x 
            self.vpY = y 

    # create new canvas to draw image 
    def vertex(self, x, y): 
        pointSize = 10
        if self.vpHeight !=  0 or self.vpWidth != 0:
            xx = x * ((self.vpWidth - pointSize) / 2)
            yy = y * ((self.vpHeight - pointSize) / 2)
            localX = self.vpX+int((self.vpWidth - pointSize)/2)+int(xx)
            localY = self.vpY+int((self.vpHeight - pointSize)/2)+int(yy)
            print(x, y, localX, localY)
            for x in range(pointSize):
                for y in range(pointSize):
                    self.point(localX + x, localY + y)
        else: 
            print('Debe de ejecutar glViewPort para obtener un área a gráficar')

    # Create point in framebuffer
    def point(self, x, y):
        self.framebuffer[y][x] = getColor(self.vr, self.vg, self.vb)

    # Set random white and black
    def random(self):
        whiteColor = [255, 255, 255]
        blackColor = [0,0,0]
        for y in range(self.height):
            for x in range(self.width):
                self.setColor(*random.choice([whiteColor, blackColor]))
                self.point(x, y)

    # Set random color
    def randomColor(self):
        for y in range(self.height):
            for x in range(self.width):
                self.setColor(randint(0,255), randint(0,255), randint(0,255))
                self.point(x, y)

    # draw left line
    def drawLeftLine(self,padding):
        x = padding
        for y in range(padding, self.vpHeight - padding):
            self.point(x, y)
    
    # draw rigth line
    def drawRightLine(self,padding):
        x = self.vpWidth - padding
        for y in range(padding, self.vpHeight - padding):
            self.point(x, y)

    # draw top line
    def drawTopLine(self,padding):
        y = padding
        for x in range(padding, self.vpWidth - padding):
            self.point(x, y)

    # draw botton line
    def drawBottonLine(self,padding):
        y = self.vpHeight - padding
        for x in range(padding, self.vpWidth - padding):
            self.point(x, y)

    # Create square 
    def square(self, size):
        cordX = int((self.vpWidth / 2)) - int(size / 2)
        cordY = int((self.vpWidth / 2)) - int(size / 2)
        for x in range (cordX, cordX + size):
            for y in range (cordY, cordY + size):
                self.point(x,y)

    # draw Slash
    def drawSlash(self):
        for cord in range(self.vpX, self.vpWidth):
            self.point(cord, cord)

    # stars
    def stars(self, numOfStars):
        loop = 0
        while(loop < numOfStars):
            loop = loop + 1
            size = randint(1, 3)
            x = randint(0, self.vpWidth - size - 2)
            y = randint(0, self.vpHeight - size - 2)
            self.printStar(x, y, size)

    # print starts 
    def printStar(self, x, y, size):
        for cordX in range(size):
            for cordY in range(size):
                self.point(cordX + x, cordY + y)

    #line custom 
    def lineCustom(self, x1 , y1 , x2 , y2):
        i = 0 
        while i <= 1:
            x = x1 + (x2 - x1) * i 
            y = y1 + (y2 - y1) * i 
            self.point( round(x) , round(y))
            i += 0.01 

    def line (self, x1, y1, x2, y2): 
        dy = abs(y2 - y1) 
        dx = abs(x2 - x1) 

        steep = dy > dx 

        if steep: 
            x1, y1 = y1 , x1 
            x2, y2  = y2, x2 

        if  x1 > x2: 
            x1,x2 = x2, x1 
            y1, y2 = y2, y1

        dy = abs(y2 - y1)  
        dx = abs(x2 - x1)  

        offset = 0  * 2 * dx
        threshold = 0.5 * 2 * dx

        y = y1 
        for x in range (x1, x2 + 1):
            if steep: 
                self.point(y, x)
            else: 
                self.point(x, y)
            offset += dy
            if offset >= threshold: 
                y += 1 if y1 < y2 else -1 
                threshold += 1 * 2 * dx

