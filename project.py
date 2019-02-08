"""
María Mercedes Retolaza Reyna, 16339
Gráficas por Computadora  
""" 
import libs 
import struct
import os 
from libs import Bitmap
from libs import word
from libs import getColor
from libs import randint


#Objet to draw 
img = None

#Constructor 
def glInit():
    return None

#Init FrameBuffer
def glCreateWindow(width, height):
    global img 
    img = Bitmap(width,height)
    return img 

#Delete actual image 
def glClear(): 
    img.clear()

#Image area can draw
def glViewPort(x,y,widht, height):
    img.viewPort(x,y,widht, height)

#Get Color 
def glColor(r,g,b):
    img.setColor(r,g,b)

#Init canvas with new color 
def glClearColor(r,g,b):
    img.clearColor(0,0,0) 

#Get new x,y points 
def glVertex(x,y):
    img.vertex(x,y)

#Show new image 
def glFinish():
    img.writeFile("img.bmp")

def menu(): 
    os.system('cls')
    print ('0. Salir')
    print('1. Por renderizar una imagen negra con un punto blanco en una ubicación random dentro de la imagen.')
    print('2. Por renderizar una imagen negra con un punto blanco en cada esquina')
    print('3. Por renderizar un cubo de 100 pixeles en el centro de su imagen')
    print('4. Por renderizar líneas blancas en toda la orilla de su imagen (4 lineas)')
    print('5. Por renderizar una línea blanca en diagonal por el centro de su imagen.')
    print('6. Por llenar su imagen entera de puntos blancos y negros (las posibilidades de que un punto sea blanco o negro son de 50%)')
    print ('7. Por llenar su imagen entera de puntos de colores random')
    print ('8. Por crear una escena de un cielo con estrellas ')
    print(' 9. Mostrar una escena de atari')
    

glCreateWindow(400,400)

option = True 
while option: 
    menu()
    menuOption = input("Ingresa una opción del menú  >> ")

    if menuOption == "1":
        print("----")
        input ("Has ingresado a la opción 1...\npulsa una tecla para continuar")
        glClearColor(0,0,0)
        glClear()
        glViewPort(0,0,300,300)
        glColor(255,255,255)
        glVertex(randint(-1, 1), randint(-1, 1))
        glFinish()

    elif menuOption == "2":
        print("----")
        input ("Has ingresado a la opción 2...\npulsa una tecla para continuar")
        glClearColor(0,0,0)
        glClear()
        glViewPort(0,0,399,399)
        glColor(255,255,255)
        glVertex(-1,1)
        glVertex(-1,-1)
        glVertex(1,-1)
        glVertex(1,1)
        glFinish()
    
    elif menuOption == "3":
        print("----")
        input ("Has ingresado a la opción 3...\npulsa una tecla para continuar")
        glClearColor(0,0,0)
        glClear()
        glViewPort(0,0,400,400)
        glColor(255,255,255)
        img.square(100)
        glFinish()
    
    elif menuOption == "4":
        print("----")
        input ("Has ingresado a la opción 4...\npulsa una tecla para continuar")
        glClearColor(0,0,0)
        glClear()
        glViewPort(0,0,400,400)
        glColor(255,255,255)
        img.drawLeftLine(10)
        img.drawRightLine(10)
        img.drawTopLine(10)
        img.drawBottonLine(10)
        glFinish()
    
    elif menuOption == "5":
        print("----")
        input ("Has ingresado a la opción 5...\npulsa una tecla para continuar")
        glClearColor(0,0,0)
        glClear()
        glViewPort(0,0,400,400)
        glColor(255,255,255)
        img.drawSlash()
        glFinish()
    
    elif menuOption == "6":
        print("----")
        input ("Has ingresado a la opción 6...\npulsa una tecla para continuar")
        glClearColor(0,0,0)
        glClear()
        glViewPort(0,0,400,400)
        glColor(255,255,255)
        img.random()
        glFinish()
    
    elif menuOption == "7":
        print("----")
        input ("Has ingresado a la opción 7...\npulsa una tecla para continuar")
        glClearColor(0,0,0)
        glClear()
        glViewPort(0,0,400,400)
        glColor(255,255,255)
        img.randomColor()
        glFinish()
    
    elif menuOption == "8":
        print("----")
        input ("Has ingresado a la opción 8...\npulsa una tecla para continuar")
        glClearColor(0,0,0)
        glClear()
        glViewPort(0,0,395,395)
        glColor(255,255,255)
        img.stars(200)
        glFinish()
    
    elif menuOption == "9":
        print("----")
        input("Has ingresado a la opción 9...\npulsa una tecla para continuar")
        glClearColor(0, 0, 0)
        glClear()
        glViewPort(0, 0, 160, 192)
        glColor(255, 255, 255)
        # ---------
        glVertex(0, 1)
        glVertex(0, 0.9)
        glVertex(0, 0.8)
        glVertex(0, 0.7)
        glVertex(0, 0.6)
        glVertex(0, 0.5)
        glVertex(0, 0.4)
        glVertex(0, 0.3)
        glVertex(0, 0.2)
        glVertex(0, 0.1)
        glVertex(0, 0)
        glVertex(0, -0.9)
        glVertex(0, -0.8)
        glVertex(0, -0.7)
        glVertex(0, -0.6)
        glVertex(0, -0.5)
        glVertex(0, -0.4)
        glVertex(0, -0.3)
        glVertex(0, -0.2)
        glVertex(0, -0.1)
        glVertex(0, -1)
        # ---------
        glVertex(-1, 0)
        glVertex(-1, 0.02)
        glVertex(-1, 0.04)
        glVertex(-1, 0.06)
        glVertex(-1, 0.08)
        glVertex(-1, 0.1)
        glVertex(-1, 0.12)
        glVertex(-1, 0.14)

        # ----------
        glVertex(1, 0)
        glVertex(1, 0.02)
        glVertex(1, 0.04)
        glVertex(1, 0.06)
        glVertex(1, 0.08)
        glVertex(1, 0.1)
        glVertex(1, 0.12)
        glVertex(1, 0.14)
        # -------------
        glVertex(0.5, 0.5)
        glFinish()

    elif menuOption == "0":
        break 
    else: 
        print("")
        input("No has ingresado ninguna opción correcta...\npulsa una tecla para continuar")