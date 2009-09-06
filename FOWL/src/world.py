from pyglet.gl import *
import math
from helper import LoadGLTextures
import ctypes
import sys
from math import sin,cos
from pyglet import window
from pyglet import clock
from pyglet import font

light_position = [ -1.0, 0.5, 6.0, 0.0 ]
mat_ambient = [ 0.8, 0.3, 0.3, 1.0 ]
mat_diffuse = [ 0.9, 0.7, 0.1, 1.0 ]
mat_specular = [ 0.9, 0.9, 0.9, 1.0 ]
mat_shininess = [ 50.0 ]

def vec(*args):
    return (GLfloat * len(args))(*args)


class World:
    worldTexture=None
    
    def __init__(self):
        self.radius = 15
        self.rotx=0
        self.roty=0
        self.rotz=0
        self.quadratic=gluNewQuadric()
        gluQuadricNormals(self.quadratic, GLU_SMOOTH)
        gluQuadricTexture(self.quadratic, GL_TRUE)
        self.texture = LoadGLTextures('../data/world.bmp')
        self.resetMatrix = None
        self.oldRotationMatrix = None
        self.resetMatrix = None

    def rotate(self, angle, new_rotx, new_roty):
        glPushMatrix()

        glLoadIdentity()
        glRotatef(angle, new_rotx, new_roty, 0)
        
        if (self.oldRotationMatrix):
            # load the old matrix
            glMultMatrixf( (ctypes.c_float*16)(*self.oldRotationMatrix) )

        # save the rotation matrix
        self.oldRotationMatrix = (ctypes.c_double*16)()
        glGetDoublev( GL_MODELVIEW_MATRIX, self.oldRotationMatrix )
        
        glPopMatrix()

    def setupLights(self):
        # rotate with save matrix
        if (self.oldRotationMatrix):
            glMultMatrixf( (ctypes.c_float*16)(*self.oldRotationMatrix) )
            

        glShadeModel(GL_SMOOTH)               # Enable Smooth Shading

        glEnable(GL_DEPTH_TEST)               # Enables Depth Testing
        glDepthFunc(GL_LEQUAL)       
        
        glLightfv ( GL_LIGHT0, GL_POSITION,
                    (GLfloat * len(light_position))(*light_position))
        glEnable ( GL_LIGHTING )
        glEnable ( GL_LIGHT0 )
        glShadeModel ( GL_SMOOTH )
        glMaterialfv ( GL_FRONT, GL_AMBIENT,
                       (GLfloat * len(mat_ambient))(*mat_ambient))
        glMaterialfv ( GL_FRONT, GL_DIFFUSE,
                       (GLfloat * len(mat_diffuse))(*mat_diffuse) )
        
        glMaterialfv ( GL_FRONT, GL_SPECULAR,
                       (GLfloat * len(mat_specular))(*light_position))
        glMaterialfv ( GL_FRONT, GL_SHININESS,
                       (GLfloat * len(mat_shininess))(*mat_shininess ))

 

    def draw(self):

        glLoadIdentity()
        glTranslatef(0,0,-40)
        
        # rotate by the new values
        glRotatef(self.rotx, 1,0,0)
        glRotatef(self.roty, 0,1,0)
        glRotatef(self.rotz, 0,0,1)

        self.setupLights()

        glBindTexture(self.texture.target, self.texture.id)
        #glDisable(GL_TEXTURE_2D)
        glColor3f(0,1,0)
        gluSphere(self.quadratic,self.radius,32,32)
        #glEnable(GL_TEXTURE_2D)

