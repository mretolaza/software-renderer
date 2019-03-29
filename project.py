from srLibs import Bitmap
from textureLoader import textureLoader
from utils import vertex3

GL = Bitmap('render.bmp')

def setUpRenderer():
    GL.glInit()
    GL.glCreateWindow(1920, 1080)
    GL.glViewPort(0, 0, 1920, 1080)
    GL.glClear(1, 1, 1)
    GL.glColor(1, 1, 1)

def medShot():
    obj = 'deer/deer.obj'
    translate = (1.5, 0.05, -0.2)
    scale = (0.15, 0.18, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando:   ' + obj + '\ntranslación:   ' + str(translate) + '\nescala:   ' + str(scale))
    print('Por favor espere un momento...')
    
    setUpRenderer()
    GL.glLookAt(
        vertex3(5, 1, 0), 
        vertex3(0, 0, 0), 
        vertex3(0, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    GL.glFinish()

    print('Puede verlo en la carpeta como:  \'render.bmp\'')

def dutchAngle():
    obj = 'deer/deer.obj'
    translate = (0, 0, 0)
    scale = (0.08, 0.16, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando:   ' + obj + '\ntranslación:   ' + str(translate) + '\nescala:   ' + str(scale))
    print('Por favor espere un momento...')

    setUpRenderer()
    GL.glLookAt(
        vertex3(5, 1, 0), 
        vertex3(0, 0, 0), 
        vertex3(0, 1, 0.13)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    GL.glFinish()

    print('Puede verlo en la carpeta:  \'render.bmp\'')

def lowShot():
    obj = 'deer/deer.obj'
    translate = (0, 0, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando:   ' + obj + '\ntranslación:   ' + str(translate) + '\nescala:   ' + str(scale))
    print('Por favor espere un momento...')
    
    setUpRenderer()
    GL.glLookAt(
        vertex3(10, -6.5, 5), 
        vertex3(0, -0.2, 0), 
        vertex3(0, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    GL.glFinish()

    print('Puede verlo en la carpeta:  \'render.bmp\'')

def highShot():
    obj = 'deer/deer.obj'
    translate = (0, 0, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando:   ' + obj + '\ntranslación:   ' + str(translate) + '\nescala:   ' + str(scale))
    print('Por favor espere un momento...')
    
    setUpRenderer()
    GL.glLookAt(
        vertex3(10, 25, 28), 
        vertex3(0, -0.2, 0), 
        vertex3(0, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    GL.glFinish()

    print('Puede verlo en la carpeta:  \'render.bmp\'')


#medShot()
#dutchAngle()
lowShot()
#highShot()
