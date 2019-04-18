from srLibs import Bitmap
from textureLoader import textureLoader
from utils import vertex3

IMG = Bitmap('render.bmp')

def setUpRenderer():

    IMG.glInit()
    IMG.glCreateWindow(1920, 1080)
    IMG.glViewPort(0, 0, 1920, 1080)
    IMG.glClear(0.9, 0.8, 0.6)
    IMG.glColor(1, 0.8, 0.6)
    
def scene():

    setUpRenderer()

    # Fondo de imagen 
    t = textureLoader('canva/fondo.bmp')
    IMG.framebuffer = t.pixels

    IMG.glLookAt(
        vertex3(10, 25, 28), 
        vertex3(0, -0.2, 0), 
        vertex3(0, 1, 0)
    )

      # venado (objeto 0)
    obj = 'deer/deer.obj'
    translate = (-0.4, 0, 0)
    scale = (0.08, 0.12, 0.08)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando (Objeto 0):   ' + obj)

    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    
    # venado (objeto 1)
    obj = 'deer/deer.obj'
    translate = (0.60, 0, 0)
    scale = (0.08, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando (Objeto 1):   ' + obj)

    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # venado (objeto 2)
    obj = 'deer/deer.obj'
    translate = (-0.1, 0, 0)
    scale = (0.05, 0.08, 0.05)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando (Objeto 2):   ' + obj)

    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca (objeto 3)
    obj = 'stone/stone.obj'
    translate = (0.06, -1.2, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 3):   ' + obj)

    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca (objeto 3)
    obj = 'stone/stone.obj'
    translate = (0.70, -1.1, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 4):   ' + obj)

    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    
    # roca (objeto 3)
    obj = 'stone/stone.obj'
    translate = (-0.3, -0.3, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 5):   ' + obj)

    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca (Objeto 3)
    obj = 'stone/stone.obj'
    translate = (-0.4, -0.4, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 6):   ' + obj)
    
    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca (Objeto 3)
    obj = 'stone/stone.obj'
    translate = (0.1, 0.1, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 7):   ' + obj)
    
    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca (Objeto 3)
    obj = 'stone/stone.obj'
    translate = (0.2, 0.2, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Renderizando (Objeto 8):   ' + obj)
    
    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # base (Objeto 4)
    obj = 'base/base.obj'
    translate = (0, -1.2, 0)
    scale = (2, 1, 2)
    rotate = (0, 0, 0)
    intensity = 5   
    texture = textureLoader('base/base.bmp')
    print('Renderizando (Objeto 9):   ' + obj)
    
    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # dragon (Objeto 10)
    obj = 'dragon/dragon.obj'
    translate = (0.06, 0.4, -0.2)
    scale = (0.1, 0.1, 0.1)
    rotate = (0, 2, 10)
    intensity = 1    
    texture = textureLoader('dragon/dragon.bmp')
    print('Renderizando (Objeto 10):   ' + obj)
    
    IMG.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    IMG.glFinish()
    print('Puede revisar la escena final en:  \'render.bmp\'')
    

scene()
