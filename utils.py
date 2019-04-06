from collections import namedtuple
import numpy as np
import math

vertex2 = namedtuple('Point2', ['x', 'y'])
vertex3 = namedtuple('Point3', ['x', 'y', 'z'])
pointP = -1, -1, -1

def sum(v1, v2):
    return vertex3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def sub(v1, v2):
    return vertex3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def scalarMult(v1, k):
    return vertex3(v1.x * k, v1.y * k, v1.z *k)

def dotProduct(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def crossProduct(v1, v2):
    return vertex3(
        v1.y * v2.z - v1.z * v2.y, 
        v1.z * v2.x - v1.x * v2.z, 
        v1.x * v2.y - v1.y * v2.x
    )

def vecLength(v1):
    return (v1.x**2 + v1.y**2 + v1.z**2)**0.5

def vectorNormal(v1):
    length = vecLength(v1)

    if not length:
        return vertex3(0, 0, 0)
    else:
        return vertex3(v1.x/length, v1.y/length, v1.z/length)
#Ingreso de A , B , C en formato de vertices 
def boundingBox(*vertices):
    xCoords = [ v.x for v in vertices ]
    yCoords = [ v.y for v in vertices ]
    xCoords.sort()
    yCoords.sort()

    return vertex2(xCoords[0], yCoords[0]), vertex2(xCoords[-1], yCoords[-1])

# vertex = v 
# translate = t 
# scale = s 
def transform(v, t=(0,0,0), s=(1,1,1)):
    # retorna el vertex 3 trasladado y transformado 
    param1 = round((v[0] + t[0]) * s[0])
    param2 = round((v[1] + t[1]) * s[1])
    param3 = round((v[2] + t[2]) * s[2])
    return vertex3(param1, param2, param3 )

def matrixTransform(v, viewPort, projection, view, model):
    augmentedVertexMatrix = [ [v.x], [v.y], [v.z], [1] ]
    transformedVertexMatrix = matrixMult(
        matrixMult(
            matrixMult(
                matrixMult(
                    viewPort, 
                    projection
                ), 
            view),
        model), 
        augmentedVertexMatrix
    )    
    transformedVertexMatrix = [
        round(transformedVertexMatrix[0][0] / transformedVertexMatrix[3][0]),
        round(transformedVertexMatrix[1][0] / transformedVertexMatrix[3][0]),
        round(transformedVertexMatrix[2][0] / transformedVertexMatrix[3][0])
    ]
    return vertex3(*transformedVertexMatrix)

def matrixMult(A, B):
    res = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]    

    for i in range(len(A)):        
        for j in range(len(B[0])):
            for k in range(len(B)):
                res[i][j] += A[i][k] * B[k][j]
    return res

def barycentric(vecA, vecB, vectC, P):
    b = crossProduct(
        vertex3(vectC.x - vecA.x, vecB.x - vecA.x, vecA.x - P.x), 
        vertex3(vectC.y - vecA.y, vecB.y - vecA.y, vecA.y - P.y)
    )

    if abs(b[2]) < 1:
        return pointP
    else:
        return (1 - (b[0] + b[1]) / b[2], b[1] / b[2], b[0] / b[2])

def getBaryCoords(vecA, vecB, vectC, minBBox, maxBBox):
    transform = np.linalg.inv(
        [
            [   vecA.x,      vecB.x,    vectC.x],
            [   vecA.y,      vecB.y,    vectC.y],
            [         1,          1,          1]
        ]
    )

    bboxGrid = np.mgrid[
        minBBox.x:maxBBox.x,
        minBBox.y:maxBBox.y
    ].reshape(2, -1)
    bboxGrid = np.vstack((bboxGrid, np.ones((1, bboxGrid.shape[1]))))
    
    return np.transpose(np.dot(transform, bboxGrid))