from srLibs import Bitmap
from textureLoader import textureLoader
from utils import vertex3

GL = Bitmap('render.bmp')

def setUpRenderer():
    GL.glInit()
    GL.glCreateWindow(1920, 1080)
    GL.glViewPort(0, 0, 1920, 1080)
    GL.glClear(0, 0, 0)
    GL.glColor(1, 1, 1)
   

def scene():

    # venado
    obj = 'deer/deer_normals.obj'
    translate = (-0.5, 0, 0)
    scale = (0.08, 0.15, 0.08)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('deer/deer.bmp')
    print('Renderizando:   ' + obj + '\ntraslación:   ' + str(translate) + '\nescala:   ' + str(scale))
    print('Por favor espere...')

    setUpRenderer()
    GL.glLookAt(
        vertex3(10, 25, 28), 
        vertex3(0, -0.2, 0), 
        vertex3(0, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    
    # roca
    obj = 'stone/stone.obj'
    translate = (-0.3, -0.3, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca
    obj = 'stone/stone.obj'
    translate = (-0.4, -0.4, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca
    obj = 'stone/stone.obj'
    translate = (0, 0, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # roca
    obj = 'stone/stone.obj'
    translate = (0.1, 0.1, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = textureLoader('stone/stone.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

  
  


  
  

   

  
  
  
   
    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

scene()
