#!/usr/bin/env python

from pyglet import window
from pyglet import clock
from pyglet import font
import random
import math

from bird import Bird
from pyglet.gl import *
from world import World
import sys
from enemy import Enemy

def vec(*args):
    return (GLfloat * len(args))(*args)

LightAmbient = [ 1.0, 1.0, 1.0, 1.0 ]
LightDiffuse = [ 1.0, 1.0, 1.0, 1.0 ]
LightPosition = [ 0.0, 0.0, -10.0, 1.0 ]

mat_shininess = [ 5.0 ]

class MainWindow(window.Window):

    def __init__(self, *args, **kwargs):
        #Let all of the standard stuff pass through
        window.Window.__init__(self, *args, **kwargs)
        self.initGL()
        self.bird = Bird()
        self.world = World()
        self.enemy = Enemy()

    def initGL(self):

        glClearColor(0.0, 0.0, 0.0, 0.0)        # This Will Clear The Background Color To Black
        glClearDepth(1.0)                                       # Enables Clearing Of The Depth Buffer
        glDepthFunc(GL_LESS)                            # The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)                         # Enables Depth Testing
        glShadeModel(GL_SMOOTH)                         # Enables Smooth Color Shading
        
        glEnable(GL_TEXTURE_2D)               # Enable Texture Mapping
        glShadeModel(GL_SMOOTH)               # Enable Smooth Shading
        glClearColor(0.0, 0.0, 0.0, 0.5)      # Black Background
        glClearDepth(1.0)                     # Depth Buffer Setup
        glEnable(GL_DEPTH_TEST)               # Enables Depth Testing
        glDepthFunc(GL_LEQUAL)                # The Type Of Depth Testing To Do
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST) # Really Nice Perspective Calculations
        
        glLightfv(GL_LIGHT1, GL_AMBIENT, vec(*LightAmbient))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(*LightDiffuse))
        glLightfv(GL_LIGHT1, GL_POSITION, vec(*LightPosition))
        glEnable(GL_LIGHT1)
        
        glColor4f(1.0,1.0,1.0,0.5)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)

    def rotate_world(self):
        # know bird.roty is off of (1,0)
        ref_angle = self.bird.roty
        
        point1=0
        if (ref_angle >= 0 and ref_angle<=90):
            point1 = math.atan(ref_angle * math.pi/180.0)
        elif (ref_angle >= 90 and ref_angle<=180):
            point1 = math.atan((180-ref_angle) * math.pi/180.0)
        elif (ref_angle >= 180 and ref_angle<=270):
            point1 = -math.atan((ref_angle-180) * math.pi/180.0)
        else:
            point1 = math.atan((ref_angle) * math.pi/180.0)

        point2=0
        if (ref_angle >= 0 and ref_angle<=90):
            point2 = math.atan((90-ref_angle) * math.pi/180.0)
        elif (ref_angle >= 90 and ref_angle<=180):
            point2 = math.atan((90.0-ref_angle) * math.pi/180.0)
        elif (ref_angle >= 180 and ref_angle<=270):
            point2 = math.atan((ref_angle-270) * math.pi/180.0)
        else:
            # between -90 and 0
            point2 = math.atan((ref_angle+90) * math.pi/180.0)

        self.world.rotate(1, point2, -point1)
        
    def animate_bird(self, interval):
        self.bird.flap()
        self.rotate_world()
        self.enemy.move(45)

    def update(self):
        pass

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glPushMatrix()
        self.world.draw()
        glPopMatrix()

        glPushMatrix()
        self.bird.draw()
        glPopMatrix()
        
        glPushMatrix()
        self.enemy.draw()
        glPopMatrix()
        
        
    def main_loop(self):
        clock.set_fps_limit(30)
        clock.schedule_interval(self.animate_bird, 0.01)
        
        while not self.has_exit:
            self.dispatch_events()
            self.clear()
        
            self.update()
            self.draw()
        
            #Tick the clock
            clock.tick()
            self.flip()


    
    """******************************************
    Event Handlers
    *********************************************"""
    def on_mouse_motion(self, x, y, dx, dy):
        new_dest_x = (float(x - self.width/2.0) / (self.width/2.0))*4.0
        new_dest_y = (float(y - self.height/2.0) / (self.height/2.0))*4.0
        old_dest_x = 0
        old_dest_y = 0

        y_rot = old_dest_y - new_dest_y
        x_rot = old_dest_x - new_dest_x

        if (y_rot != 0 and new_dest_y < old_dest_y):
            new_roty_dest = 180 + 1.0 * math.atan((x_rot) /
                                    (y_rot)) * 180.0/math.pi
        elif (y_rot != 0):
            new_roty_dest = 1.0 * math.atan((x_rot) /
                            (y_rot)) * 180.0/math.pi

        old_dest_x = self.bird.dest_x
        old_dest_y = self.bird.dest_y

        if (old_dest_x < 0 and new_dest_x < 0):
            if (old_dest_y <= 0 and new_dest_y>=0):
                new_roty_dest = -90
                self.bird.roty = -90
            elif (old_dest_y >=0 and new_dest_y<=0):
                new_roty_dest = 270
                self.bird.roty = 270
            
        if (y_rot):
            self.bird.roty_dest=new_roty_dest
            

        self.bird.dest_x = new_dest_x
        self.bird.dest_y = new_dest_y
        
        if (self.world.oldRotationMatrix):
            self.world.resetMatrix = self.world.oldRotationMatrix


    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

if __name__ == "__main__":
    # Someone is launching this directly
    main = MainWindow()
    main.main_loop()

