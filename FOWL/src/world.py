from pyglet.gl import *
import math
from helper import LoadGLTextures



class World:
    worldTexture=None
    
    def __init__(self):
        self.radius = 15
        self.quadratic=gluNewQuadric()
        gluQuadricNormals(self.quadratic, GLU_SMOOTH)
        gluQuadricTexture(self.quadratic, GL_TRUE)
        self.texture = LoadGLTextures('../data/world.bmp')
        
    def draw(self):
        glTranslatef(0.0,0.0,-30)
        glBindTexture(self.texture.target, self.texture.id)
        gluSphere(self.quadratic,self.radius,32,32)


