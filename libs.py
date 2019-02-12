import struct
import math

def char(c):
    return struct.pack("=c", c.encode('ascii'))

def word(c):
    return struct.pack("=h", c)

def dword(c):
    return struct.pack("=l", c)

def color(r, g, b):
    return bytes([b, g, r])

class Bitmap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.newGlColor = color(255, 255, 255)
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
    
    #clear the canvas with a new color 
    def clearColor(self, r, g, b): 
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.framebuffer = [
            [color(newR, newG, newB) for x in range(self.width)]
            for y in range(self.height)
        ]
    
    # Clear image 
    def clear(self):
        self.framebuffer = [
            [
                #show background color 
                self.color(0,0,0) for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    # get dimension image (begin of glViewPort)
    def viewPort(self, x, y, width, height):
        self.viewPortWidth = width
        self.viewPortHeight = height
        self.xViewPort = x
        self.yViewPort = y
    
    def getRXCoord(self, x):
        dx = x * (self.viewPortWidth / 2)
        realXVP = (self.viewPortWidth / 2) + dx
        realX = realXVP + self.xViewPort
        return realX

    def getRYCoord(self, y):
        dy = y * (self.viewPortHeight / 2)
        realYVP = (self.viewPortHeight / 2) + dy
        realY = realYVP + self.yViewPort
        return realY

    def getNormXCoord(self, realX):
        realXVP = realX - self.xViewPort
        dx = realXVP - (self.viewPortWidth / 2)
        x = dx / (self.viewPortWidth / 2)
        return x

    def getNormYCoord(self, realY):
        realYVP = realY - self.yViewPort
        dy = realYVP - (self.viewPortHeight / 2)
        y = dy / (self.viewPortHeight / 2)
        return y

    # create new canvas to draw image 
    def vertex(self, x, y):
        if ((x >= -1 and x <= 1) and (y >= -1 and y <= 1)):
            # x           
            dx = x * (self.viewPortWidth / 2)
            realXVP = (self.viewPortWidth / 2) + dx

            # y
            dy = y * (self.viewPortHeight / 2)
            realYVP = (self.viewPortHeight / 2) + dy

            # Add new viewports 
            realX = realXVP + self.xViewPort
            realY = realYVP + self.yViewPort       

            # draw inside dimensions 
            if ((realX <= self.width) and (realY <= self.height)):
                if (realX == self.width):
                    realX = self.width - 1
                if (realY == self.height): 
                    realY = self.height - 1
                self.framebuffer[math.floor(realY)][math.floor(realX)] = self.newGlColor

    def color(self, r, g, b):
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.newGlColor = color(newR, newG, newB)
        return self.newGlColor

    def point(self, x, y, color):
        self.framebuffer[y][x] = color

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
        count = x1 
        while (x2  + 1) >= count:
        #for x in range (x1,x2 +1): 
            if steep:    
                self.point(y, count , self.newGlColor)
            else: 
                self.point(count, y, self.newGlColor)

            offset += dy * 2
            if offset >= threshold: 
                y += 1 if y1 < y2 else -1 
                threshold += 1 * 2 * dx
            count += 1 