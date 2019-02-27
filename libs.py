import struct
import math
from obj import Obj
from vectors_math import * 

def barycentric( A, B, C, P): 
    cx , cy , cz = crossProduct(
        vertex3(B.x - A.x , C.x - A.x , A.x - P.x),
        vertex3(B.y - A.y , C.y - A.y , A.y - P.y)
    )

    # [cx/cz cy/cz cz/cz = [u v 1]]
    if cz == 0: 
        return -1, -1, -1 

    u = cx/cz 
    v = cy/cz 
    w = 1 - u - v 

    return w, v, u

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
        self.zbuffer = []
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

        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range (self.height)
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

    def point(self, x, y):
        self.framebuffer[int(y)][int(x)] = self.newGlColor

    def load(self, filename, translate=(0, 0), scale=(1, 1)):
        model = Obj(filename)

        for face in model.vfaces:
            vcount = len(face)
            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j+1)%vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]

               # scaleX, scaleY = scale
                #translateX, translateY = translate

                x1 = v1[0]
                y1 = v1[1] 
                x2 = v2[0] 
                y2 = v2[1] 
        
                self.line(x1, y1, x2, y2)

    def line (self, x1, y1, x2, y2): 
        x1 = math.floor(self.getRXCoord(x1))
        x2 = math.floor(self.getRXCoord(x2))
        y1 = math.floor(self.getRYCoord(y1))
        y2 = math.floor(self.getRYCoord(y2))

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

        for x in range (x1,x2 +1): 
            if steep:    
                self.point(y, x)
            else: 
                self.point(x, y)

            offset += dy * 2
            if offset >= threshold: 
                y += 1 if y1 < y2 else -1 
                threshold += 1 * 2 * dx

    def triangleOne(self, A, B, C, color=None): 
        if A.y > B.y:
            A, B = B , A 
        if A.y > C.y: 
            A, C = C, A
        if B.y > C.y: 
            B , C = C, B 
        
        dxAc = C.x - A.x 
        dyAc = C.y - A.y 
        if dyAc == 0: 
            return 
        miAc = dxAc/dyAc

        dxAb  = B.x - A.x 
        dyAb = B.y - A.y 

        if dyAb != 0: 
            miAb = dxAb/dyAb
        
            for y in range(A.y, B.y + 1):
                xi = round(A.x - miAc * (A.y -y))
                xf = round(A.x - miAb * (A.y - y))

                if xi > xf: 
                    xi, xf = xf, xi 
                for x in range(xi, xf + 1): 
                    self.point(x,y) 
        
        dxBc = C.x - B.x 
        dyBc = C.y - B.y 
        if dyBc: 
            miBc = dxBc/dyBc

            for y in range(B.y, C.y + 1): 
                xi = round(A.x - miAc * (A.y - y))
                xf = round(B.x - miBc * (B.y - y))

                if xi > xf: 
                    xi, xf = xf, xi 

                    for x in range(xi, xf + 1): 
                        self.point(x,y)

    def loadOne(self, filename, translate=(0,0,0), scale=(1,1,1)): 
         model = Obj(filename)

         light = vertex3(0,0,1)

         for face in model.vfaces: 
             vcount = len(face)

             if vcount == 3: 
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1 
            
                a = transform(model.vertices[f1], translate, scale)
                b = transform(model.vertices[f2], translate, scale)
                c = transform(model.vertices[f3], translate, scale)

                normal = normProduct(crossProduct(sub(b,a), sub(c,a)))
                intensity = dotProduct(normal, light)
                grey = round(255 * intensity)

                if grey < 0: 
                    continue
                self.triangleOne(a,b,c, color(grey,grey,grey))
             else: 
              f1 = face[0][0] - 1
              f2 = face[1][0] - 1
              f3 = face[2][0] - 1
              f4 = face[3][0] - 1

              vertices  = [
                  transform(model.vertices[f1], translate, scale),
                  transform(model.vertices[f2], translate, scale),
                  transform(model.vertices[f3], translate, scale),
                  transform(model.vertices[f4], translate, scale)
              ]

              normal = normProduct(crossProduct(sub(vertices[0], vertices[1]), sub(vertices[1], vertices[2])))
              intensity = dotProduct(normal, light)
              grey = round(255 * intensity)

              if grey < 0:
                  continue 
              
              A, B, C, D = vertices 

              self.triangleOne(A, B, C, color(grey, grey,grey))
              self.triangleOne(A, C, D, color(grey,grey,grey))
              
                
