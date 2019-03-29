import struct
import math
from math import cos, sin
from constants import *
from obj import Obj
from objectLoader import objectLoader
from textureLoader import textureLoader
from collections import namedtuple
from utils import *
 
class Bitmap(object):
    def __init__(self, filename):
        self.filename = filename
        self.glInit()
       

    def glInit(self): 
        self.framebuffer = []
        self.newGlColor = getColor(255, 255, 255)
        self.glInitTexParams()
        self.activeShader = self.setGouradShader
        self.activeShaderNoTexture = self.setGouradShaderNoTexture

    def glInitTexParams(self): 
        self.tex = None
        self.activeVArray = None 
        self.activeTexture = None 
        self.vertexBuffer = []
    
     #structure image file 
    def writeFile(self):
        f = open(self.filename, "wb")
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
    
    def createWindow(self, width, height): 
        self.width = width
        self.height = height
    
    #clear the canvas with a new color 
    def clearColor(self, r, g, b): 
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.framebuffer = [
            [getColor(newR, newG, newB) for x in range(self.width)]
            for y in range(self.height)
        ]
    
    def clearCanva(self): 
         self.framebuffer = [
            [
                #show background color 
                self.color(0,0,0) for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def setZBuffer(self, z="inf"):
        self.zbuffer = [ 
            [ -float(z) for x in range (self.width)]
            for y in range(self.height)
        ]

    def clear(self, r=0, g=0, b=0 ):
        self.clearColor(r,g,b)
        self.clearCanva()
        self.setZBuffer()
        
    # get dimension image (begin of glViewPort)
    def viewPort(self, x, y, width, height):
        self.viewPortWidth = width
        self.viewPortHeight = height
        self.xViewPort = x
        self.yViewPort = y
        self.loadViewPortMatrix()

    
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
    def vertex(self, x, y, color=None):
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
                self.framebuffer[math.floor(realY)][math.floor(realX)] = color or self.newGlColor

    def color(self, r, g, b):
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.newGlColor = getColor(newR, newG, newB)
        return self.newGlColor

    def point(self, x, y, color= None):
        try: 
            self.framebuffer[int(y)][int(x)] = color or self.newGlColor
        except: 
            pass 

    def lineLow(self, x1,y1, x2,y2): 
        dx = x2 - x1 
        dy = y2 - y1 

        yi = 1 

        if dy < 0: 
            yi = -1 
            dy - dy 
        
        D = dy*2 - dx 
        y = y1 

        for x in range (x1. x2): 
            self.vertex(self.getNormXCoord(x), self.getNormYCoord(y))
            if D > 0: 
                y = y + yi 
                D = D - dx*2 
            D = D + dy*2

    def lineHigh(self, x1,y1, x2,y2):
        dx = x2 - x1 
        dy = y2 - y1 

        if dx < 0: 
            xi = -1 
            dx = -dx 

        D = dx*2 - dy
        x = x1 

        for y in range(y1, y2): 
            self.vertex(self.getNormXCoord(x), self.getNormYCoord(y))
            if D > 0: 
                x = x + xi 
                D = D - dy*2
            D = D + dx*2

    def lineGl(self, x1, y1, x2,y2): 
        x1 = math.floor(self.getRXCoord(x1))
        y1 = math.floor(self.getRYCoord(y1))
        x2 = math.floor(self.getRXCoord(x2))
        y2 = math.floor(self.getRYCoord(y2))

        paramY = abs(y2 - y1) 
        paramX = abs(x2 - x1)

        if paramY < paramX: 
            if x1 > x2: 
                self.lineLow(x2, y2, x1, y1)
            else: 
                self.lineLow(x1, y1, x2, y2)
        else: 
            if y1 > y2: 
                self.lineHigh(x2,y2,x1,y1)
            else: 
                self.lineHigh(x1, y1, x2, y2)
                
    def line (self, x1, y1, x2, y2, color = None): 
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

        offset = 0 
        threshold = dx

        y = y1 

        for x in range (x1,x2 +1): 
            if steep:    
                self.point(y, x, color)
            else: 
                self.point(x, y, color)

            offset += dy * 2
            if offset >= threshold: 
                y += 1 if y1 < y2 else -1 
                threshold += dx * 2

    def lineSweeping(self, A, B, C, color=None): #Primer algoritmo enseñado para pintar los triangulos 
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
                    self.point(x,y, color) 
        
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
                        self.point(x,y, color)

    def loadTexture(self, filename, scale): 
        texture = textureLoader(filename)
        for y in range(texture.height): 
             for x in range(texture.width): 
                 xNorm = self.getNormXCoord(x)
                 yNorm = self.getNormYCoord(y)
                 tex_color = texture.getTextureColor(xNorm, yNorm)
                 xNormS = self.getNormXCoord(x*scale)
                 yNormS = self.getNormYCoord(y*scale)
                 self.vertex(xNormS, yNormS, tex_color)
        
    #donde t es la pinche textura 
    def loadObjWireFrameUV(self, filename, scale, t):  
        model = objectLoader(filename)
        for face in model.faces: 
            vcount = len(face)
            for j in range(vcount): 
                f1 = face[j][1]
                f2 = face[(j+1) % vcount][1]
                
                v1 = model.textures[f1 - 2]
                v2 = model.textures[f2 - 1]

                x1 = (v1[0] * scale) - t  
                x2 = (v2[0] * scale) - t
                y1 = (v1[1] * scale) - t
                y2 = (v2[1] * scale) - t
                
                self.lineGl(x1, y1, x2, y2)

    def loadObjWireFrame(self, filename, scale): 
        model = objectLoader(filename)

        for face in model.faces: 
            vcount: len(face) 

            for j in range (vcount): 
                f1 = face[j][1]
                f2 = face[(j+1) % vcount][1]

                v1 = model.textures[f1 -1] 
                v2 = model.textures[f2 -1]

                x1 = v1[0] * scale
                y1 = v1[1] * scale
                x2 = v2[0] * scale
                y2 = v2[1] * scale 

                self.lineGl(x1, y1, x2, y2)


    def loadObj(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0,0,0), intensity=1, texture=None): 
        self.loadModelMatrix(translate, scale, rotate)
        model = objectLoader(filename)
        if texture: 
            self.activeTexture = texture 
            vertexBuffer = []
            
            for face in model.faces: 
                for fi in face: 
                    transformedVertex = matrixTransform(
                        vertex3(*model.vertices[fi[0]]), 
                        self.viewPortMatrix, 
                        self.projectionMatrix, 
                        self.viewMatrix, 
                        self.modelMatrix
                    )
                    vertexBuffer.append(transformedVertex)
                        
                if self.activeTexture: 
                    for fi in face: 
                        texVertex = vertex3(*model.textures[fi[1]])
                        vertexBuffer.append(texVertex)
                
                for fi in face: 
                    normVertex = vertex3(*model.normals[fi[2]])
                    vertexBuffer.append(normVertex)
                    
            self.activeVArray = iter(vertexBuffer)

            try: 
                while True: 
                    self.baryctriangle()
            except StopIteration: 
                    pass
    
    def lookAt(self, e, c, u): 
        z = normProduct(sub(e,c))
        x = normProduct(crossProduct(u,z))
        y = normProduct(crossProduct(z,x))
        
        self.loadViewMatrix(x, y, z, c)
        self.loadProjectionMatrix( -1 / length(sub(e,c)))

        
    def loadModelMatrix(self, t=(0,0,0), s=(1,1,1), r=(0,0,0)):
        t = vertex3(*t)
        s = vertex3(*s)
        r = vertex3(*r)
        
        translation_matrix = [
            [1, 0, 0, t.x], 
            [0, 1, 0, t.y], 
            [0, 0, 0, t.x], 
            [0, 0, 0,   1]
        ]
        
        a = r.x 
        r_matrix_x = [ 
            [1,         0,            0,  0], 
            [0,     cos(a),     -sin(a),  0], 
            [0,     sin(a),      cos(a),  0],
            [0,          0,          0,   1]
        ]
        
        a = r.y 
        r_matrix_y = [ 
            [cos(a),    0,  -sin(a),    0],
            [     0,    1,        0,    0],
            [-sin(a),   0,   cos(a),    0],
            [0,         0,        0,    1]        
        ]
        
        a = r.z 
        r_matrix_z = [
            [cos(a),    -sin(a),    0,  0],
            [sin(a),     cos(a),    0,  0],
            [     0,          0,    1,  0],
            [     0,          0,    0,  1]
        ]
        
        rotation_matrix = matrixMult(matrixMult(r_matrix_x, r_matrix_y), r_matrix_z)
        
        scale_matrix = [
            [s.x,     0,      0,    0],
            [  0,   s.y,      0,    0],
            [  0,     0,    s.z,    0],
            [  0,     0,      0,    1]  
        ]
        
        self.modelMatrix = matrixMult(matrixMult(translation_matrix, rotation_matrix), scale_matrix)
        
        
    def loadViewMatrix(self, i, j, k, c): 
        
        M = [
            [i.x,   i.y,    i.z,    0],
            [j.x,   j.y,    j.z,    0],
            [k.x,   k.y,    k.z,    0],
            [  0,     0,      0,    1]
        ]
            
        O = [
            [1, 0, 0, -c.x],
            [0, 1, 0, -c.y],
            [0, 0, 1, -c.z],
            [0, 0, 0,    1]
        ]
            
        self.viewMatrix = matrixMult(M,O)

    def loadProjectionMatrix(self, k): 
        self.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, k, 1]
        ]
        
    def loadViewPortMatrix(self): 
        self.viewPortMatrix = [
            [self.viewPortWidth / 2,                           0,      0,     self.viewPortWidth / 2],
            [                      0,    self.viewPortHeight / 2,      0,    self.viewPortHeight / 2],
            [                      0,                           0,    128,                         128],
            [                      0,                           0,      0,                           1]
        ]
    
    def shaderIntensity(self, normal, intensity): 
        return (255* dotProduct(normal, vertex3(0,0,intensity)))

    def baryctriangle(self, intensity=1): 
        pointA = next(self.activeVArray)
        pointB = next(self.activeVArray)
        pointC = next(self.activeVArray)
        
        if self.activeTexture: 
            texVA = next(self.activeVArray)
            texVB = next(self.activeVArray)
            texVC = next(self.activeVArray)
            
            normalA = next(self.activeVArray)
            normalB = next(self.activeVArray)
            normalC = next(self.activeVArray)

            minBoundingBox, maxBoundingBox = boundingBox(pointA, pointB, pointC)

            normal = normProduct(crossProduct(sub(pointB, pointA), sub(pointC, pointA)))
            grey = self.shaderIntensity(normal, intensity)
            texIntensity = dotProduct(normal, vertex3(0,0,intensity))

            if texIntensity < 0: 
                return 

            for x in range (minBoundingBox.x, maxBoundingBox.x + 1): 
                for y in range(minBoundingBox.y, maxBoundingBox.y + 1): 
                    b1, b2, b3 = barycentric(pointA, pointB, pointC, vertex2(x,y))

                    if (b1 <0) or (b2 < 0) or (b3<0): 
                        continue
                    
                    if self.activeTexture: 
                        texXPos = (texVA.x * b1) + (texVB.x * b2) + (texVC.x * b3)
                        texYPos = (texVA.y * b1) + (texVB.y * b2) + (texVC.y * b3)

                        colour = self.activeShader( 
                            self, 
                            triangle=(pointA, pointB, pointC),
                            barycentric_coords=(b1, b2, b3),
                            texture_coords=(texXPos, texYPos),
                            varying_normals=(normalA, normalB, normalC),
                            intensity=intensity
                        ) 

                        z = (pointA.z * b1) + (pointB.z * b2) + (pointC.z * b3)

                        if (x < 0) or (y < 0): 
                            continue
                        
                        try: 
                            if z > self.zbuffer[y][x]: 
                                self.vertex(self.getNormXCoord(x), self.getNormYCoord(y), colour)
                                self.zbuffer[y][x] = z 
                        except: 
                            pass
                    else: 
                        if grey < 0: 
                            continue
                        
                        z = (pointA.z * b1) + (pointB.z * b2) + (pointC.z * b3)

                        if x < 0 or y < 0: 
                            continue
                        
                        colour_grey = self.activeShaderNoTexture( 
                            self,
                            barycentric_coords=(b1, b2, b3),                        
                            varying_normals=(normalA, normalB, normalC),
                            intensity=intensity 
                        )

                        try: 
                            if z > self.zbuffer[y][x]: 
                                self.vertex(self.getNormXCoord(x), self.getNormYCoord(y), colour_grey)
                                self.zbuffer[y][x] = z 
                        except: 
                            pass 
                    
    def setGouradShaderNoTexture(self,obj, **kwargs): 
        b1, b2, b3 = kwargs['barycentric_coords']
        normalA, normalB, normalC = kwargs['varying_normals']
        
        norm_x = normalA.x * b1 + normalB.x * b2 + normalC.x * b3
        norm_y = normalA.y * b1 + normalB.y * b2 + normalC.y * b3
        norm_z = normalA.z * b1 + normalB.z * b2 + normalC.z * b3
        
        norm = vertex3(norm_x, norm_y, norm_z)
        textureColor = getColor(255,255,255)
        texIntensity = dotProduct(norm, vertex3(0,0, kwargs['intensity']))
        try: 
            return color (
                int(textureColor[2] * texIntensity) if (textureColor[0] * texIntensity > 0)  else 0,
                int(textureColor[1] * texIntensity) if (textureColor[1] * texIntensity > 0)  else 0,
                int(textureColor[0] * texIntensity) if (textureColor[2] * texIntensity > 0)  else 0
            )
        except: 
            pass

    def setGouradShader(self, obj, **kwargs): 
        b1, b2, b3 = kwargs['barycentric_coords']
        texXPos, texYPos  = kwargs['texture_coords']
        textureColor = obj.activeTexture.getTextureColor(texXPos, texYPos)
        normalA, normalB, normalC = kwargs['varying_normals']
        intensityPointA, intensityPointB, intensityPointC = [
            dotProduct(normal, vertex3(0,0,kwargs['intensity'])) for normal in (normalA, normalB, normalC)
        ]

        texIntensity = (b1*intensityPointA) + (b2*intensityPointB) + (b3*intensityPointC)  

        try: 
            return color( 
                int(textureColor[2] * texIntensity) if (textureColor[0] * texIntensity > 0) else 0,
                int(textureColor[1] * texIntensity) if (textureColor[1] * texIntensity > 0) else 0,
                int(textureColor[0] * texIntensity) if (textureColor[2] * texIntensity > 0) else 0
            )
        except: 
            pass