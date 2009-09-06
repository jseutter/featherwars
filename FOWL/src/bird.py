from pyglet.gl import *
from helper import LoadGLTextures

class Bird:
    birdTexture=None
    
    def __init__(self):
        global birdTexture
        self.x = 0
        self.y = 0
        self.z = 0
        self.rotx = -90
        self.roty = 0
        self.rotz = 0
        self.gllist = -1
        self.quadratic=gluNewQuadric()
        gluQuadricNormals(self.quadratic, GLU_SMOOTH)
        gluQuadricTexture(self.quadratic, GL_TRUE)
        self.wingAngle=0
        self.wing_inc=5
        self.wing_inc_const=10
        self.y_inc = 0
        self.y_inc_const = 0.1
        self.dest_x=0
        self.dest_y=0
        self.roty_dest = 0        
        self.texture = LoadGLTextures('../data/crate.bmp')

        
    def drawBird(self):
        glBindTexture(self.texture.target, self.texture.id)
        gluCylinder(self.quadratic,0.1,0.0,0.3,32,32)
        glTranslatef(0.0,0.0,-0.1)
        gluSphere(self.quadratic,0.2,32,32)
        
        glTranslatef(0.0,0.0,-0.7)
        gluCylinder(self.quadratic,0.1,0.15,0.6,32,32)
        glPushMatrix()
        glRotatef(-self.wingAngle,0,0,1)
        glRotatef(-90,0,1,0)
        glTranslatef(0.3,0.0,0.0)
        glScalef(1, 0.5, 1)
        gluCylinder(self.quadratic,0.1,0.15,0.6,32,32)
        glPopMatrix()

        glPushMatrix()
        glRotatef(self.wingAngle,0,0,1)
        glRotatef(90,0,1,0)
        glTranslatef(-0.3,0.0,0.0)
        glScalef(1, 0.5, 1)

        gluCylinder(self.quadratic,0.1,0.15,0.6,32,32)
        glPopMatrix()

    def draw(self):
        
        glTranslatef(self.x,self.y,-10.0)
        glRotatef(self.rotx, 1,0,0)
        glRotatef(self.roty, 0,1,0)
        glRotatef(self.rotz, 0,0,1)

        self.drawBird()

    def flap(self):
        if (self.wingAngle > 45):
            self.wing_inc = -self.wing_inc_const
        if (self.wingAngle < -45):
            self.wing_inc = self.wing_inc_const
            
        self.wingAngle = self.wingAngle + self.wing_inc

        self.move()

    def move(self):

        if (self.roty < self.roty_dest):
            self.roty += 10

        if (self.roty > self.roty_dest):
            self.roty -= 10
