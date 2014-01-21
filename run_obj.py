'''
Created on Dec 15, 2013

@author: Phil Williammee
'''
# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
 
# IMPORT OBJECT LOADER
from my_obj_loader import *

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
 
glLightfv(GL_LIGHT0, GL_POSITION,  (10, 10, 100, 0.0))
#glLightfv(GL_LIGHT0, GL_AMBIENT, (0.15, 0.15, 0.15, 1.0))
#glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
#glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded
 
# LOAD OBJECT AFTER PYGAME INIT
#obj = OBJ(sys.argv[1], swapyz=True)
cam = OBJ('cam_b.obj', swapyz=True)
drive = OBJ('drive_b.obj', swapyz=True)
plate = OBJ('plate_b.obj', swapyz=True)
drive_shaft = OBJ('drive_shaft_b.obj', swapyz=True)
cam_shaft = OBJ('cam_shaft_b.obj', swapyz=True)

clock = pygame.time.Clock()

glClearColor(0.2, 0.2, 0.2, 1)
glMatrixMode(GL_PROJECTION)

glLoadIdentity()
width, height = viewport
gluPerspective(45.0, width/float(height), 1, 1000.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
 
rx, ry = (0,0)
tx, ty = (0,0)
zpos = 20
rotate = move = False
angle = 0

while 1:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j
 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
 
    # RENDER OBJECT
    angle += 3
    if angle > 360:
        angle -=360
    glTranslate(tx+2.25, ty, - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glRotate(-135,1,0,0)
    
    glCallList(plate.gl_list)
    
    glPushMatrix()
    #glTranslate(4.5*math.cos(math.radians(angle))-4.5,0, -4.5*math.sin(math.radians(angle)))
    glTranslate(-4.5,0,0)
    glRotate(angle,0,1,0)  
    glTranslate(4.5,0,0) 
    #glTranslate(-4.5*math.cos(math.radians(angle))+4.5,0, 4.5*math.sin(math.radians(angle)))
    glCallList(drive.gl_list)
    glPopMatrix()
    offset = 30
    a = 2.25
    b = 4.5
    C = math.radians(60-angle)
    c= math.sqrt(math.pow(a,2)+math.pow(b,2)-2*a*b*math.cos(C))
    A = math.acos((math.pow(b, 2)+math.pow(c,2)-math.pow(a,2))/(2*b*c))
    A = math.degrees(A)+60
    #B = 180 - A -C
    
    glPushMatrix()
    if angle >=1 and angle < 60:
        glRotate(A-offset,0,1,0)
    if angle >=60 and angle < 120:
        glRotate(-A+offset,0,1,0)
    
    glCallList(cam.gl_list)
    glCallList(cam_shaft.gl_list)
    glPopMatrix()
    
    glCallList(drive_shaft.gl_list)

 
    pygame.display.flip()