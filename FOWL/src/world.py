from pyglet.gl import *
import math
from helper import LoadGLTextures
import ctypes
import sys
from math import sin,cos
from pyglet import window
from pyglet import clock
from pyglet import font

LightAmbient = [ 0.5, 1.0, 0.5, 1.0 ]
LightDiffuse = [ 1.0, 1.0, 1.0, 1.0 ]
LightPosition = [ -50.0, 0.0, 2.0, 1.0 ]


light_position = [ -1.0, 0.5, 6.0, 0.0 ]
mat_ambient = [ 0.8, 0, 0, 1.0 ]
mat_diffuse = [ 0.9, 0.7, 0.1, 1.0 ]
mat_specular = [ 1.0, 1.0, 1.0, 1.0 ]
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

    def rotate(self, new_rotx, new_roty):
        #print "NRX: ", new_rotx, "NRY: ", new_roty

        glPushMatrix()

        glLoadIdentity()
        glRotatef(new_rotx, 1,0,0)
        x_rot_matrix = (ctypes.c_double*16)()
        glGetDoublev( GL_MODELVIEW_MATRIX, x_rot_matrix )

        glLoadIdentity()
        glRotatef(new_roty, 0,1,0)
        y_rot_matrix = (ctypes.c_double*16)()
        glGetDoublev( GL_MODELVIEW_MATRIX, y_rot_matrix )

        glLoadIdentity()
        glMultMatrixf( (ctypes.c_float*16)(*x_rot_matrix) )
        glMultMatrixf( (ctypes.c_float*16)(*y_rot_matrix) )
        temp_rot_matrix = (ctypes.c_double*16)()
        glGetDoublev( GL_MODELVIEW_MATRIX, temp_rot_matrix )

        glLoadIdentity()

        if (self.oldRotationMatrix):
            # load the old matrix
            glMultMatrixf( (ctypes.c_float*16)(*self.oldRotationMatrix) )

        glMultMatrixf( (ctypes.c_float*16)(*temp_rot_matrix) )

        # save the rotation matrix
        self.oldRotationMatrix = (ctypes.c_double*16)()
        glGetDoublev( GL_MODELVIEW_MATRIX, self.oldRotationMatrix )
        
        glPopMatrix()

    def draw(self):

        glLoadIdentity()
        glTranslatef(0,0,-40)
        
        # rotate by the new values
        glRotatef(self.rotx, 1,0,0)
        glRotatef(self.roty, 0,1,0)
        glRotatef(self.rotz, 0,0,1)

        # rotate with save matrix
        if (self.oldRotationMatrix):
            glMultMatrixf( (ctypes.c_float*16)(*self.oldRotationMatrix) )
        

        glShadeModel(GL_SMOOTH)               # Enable Smooth Shading

        glEnable(GL_DEPTH_TEST)               # Enables Depth Testing
        glDepthFunc(GL_LEQUAL)       
        
        glLightfv ( GL_LIGHT0, GL_POSITION,
                    (GLfloat * len(light_position))(*light_position))
        glEnable ( GL_LIGHTING );
        glEnable ( GL_LIGHT0 );
        glShadeModel ( GL_SMOOTH );
        glMaterialfv ( GL_FRONT, GL_AMBIENT,
                       (GLfloat * len(mat_ambient))(*mat_ambient))
        glMaterialfv ( GL_FRONT, GL_DIFFUSE,
                       (GLfloat * len(mat_diffuse))(*mat_diffuse) )
        
        glMaterialfv ( GL_FRONT, GL_SPECULAR,
                       (GLfloat * len(mat_specular))(*light_position))
        glMaterialfv ( GL_FRONT, GL_SHININESS,
                       (GLfloat * len(mat_shininess))(*mat_shininess ))

 

        glDisable(GL_TEXTURE_2D)

        glColor3f(0,1,0)
        gluSphere(self.quadratic,self.radius,32,32)
        gluCylinder(self.quadratic,1,1,20,32,32)
        glRotatef(-90,0,1,0)
        gluCylinder(self.quadratic,1,1,20,32,32)
        glEnable(GL_TEXTURE_2D)

