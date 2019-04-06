from srLibs import Bitmap
from textureLoader import textureLoader
from utils import vertex3

GL = Bitmap('render.bmp')

def renderer():
    GL.glInit()
    GL.createWindow(1920, 1080)
    GL.viewPort(0, 0, 1920, 1080)
    GL.clear(0, 0, 0)
    GL.color(1, 1, 1)

def render():

    obj = 'planet/planet.obj'
    translate = (0, 0, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1        
    print('Renderizando:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Generando...')
    
    renderer()
    GL.lookAt(
        vertex3(20, 1, 20), 
        vertex3(0, 0, 0), 
        vertex3(0, 1, 0)
    )

    GL.drawStars()

    GL.renderIs = 'planet'
    GL.loadObj(obj, translate, scale, rotate, intensity)

    obj = 'planet/moon.obj'
    translate = (0.8, 0.3, 0)
    scale = (0.02, 0.03, 0.02)
    rotate = (0, 0, 0)
    intensity = 1        
    print('Renderizando:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Generando...')

    GL.renderIs = 'moon'
    GL.loadObj(obj, translate, scale, rotate, intensity)

    obj = 'planet/moon.obj'
    translate = (0.7, -0.3, 0)
    scale = (0.015, 0.008, 0.01)
    rotate = (0, 0, 5)
    intensity = 1        
    print('Renderizando:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Generando...')

    GL.renderIs = 'moon'
    GL.loadObj(obj, translate, scale, rotate, intensity)

    GL.writeFile()

    print('Ver imagen en:  \'render.bmp\'')

render()
