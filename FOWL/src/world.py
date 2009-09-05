from pyglet.gl import *
import math
from helper import LoadGLTextures
import ctypes
import sys

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

        # rotate by the new values
        #glRotatef(new_rotx, 1,0,0)
        #glRotatef(new_roty, 0,1,0)
        #glRotatef(self.rotz, 0,0,1)
        glMultMatrixf( (ctypes.c_float*16)(*temp_rot_matrix) )

        # save the rotation matrix
        self.oldRotationMatrix = (ctypes.c_double*16)()
        glGetDoublev( GL_MODELVIEW_MATRIX, self.oldRotationMatrix )

        #import sys
        #for i in range(0, 16):
        #    sys.stdout.write("%s," %(self.oldRotationMatrix[i]))
        #sys.stdout.write("\n")

        glPopMatrix()
        # get original sphere transform matrix
        #var tempMatrix:Matrix3D = sphere.transform;
        
        # create the rotation Matrixes for each local rotation axis given the corresponding X & Y
        # distances where the user rolled over on the surface of the sphere
        # Note: The value passed to Matrix3D.rotationX() should really be radians but I'm just using the x & y values 
        # divided by rotSpeedRatio which is a constant to bring the values down to "radiany" magnitudes 
        # and thus decrease the speed of the rotation. this will have to be the variable to work with 
        #when I implement the slowing down of the rotation.
        ##var rotX:Matrix3D = Matrix3D.rotationX(-[mouse Y here]/[rotSpeedRatio]);
        ##var rotY:Matrix3D = Matrix3D.rotationY(-[mouse X here]/[rotSpeedRatio]);

        #Mix both Matrixes together
        ##var rotResult:Matrix3D = Matrix3D.multiply(rotX,rotY);
        #Apply (Multiply) the final transform matrix to the original one and assign it to the sphere transform
        ##sphere.transform = Matrix3D.multiply(rotResult,tempMatrix);
        #pass
    
    def draw(self):
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(0.0,0.0,-30)

        # rotate with save matrix
        if (self.oldRotationMatrix):
            glMultMatrixf( (ctypes.c_float*16)(*self.oldRotationMatrix) )

        glBindTexture(self.texture.target, self.texture.id)
        gluSphere(self.quadratic,self.radius,32,32)
        glPopMatrix()

