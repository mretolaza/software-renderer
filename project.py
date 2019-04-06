from srLibs import Bitmap
from textureLoader import textureLoader
from utils import vertex3

GL = Bitmap('lab.bmp')

def setUprRender():
    GL.glInit()
    GL.glCreateWindow(1920, 1080)
    GL.glViewPort(0, 0, 1920, 1080)
    GL.glClear(0, 0, 0)
    GL.glColor(1, 1, 1)

def render():

    obj = 'planet/planet.obj'
    translate = (0, 0, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1        
    print('Renderizando:   ' + obj + '\ntraslación:   ' + str(translate) + '\nescala:   ' + str(scale))
    print('Por favor aguarde...')
    
    setUprRender()
    GL.glLookAt(
        vertex3(20, 1, 20), 
        vertex3(0, 0, 0), 
        vertex3(0, 1, 0)
    )

    GL.createStarsInCanva()

    GL.renderIs = 'planet'
    GL.glLoadObj(obj, translate, scale, rotate, intensity)

   
    obj = 'planet/moon.obj'
    translate = (0.8, 0.3, 0)
    scale = (0.02, 0.03, 0.02)
    rotate = (0, 0, 0)
    intensity = 1        
    print('Renderizando:   ' + obj + '\ntraslación:   ' + str(translate) + '\nescala:   ' + str(scale))
    print('Por favor aguarde...')

    GL.renderIs = 'moon'
    GL.glLoadObj(obj, translate, scale, rotate, intensity)

    
    obj = 'planet/moon.obj'
    translate = (0.7, -0.3, 0)
    scale = (0.015, 0.008, 0.01)
    rotate = (0, 0, 5)
    intensity = 1        
    print('Renderizando:   ' + obj + '\ntraslación:   ' + str(translate) + '\nescala:   ' + str(scale))
    print('Por favor aguarde...')

    GL.renderIs = 'moon'
    GL.glLoadObj(obj, translate, scale, rotate, intensity)

    GL.glFinish()

    print('Ver imagen en carpeta:  \'lab.bmp\'')

render()
