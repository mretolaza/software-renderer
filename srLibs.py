import struct
import math
from math import cos, sin
import random
from random import randint
from objectLoader import objectLoader
from textureLoader import textureLoader
from collections import namedtuple
from constants import *
from utils import *

class Bitmap(object):
    def __init__(self, filename):
        self.filename = filename
        self.glInit()

    def glInit(self):
        self.framebuffer = []
        self.newGLColor = color(250, 214, 165)
        self.glInitTexture()
        self.activeShader = self.glSetGouradShader
        self.activeShaderNoTexture = self.glSetGouradShaderNoTexture

    def glInitTexture(self):
        self.tex = None
        self.activeVertexArray = None
        self.activeTex = None
        self.vertexBuffer = []

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewPort(self, x, y, width, height):
        self.viewportWidth = width
        self.viewportHeight = height
        self.viewportXOS = x
        self.viewportYOS = y
        self.loadViewPortMatrix()

    def glClear(self, r=0, g=0, b=0):
        self.glClearColor(r, g, b)
        self.setZBuffer()

    def glClearColor(self, r, g, b): 
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.framebuffer = [
            [color(newR, newG, newB) for x in range(self.width)]
            for y in range(self.height)
        ]

    def setZBuffer(self, z='inf'):
        self.zBuffer = [
            [-float(z) for x in range(self.width)]
            for y in range(self.height)
        ]

    def getRealXCoord(self, x):
        dx = x * (self.viewportWidth / 2)
        realXViewportCd = (self.viewportWidth / 2) + dx
        realXC = realXViewportCd + self.viewportXOS
        return realXC

    def getRealYCoord(self, y):
        dy = y * (self.viewportHeight / 2)
        realYViewportCd = (self.viewportHeight / 2) + dy
        realYC = realYViewportCd + self.viewportYOS
        return realYC

    def getNormXCoord(self, realXC):
        realXViewportCd = realXC - self.viewportXOS
        dx = realXViewportCd - (self.viewportWidth / 2)
        x = dx / (self.viewportWidth / 2)
        return x

    def getNormYCoord(self, realYC):        
        realYViewportCd = realYC - self.viewportYOS
        dy = realYViewportCd - (self.viewportHeight / 2)
        y = dy / (self.viewportHeight / 2)
        return y

    def glVertex(self, x, y, color=None):
        if ((x >= -1 and x <= 1) and (y >= -1 and y <= 1)):
                 
            dx = x * (self.viewportWidth / 2)
            realXViewportCd = (self.viewportWidth / 2) + dx

            dy = y * (self.viewportHeight / 2)
            realYViewportCd = (self.viewportHeight / 2) + dy

            realXC = realXViewportCd + self.viewportXOS
            realYC = realYViewportCd + self.viewportYOS           

            if ((realXC <= self.width) and (realYC <= self.height)):
                if (realXC == self.width):
                    realXC = self.width - 1
                if (realYC == self.height): 
                    realYC = self.height - 1
                self.framebuffer[round(realYC)][round(realXC)] = color or self.newGLColor

    def glColor(self, r, g, b):
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.newGLColor = color(newR, newG, newB)

    def lineBotton(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        yi = 1

        if (dy < 0):
            yi = -1
            dy = -dy
        
        D = 2*dy - dx
        y = y1

        for x in range(x1, x2):            
            self.glVertex(self.getNormXCoord(x), self.getNormYCoord(y))
            if (D > 0):
                y = y + yi
                D = D - 2*dx
            
            D = D + 2*dy

    def lineTop(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        xi = 1

        if (dx < 0):
            xi = -1
            dx = -dx
        
        D = 2*dx - dy
        x = x1

        for y in range(y1, y2):            
            self.glVertex(self.getNormXCoord(x), self.getNormYCoord(y))
            if (D > 0):
                x = x + xi
                D = D - 2*dy
            
            D = D + 2*dx

    def glLine(self, x0, y0, x1, y1):
        x0 = math.floor(self.getRealXCoord(x0))
        y0 = math.floor(self.getRealYCoord(y0))
        x1 = math.floor(self.getRealXCoord(x1))
        y1 = math.floor(self.getRealYCoord(y1))        

        if abs(y1 - y0) < abs(x1 - x0):
            if (x0 > x1):
                self.lineBotton(x1, y1, x0, y0)
            else:
                self.lineBotton(x0, y0, x1, y1)
        else:
            if (y0 > y1):
                self.lineTop(x1, y1, x0, y0)
            else:
                self.lineTop(x0, y0, x1, y1)

    def glLoadObjWireFrame(self, filename, scale):
        model = objectLoader(filename)

        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j+1) % vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]                

                x1 = v1[0] * scale
                y1 = v1[1] * scale
                x2 = v2[0] * scale
                y2 = v2[1] * scale

                self.glLine(x1, y1, x2, y2)

    def glLoadTexture(self, filename, scale):
        texture = textureLoader(filename)
        
        for y in range(texture.height):
            for x in range(texture.width):
                texColor = texture.getTextureColor(
                    self.getNormXCoord(x), 
                    self.getNormYCoord(y)
                )
                self.glVertex(
                    self.getNormXCoord(x*scale), 
                    self.getNormYCoord(y*scale), 
                    texColor
                )

    def glLoadObjWireFrameUV(self, filename, scale, texture):
        model = objectLoader(filename)              

        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                f1 = face[j][1]
                f2 = face[(j+1) % vcount][1]

                v1 = model.textures[f1 - 1]
                v2 = model.textures[f2 - 1]

                x1 = (v1[0] * scale) - texture
                y1 = (v1[1] * scale) - texture
                x2 = (v2[0] * scale) - texture
                y2 = (v2[1] * scale) - texture

                self.glLine(x1, y1, x2, y2)

    def glLoadObj(self, filename, texture=(0,0,0), scale=(1,1,1), r=(0,0,0), intensity=1, tex=None):

        self.glLoadModelMatrix(texture, scale, r)

        model = objectLoader(filename)
        if tex:
            self.activeTex = tex
            
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

            if self.activeTex:
                for fi in face:
                    textureVertex = vertex2(*model.textures[fi[1]])
                    vertexBuffer.append(textureVertex)

            for fi in face:
                normalVertex = vertex3(*model.normals[fi[2]])
                vertexBuffer.append(normalVertex)

        self.activeVertexArray = iter(vertexBuffer)        

        try:
            while True:
                self.glBarycentricTriangle()
        except StopIteration:
                pass

    def glLookAt(self, e, c, u):
        z = vectorNormal(sub(e, c))
        x = vectorNormal(crossProduct(u, z))
        y = vectorNormal(crossProduct(z, x))

        self.glLoadViewMatrix(x, y, z, c)
        self.glLoadProjectionMatrix(-1 / vecLength(sub(e, c)))        

    def glLoadModelMatrix(self, texture=(0,0,0), scale=(1,1,1), r=(0,0,0)):
        texture = vertex3(*texture)
        scale = vertex3(*scale)
        r = vertex3(*r)

        translationMatrix = [
            [1, 0, 0, texture.x],
            [0, 1, 0, texture.y],
            [0, 0, 1, texture.z],
            [0, 0, 0,   1]
        ]

        a = r.x
        rMatrixX = [
            [1,          0,          0,  0],
            [0,     cos(a),    -sin(a),  0],
            [0,     sin(a),     cos(a),  0],
            [0,          0,          0,  1]
        ]

        a = r.y
        rMatrixY = [
            [cos(a),    0,  -sin(a),    0],
            [     0,    1,        0,    0],
            [-sin(a),   0,   cos(a),    0],
            [0,         0,        0,    1]
        ]

        a = r.z
        rMatrixZ = [
            [cos(a),    -sin(a),    0,  0],
            [sin(a),     cos(a),    0,  0],
            [     0,          0,    1,  0],
            [     0,          0,    0,  1]
        ]

        rotationMatrix = matrixMult(
            matrixMult(
                rMatrixX, 
                rMatrixY
                ), 
                rMatrixZ
            )
        scaleMatrix = [
            [scale.x,     0,      0,    0],
            [  0,   scale.y,      0,    0],
            [  0,     0,    scale.z,    0],
            [  0,     0,      0,    1]
        ]

        self.modelMatrix = matrixMult(
            matrixMult(
                translationMatrix, 
                rotationMatrix
                ), 
                scaleMatrix
            )

    def glLoadViewMatrix(self, i, j, k, c):
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

        self.viewMatrix = matrixMult(M, O)

    def glLoadProjectionMatrix(self, k):
        self.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, k, 1]
        ]

    def loadViewPortMatrix(self):
        self.viewPortMatrix = [
            [self.viewportWidth / 2,                           0,      0,     self.viewportWidth / 2],
            [                      0,    self.viewportHeight / 2,      0,    self.viewportHeight / 2],
            [                      0,                           0,    128,                         128],
            [                      0,                           0,      0,                           1]
        ]

    def glShaderIntensity(self, normal, intensity):
        return round(255 * dotProduct(normal, vertex3(0,0,intensity)))

    def glBarycentricTriangle(self, intensity=1):        
        pointA = next(self.activeVertexArray)
        pointB = next(self.activeVertexArray)
        pointC = next(self.activeVertexArray)        

        if self.activeTex:
            texVertexAArray = next(self.activeVertexArray)
            texVertexBArray = next(self.activeVertexArray)
            texVertexCArray = next(self.activeVertexArray)

        normalA = next(self.activeVertexArray)
        normalB = next(self.activeVertexArray)
        normalC = next(self.activeVertexArray)

        minBBox, maxBBox = boundingBox(pointA, pointB, pointC)

        normal = vectorNormal(crossProduct(sub(pointB, pointA), sub(pointC, pointA)))
        grey = self.glShaderIntensity(normal, intensity)
        textureIntensity = dotProduct(normal, vertex3(0,0,intensity))

        if textureIntensity < 0:
            return

        for x in range(minBBox.x, maxBBox.x + 1):
            for y in range(minBBox.y, maxBBox.y + 1):
                b1, b2, b3 = barycentric(pointA, pointB, pointC, vertex2(x, y))

                if (b1 < 0) or (b2 < 0) or (b3 < 0):
                    continue                

                if self.activeTex:  
                    textureXPos = (texVertexAArray.x * b1) + (texVertexBArray.x * b2) + (texVertexCArray.x * b3)
                    textureYPos = (texVertexAArray.y * b1) + (texVertexBArray.y * b2) + (texVertexCArray.y * b3)

                    colour = self.activeShader(
                        self,
                        triangle=(pointA, pointB, pointC),
                        barycentricCoords=(b1, b2, b3),
                        textureCoords=(textureXPos, textureYPos),
                        varyingNormals=(normalA, normalB, normalC),
                        intensity=intensity
                    )

                    z = (pointA.z * b1) + (pointB.z * b2) + (pointC.z * b3)

                    if x < 0 or y < 0:
                        continue
                    try:
                        if z > self.zBuffer[y][x]:
                            self.glVertex(self.getNormXCoord(x), self.getNormYCoord(y), colour)
                            self.zBuffer[y][x] = z
                    except:
                        pass
                else:
                    if grey < 0:
                        continue

                    z = (pointA.z * b1) + (pointB.z * b2) + (pointC.z * b3)

                    if x < 0 or y < 0:
                        continue

                    colourGrey = self.activeShaderNoTexture(
                        self,                        
                        barycentricCoords=(b1, b2, b3),       
                        varyingNormals=(normalA, normalB, normalC),
                        intensity=intensity
                    )

                    try:
                        if z > self.zBuffer[y][x]:
                            self.glVertex(self.getNormXCoord(x), self.getNormYCoord(y), colourGrey)
                            self.zBuffer[y][x] = z
                    except:
                        pass
                        
    def glSetGouradShaderNoTexture(self, obj, **kwargs):
        b1, b2, b3 = kwargs['barycentricCoords']        
        normalA, normalB, normalC = kwargs['varyingNormals']

        normX = normalA.x * b1 + normalB.x * b2 + normalC.x * b3
        normY = normalA.y * b1 + normalB.y * b2 + normalC.y * b3
        normZ = normalA.z * b1 + normalB.z * b2 + normalC.z * b3

        vect = vertex3(normX, normY, normZ)

        textureColor = color(250, 214, 165) 
        textureIntensity = dotProduct(vect, vertex3(0,0,1))

        try:
            return color(
                int(textureColor[2] * textureIntensity) if (textureColor[0] * textureIntensity > 0) else 0,
                int(textureColor[1] * textureIntensity) if (textureColor[1] * textureIntensity > 0) else 0,
                int(textureColor[0] * textureIntensity) if (textureColor[2] * textureIntensity > 0) else 0
            )
        except:
            pass

    def glSetGouradShader(self, obj, **kwargs):
        b1, b2, b3 = kwargs['barycentricCoords']
        textureXPos, textureYPos = kwargs['textureCoords']
        textureColor = obj.activeTex.getTextureColor(textureXPos, textureYPos)
        normalA, normalB, normalC = kwargs['varyingNormals']

        intensityPointA, intensityPointB, intensityPointC = [
            dotProduct(normal, vertex3(0,0,kwargs['intensity'])) for normal in (normalA, normalB, normalC)
        ]

        textureIntensity = (b1*intensityPointA) + (b2*intensityPointB) + (b3*intensityPointC)

        try:
            return color(
                int(textureColor[2] * textureIntensity) if (textureColor[0] * textureIntensity > 0) else 0,
                int(textureColor[1] * textureIntensity) if (textureColor[1] * textureIntensity > 0) else 0,
                int(textureColor[0] * textureIntensity) if (textureColor[2] * textureIntensity > 0) else 0
            )
        except:
            pass

    def glFinish(self):
        f = open(self.filename, 'bw')

        # file header 14 bytes
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header 40 bytes
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # framebuffer data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()