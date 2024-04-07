import pygame as pg
from OpenGL.GL import *

pg.init()
pg.display.set_mode((640,480), pg.OPENGL|pg.DOUBLEBUF)

glClearColor(0.1, 0.2, 0.2, 1)
glEnable(GL_BLEND)
glEnable(GL_DEPTH_TEST)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 

pg.quit()