from srLibs import Bitmap
from textureLoader import textureLoader
from utils import vertex3

GL = Bitmap('render.bmp')

def setUpRenderer():
    GL.glInit()
    GL.glCreateWindow(1920, 1080)
    GL.glViewPort(0, 0, 1920, 1080)
    GL.glClear(0.9, 0.8, 0.6)
    GL.glColor(1, 0.8, 0.6)
    
def scene():

    setUpRenderer()
    GL.glLookAt(
        vertex3(10, 25, 28), 
        vertex3(0, -0.2, 0), 
        vertex3(0, 1, 0)
    )
    
    # venado (objeto 1)
    obj = 'deer/deer.obj'
    translate = (0.60, 0, 0)
    scale = (0.08, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando (Objeto 1):   ' + obj)

    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # venado (objeto 2)
    obj = 'deer/deer.obj'
    translate = (-0.5, 0, 0)
    scale = (0.08, 0.15, 0.08)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando (Objeto 2):   ' + obj)

    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

     # roca (objeto 3)
    obj = 'stone/stone.obj'
    translate = (0.60, -1.2, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 3):   ' + obj)

    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

     # roca (objeto 3)
    obj = 'stone/stone.obj'
    translate = (0.70, -1.1, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 3):   ' + obj)

    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    
    # roca (objeto 3)
    obj = 'stone/stone.obj'
    translate = (-0.3, -0.3, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 3):   ' + obj)

    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca (Objeto 3)
    obj = 'stone/stone.obj'
    translate = (-0.4, -0.4, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 3):   ' + obj)
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca (Objeto 3)
    obj = 'stone/stone.obj'
    translate = (0.1, 0.1, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 3):   ' + obj)
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca (Objeto 3)
    obj = 'stone/stone.obj'
    translate = (0.2, 0.2, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 3):   ' + obj)
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    GL.glFinish()

    print('Puede revisar la escena final en:  \'render.bmp\'')

scene()