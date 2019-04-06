import struct
from constants import color

class textureLoader(object):
    def __init__(self, filename):
        self.filename = filename
        self.read()

    def read(self):
       
        self.image = open(self.filename, 'rb')
        self.image.seek(10)
        self.header_size = struct.unpack('=l', self.image.read(4))[0]
        self.image.seek(18)

        self.width = struct.unpack("=l", self.image.read(4))[0]
        self.height = struct.unpack("=l", self.image.read(4))[0]
        self.framebuffer = []

        self.image.seek(self.header_size)

        for y in range(self.height):
            self.framebuffer.append([])

            for x in range(self.width):
                blue = ord(self.image.read(1))
                green = ord(self.image.read(1))
                red = ord(self.image.read(1))

                self.framebuffer[y].append(color(red, green, blue))

        self.image.close()

    def getTextureColor(self, texXPosition, texYPosition, intensity = 1):
        xCoord = int(texXPosition * self.width)
        yCoord = int(texYPosition * self.height)

        try:
            return bytes(
            map(
                lambda tex: round(tex * intensity) if tex * intensity > 0 else 0, self.framebuffer[yCoord][xCoord]
            )
        )
        except:
            pass