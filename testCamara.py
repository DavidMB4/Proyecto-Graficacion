import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluSphere, gluCylinder
from PIL import Image
import sys
import math

def load_texture(filename):
    """Carga una textura desde un archivo de imagen"""
    img = Image.open(filename)
    img = img.convert("RGB")  # Asegúrate de que la imagen esté en formato RGB
    img_data = img.tobytes("raw", "RGB", 0, -1)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    return texture_id


def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad
    glEnable(GL_TEXTURE_2D) 
    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1, 6, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)



def hierba_pasto():
    glBegin(GL_TRIANGLES)
    glColor3f(0.13, 0.55, 0.13)  # Rojo brillante

    glVertex3f(0.05,0.1,0.05 )
    glVertex3d(0.1, 0.4, 0.05)
    glVertex3d(0.15,0.1,0.05)
    glEnd()


def scale_vertex(vertex):
    factor=1
    return tuple(coord * factor for coord in vertex)


def patas_pollito():
    glColor3f(1.0, 1.0, 0.0)  # Amarillo
    #P1
    glVertex3f(*scale_vertex((0,0,0)))
    glVertex3f(*scale_vertex((0,0.1,0)))
    glVertex3f(*scale_vertex((0.3,0.1,0)))
    glVertex3f(*scale_vertex((0.3,0,0)))

    #P2
    glVertex3f(*scale_vertex((0,0.1,0)))
    glVertex3f(*scale_vertex((0.3,0.1,0)))
    glVertex3f(*scale_vertex((0.3,0.1,0.3)))
    glVertex3f(*scale_vertex((0,0.1,0.3)))

    #p3
    glVertex3f(*scale_vertex((0,0.1,0.1)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.1)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.2)))
    glVertex3f(*scale_vertex((0,0.1,0.2)))

    #p4
    glVertex3f(*scale_vertex((0.3,0,0)))
    glVertex3f(*scale_vertex((0.3,0.1,0)))
    glVertex3f(*scale_vertex((0.3,0.1,0.3)))
    glVertex3f(*scale_vertex((0.3,0,0.3)))

    #P5
    glVertex3f(*scale_vertex((0.3,0,0.3)))
    glVertex3f(*scale_vertex((0.3,0.1,0.3)))
    glVertex3f(*scale_vertex((0,0.1,0.3)))
    glVertex3f(*scale_vertex((0,0,0.3)))
    
    #P6
    glVertex3f(*scale_vertex((0,0,0.3)))
    glVertex3f(*scale_vertex((0,0.1,0.3)))
    glVertex3f(*scale_vertex((0,0.1,0)))
    glVertex3f(*scale_vertex((0,0,0)))

    #P7
    glVertex3f(*scale_vertex((0,0,0.1)))
    glVertex3f(*scale_vertex((0,0.1,0.1)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.1)))
    glVertex3f(*scale_vertex((-0.1,0,0.1)))

    #p8
    glVertex3f(*scale_vertex((-0.1,0,0.1)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.1)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.2)))
    glVertex3f(*scale_vertex((-0.1,0,0.2)))

    #p9
    glVertex3f(*scale_vertex((-0.1,0,0.2)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.2)))
    glVertex3f(*scale_vertex((0,0.1,0.2)))
    glVertex3f(*scale_vertex((0,0,0.2)))

    #p10
    glVertex3f(*scale_vertex((0.3,0.1,0.1)))
    glVertex3f(*scale_vertex((0.3,0.5,0.1)))
    glVertex3f(*scale_vertex((0.2,0.5,0.1)))
    glVertex3f(*scale_vertex((0.2,0.1,0.1)))

    #p11
    glVertex3f(*scale_vertex((0.2,0.1,0.1)))
    glVertex3f(*scale_vertex((0.2,0.5,0.1)))
    glVertex3f(*scale_vertex((0.2,0.5,0.2)))
    glVertex3f(*scale_vertex((0.2,0.1,0.2)))

    #p12
    glVertex3f(*scale_vertex((0.2,0.1,0.2)))
    glVertex3f(*scale_vertex((0.2,0.5,0.2)))
    glVertex3f(*scale_vertex((0.3,0.5,0.2)))
    glVertex3f(*scale_vertex((0.3,0.1,0.2)))

    #p13
    glVertex3f(*scale_vertex((0.3,0.1,0.2)))
    glVertex3f(*scale_vertex((0.3,0.5,0.2)))
    glVertex3f(*scale_vertex((0.3,0.5,0.1)))
    glVertex3f(*scale_vertex((0.3,0,0.1)))


    #Pata Duplicada 
    #P1
    glVertex3f(*scale_vertex((0,0,0.35)))
    glVertex3f(*scale_vertex((0,0.1,0.35)))
    glVertex3f(*scale_vertex((0.3,0.1,0.35)))
    glVertex3f(*scale_vertex((0.3,0,0.35)))

    #P2
    glVertex3f(*scale_vertex((0,0.1,0.35)))
    glVertex3f(*scale_vertex((0.3,0.1,0.35)))
    glVertex3f(*scale_vertex((0.3,0.1,0.65)))
    glVertex3f(*scale_vertex((0,0.1,0.65)))

    #p3
    glVertex3f(*scale_vertex((0,0.1,0.45)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.45)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.55)))
    glVertex3f(*scale_vertex((0,0.1,0.55)))

    #p4
    glVertex3f(*scale_vertex((0.3,0,0.35)))
    glVertex3f(*scale_vertex((0.3,0.1,0.35)))
    glVertex3f(*scale_vertex((0.3,0.1,0.65)))
    glVertex3f(*scale_vertex((0.3,0,0.65)))

    #P5
    glVertex3f(*scale_vertex((0.3,0,0.65)))
    glVertex3f(*scale_vertex((0.3,0.1,0.65)))
    glVertex3f(*scale_vertex((0,0.1,0.65)))
    glVertex3f(*scale_vertex((0,0,0.65)))
    
    #P6
    glVertex3f(*scale_vertex((0,0,0.65)))
    glVertex3f(*scale_vertex((0,0.1,0.65)))
    glVertex3f(*scale_vertex((0,0.1,0.35)))
    glVertex3f(*scale_vertex((0,0,0.35)))

    #P7
    glVertex3f(*scale_vertex((0,0,0.45)))
    glVertex3f(*scale_vertex((0,0.1,0.45)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.45)))
    glVertex3f(*scale_vertex((-0.1,0,0.45)))

    #p8
    glVertex3f(*scale_vertex((-0.1,0,0.45)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.45)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.55)))
    glVertex3f(*scale_vertex((-0.1,0,0.55)))

    #p9
    glVertex3f(*scale_vertex((-0.1,0,0.55)))
    glVertex3f(*scale_vertex((-0.1,0.1,0.55)))
    glVertex3f(*scale_vertex((0,0.1,0.55)))
    glVertex3f(*scale_vertex((0,0,0.55)))

    #p10
    glVertex3f(*scale_vertex((0.3,0.1,0.45)))
    glVertex3f(*scale_vertex((0.3,0.5,0.45)))
    glVertex3f(*scale_vertex((0.2,0.5,0.45)))
    glVertex3f(*scale_vertex((0.2,0.1,0.45)))

    #p11
    glVertex3f(*scale_vertex((0.2,0.1,0.45)))
    glVertex3f(*scale_vertex((0.2,0.5,0.45)))
    glVertex3f(*scale_vertex((0.2,0.5,0.55)))
    glVertex3f(*scale_vertex((0.2,0.1,0.55)))

    #p12
    glVertex3f(*scale_vertex((0.2,0.1,0.55)))
    glVertex3f(*scale_vertex((0.2,0.5,0.55)))
    glVertex3f(*scale_vertex((0.3,0.5,0.55)))
    glVertex3f(*scale_vertex((0.3,0.1,0.55)))

    #p13
    glVertex3f(*scale_vertex((0.3,0.1,0.55)))
    glVertex3f(*scale_vertex((0.3,0.5,0.55)))
    glVertex3f(*scale_vertex((0.3,0.5,0.45)))
    glVertex3f(*scale_vertex((0.3,0,0.45)))


def cuerpo_pollito():

    glColor3f(1, 1, 1)  # Blanco
    
    #p14
    glVertex3f(*scale_vertex((-0.1,0.5,0)))
    glVertex3f(*scale_vertex((-0.1,1.1,0)))
    glVertex3f(*scale_vertex((-0.1,1.1,0.6)))
    glVertex3f(*scale_vertex((-0.1,0.5,0.6)))

    #p15
    glVertex3f(*scale_vertex((-0.1,0.5,0)))
    glVertex3f(*scale_vertex((-0.1,1.1,0)))
    glVertex3f(*scale_vertex((0.7,1.1,0)))
    glVertex3f(*scale_vertex((0.7,0.5,0)))

    #p16
    glVertex3f(*scale_vertex((0.7,0.5,0)))
    glVertex3f(*scale_vertex((0.7,1.1,0)))
    glVertex3f(*scale_vertex((0.7,1.1,0.6)))
    glVertex3f(*scale_vertex((0.7,0.5,0.6)))
    
    #p17
    glVertex3f(*scale_vertex((0.7,0.5,0.6)))
    glVertex3f(*scale_vertex((0.7,1.1,0.6)))
    glVertex3f(*scale_vertex((-0.1,1.1,0.6)))
    glVertex3f(*scale_vertex((-0.1,0.5,0.6)))

    #p18
    glVertex3f(*scale_vertex((0.7,0.5,0.6)))
    glVertex3f(*scale_vertex((0.7,1.1,0.6)))
    glVertex3f(*scale_vertex((-0.1,1.1,0.6)))
    glVertex3f(*scale_vertex((-0.1,0.5,0.6)))

    #p19
    glVertex3f(*scale_vertex((-0.1,1.1,0)))
    glVertex3f(*scale_vertex((0.7,1.1,0)))
    glVertex3f(*scale_vertex((0.7,1.1,0.6)))
    glVertex3f(*scale_vertex((-0.1,1.1,0.6)))
    
    #p20
    glVertex3f(*scale_vertex((-0.1,0.5,0)))
    glVertex3f(*scale_vertex((0.7,0.5,0)))
    glVertex3f(*scale_vertex((0.7,0.5,0.6)))
    glVertex3f(*scale_vertex((-0.1,0.5,0.6)))

    #p21
    glVertex3f(*scale_vertex((0,0.7,0)))
    glVertex3f(*scale_vertex((0,1.1,0)))
    glVertex3f(*scale_vertex((0,1.1,-0.1)))
    glVertex3f(*scale_vertex((0,0.7,-0.1)))
    
    #p22
    glVertex3f(*scale_vertex((0.6,0.7,0)))
    glVertex3f(*scale_vertex((0.6,1.1,0)))
    glVertex3f(*scale_vertex((0.6,1.1,-0.1)))
    glVertex3f(*scale_vertex((0.6,0.7,-0.1)))

    #p23
    glVertex3f(*scale_vertex((0,0.7,0)))
    glVertex3f(*scale_vertex((0,1.1,0)))
    glVertex3f(*scale_vertex((0.6,1.1,0)))
    glVertex3f(*scale_vertex((0.6,0.7,0)))

    #p24
    glVertex3f(*scale_vertex((0,0.7,-0.1)))
    glVertex3f(*scale_vertex((0,1.1,-0.1)))
    glVertex3f(*scale_vertex((0.6,1.1,-0.1)))
    glVertex3f(*scale_vertex((0.6,0.7,-0.1)))

    #p25
    glVertex3f(*scale_vertex((0,1.1,0)))
    glVertex3f(*scale_vertex((0.6,1.1,0)))
    glVertex3f(*scale_vertex((0.6,1.1,-0.1)))
    glVertex3f(*scale_vertex((0,1.1,-0.1)))

    #p26
    glVertex3f(*scale_vertex((0,0.7,0)))
    glVertex3f(*scale_vertex((0.6,0.7,0)))
    glVertex3f(*scale_vertex((0.6,0.7,-0.1)))
    glVertex3f(*scale_vertex((0,0.7,-0.1)))

    #ala izquierda
    #p21
    glVertex3f(*scale_vertex((0,0.7,0.7)))
    glVertex3f(*scale_vertex((0,1.1,0.7)))
    glVertex3f(*scale_vertex((0,1.1,0.6)))
    glVertex3f(*scale_vertex((0,0.7,0.6)))
    
    #p22
    glVertex3f(*scale_vertex((0.6,0.7,0.7)))
    glVertex3f(*scale_vertex((0.6,1.1,0.7)))
    glVertex3f(*scale_vertex((0.6,1.1,0.6)))
    glVertex3f(*scale_vertex((0.6,0.7,0.6)))

    #p23
    glVertex3f(*scale_vertex((0,0.7,0.7)))
    glVertex3f(*scale_vertex((0,1.1,0.7)))
    glVertex3f(*scale_vertex((0.6,1.1,0.7)))
    glVertex3f(*scale_vertex((0.6,0.7,0.7)))

    #p24
    glVertex3f(*scale_vertex((0,0.7,0.6)))
    glVertex3f(*scale_vertex((0,1.1,0.6)))
    glVertex3f(*scale_vertex((0.6,1.1,0.6)))
    glVertex3f(*scale_vertex((0.6,0.7,0.6)))

    #p25
    glVertex3f(*scale_vertex((0,1.1,0.7)))
    glVertex3f(*scale_vertex((0.6,1.1,0.7)))
    glVertex3f(*scale_vertex((0.6,1.1,0.6)))
    glVertex3f(*scale_vertex((0,1.1,0.6)))

    #p26
    glVertex3f(*scale_vertex((0,0.7,0.7)))
    glVertex3f(*scale_vertex((0.6,0.7,0.7)))
    glVertex3f(*scale_vertex((0.6,0.7,0.6)))
    glVertex3f(*scale_vertex((0,0.7,0.6)))
    
    #Cabeza

    #p27
    glVertex3f(0,0.9,0.1)
    glVertex3f(0,1.5,0.1)
    glVertex3f(-0.3,1.5,0.1)
    glVertex3f(-0.3,0.9,0.1)

    #p28
    glVertex3f(0,0.9,0.5)
    glVertex3f(0,1.5,0.5)
    glVertex3f(-0.3,1.5,0.5)
    glVertex3f(-0.3,0.9,0.5)

    #p29
    glVertex3f(0,1.5,0.1)
    glVertex3f(0,1.5,0.5)
    glVertex3f(-0.3,1.5,0.5)
    glVertex3f(-0.3,1.5,0.1)
    
    #p30
    glVertex3f(0,0.9,0.1)
    glVertex3f(0,0.9,0.5)
    glVertex3f(-0.3,0.9,0.5)
    glVertex3f(-0.3,0.9,0.1)

    #p31
    glVertex3f(-0.3,0.9,0.1)
    glVertex3f(-0.3,1.5,0.1)
    glVertex3f(-0.3,1.5,0.5)
    glVertex3f(-0.3,0.9,0.5)
    
    #p32
    glVertex3f(0,0.9,0.1)
    glVertex3f(0,1.5,0.1)
    glVertex3f(0,1.5,0.5)
    glVertex3f(0,0.9,0.5)

    #Ojos
    #p33
    glColor3f(0, 0, 0)  # Negro
    

    glVertex3f(-0.31,1.4,0.1)
    glVertex3f(-0.31,1.4,0.2)
    glVertex3f(-0.31,1.3,0.2)
    glVertex3f(-0.31,1.3,0.1)

    #p34
    glVertex3f(-0.31,1.4,0.4)
    glVertex3f(-0.31,1.4,0.5)
    glVertex3f(-0.31,1.3,0.5)
    glVertex3f(-0.31,1.3,0.4)

    #Pico
    glColor3f(1.0, 0.5, 0.0); #Orange
    #p35
    glVertex3f(-0.3,1.2,0.1)
    glVertex3f(-0.3,1.3,0.1)
    glVertex3f(-0.5,1.3,0.1)
    glVertex3f(-0.5,1.2,0.1)

    #p36
    glVertex3f(-0.3,1.2,0.5)
    glVertex3f(-0.3,1.3,0.5)
    glVertex3f(-0.5,1.3,0.5)
    glVertex3f(-0.5,1.2,0.5)
    
    #p37
    glVertex3f(-0.3,1.3,0.1)
    glVertex3f(-0.5,1.3,0.1)
    glVertex3f(-0.5,1.3,0.5)
    glVertex3f(-0.3,1.3,0.5)

    #p38
    glVertex3f(-0.3,1.2,0.1)
    glVertex3f(-0.5,1.2,0.1)
    glVertex3f(-0.5,1.2,0.5)
    glVertex3f(-0.3,1.2,0.5)

    #p39
    glVertex3f(-0.5,1.2,0.1)
    glVertex3f(-0.5,1.2,0.5)
    glVertex3f(-0.5,1.3,0.5)
    glVertex3f(-0.5,1.3,0.1)

    #Pico Inferior
    glColor3f(1.0, 0.45, 0.0)

    #p35
    glVertex3f(-0.3,1.1,0.1)
    glVertex3f(-0.3,1.2,0.1)
    glVertex3f(-0.5,1.2,0.1)
    glVertex3f(-0.5,1.1,0.1)

    #p36
    glVertex3f(-0.3,1.1,0.5)
    glVertex3f(-0.3,1.2,0.5)
    glVertex3f(-0.5,1.2,0.5)
    glVertex3f(-0.5,1.1,0.5)
    
    #p37
    glVertex3f(-0.3,1.2,0.1)
    glVertex3f(-0.5,1.2,0.1)
    glVertex3f(-0.5,1.2,0.5)
    glVertex3f(-0.3,1.2,0.5)

    #p38
    glVertex3f(-0.3,1.1,0.1)
    glVertex3f(-0.5,1.1,0.1)
    glVertex3f(-0.5,1.1,0.5)
    glVertex3f(-0.3,1.1,0.5)

    #p39
    glVertex3f(-0.5,1.1,0.1)
    glVertex3f(-0.5,1.1,0.5)
    glVertex3f(-0.5,1.2,0.5)
    glVertex3f(-0.5,1.2,0.1)

    #Cresta
    glColor3f(1.0, 0, 0)
    #p40
    glVertex3f(-0.4,0.9,0.2)
    glVertex3f(-0.4,1.1,0.2)
    glVertex3f(-0.4,1.1,0.4)
    glVertex3f(-0.4,0.9,0.4)

    #p41
    glVertex3f(-0.4,0.9,0.2)
    glVertex3f(-0.4,1.1,0.2)
    glVertex3f(-0.3,1.1,0.2)
    glVertex3f(-0.3,0.9,0.2)

    #p42
    glVertex3f(-0.4,0.9,0.2)
    glVertex3f(-0.3,0.9,0.2)
    glVertex3f(-0.3,0.9,0.4)
    glVertex3f(-0.4,0.9,0.4)



def pata_vaca(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    #Pata 1
    #p1
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(0,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0,1.2,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,1.2,0)

    #p2
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,0)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,1.2,0)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,1.2,0)

    #p3
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,1.2,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.4,1.2,0)
    
    #p4
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,1.2,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,1.2,0.4)

    #Pata2
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(0,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0,1.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,1.2,0.8)

    #p2
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,0.8)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,1.2,0.8)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,1.2,0.8)

    #p3
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,1.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.4,1.2,0.8)
    
    #p4
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,1.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,1.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,1.2,1.2)

    #Pata 3
    #p1
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.4,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.4,1.2,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,1.2,0)

    #p2
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,0)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,1.2,0)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,1.2,0)

    #p3
    glTexCoord2f(0.0, 0.0); glVertex3f(1.8,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,1.2,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.8,1.2,0)
    
    #p4
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,1.2,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,1.2,0.4)

    #Pata4
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.4,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.4,1.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,1.2,0.8)

    #p2
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,0.8)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,1.2,0.8)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,1.2,0.8)

    #p3
    glTexCoord2f(0.0, 0.0); glVertex3f(1.8,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,1.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.8,1.2,0.8)
    
    #p4
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,1.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,1.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,1.2,1.2)


    glEnd()


def cuerpo_vaca(texture, cara):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    #p5
    glTexCoord2f(0.0, 0.0); glVertex3d(0,1.2,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,2.2,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(1.8,2.2,0)
    glTexCoord2f(0.0, 1.0); glVertex3d(1.8,1.2,0)

    #p6
    glTexCoord2f(0.0, 0.0); glVertex3d(0,1.2,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,2.2,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(0,2.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0,1.2,1.2)

    #p7
    glTexCoord2f(0.0, 0.0); glVertex3d(0,1.2,1.2)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,2.2,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(1.8,2.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(1.8,1.2,1.2)

    #p8
    glTexCoord2f(0.0, 0.0); glVertex3d(1.8,1.2,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(1.8,2.2,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(1.8,2.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(1.8,1.2,1.2)

    #P9
    glTexCoord2f(0.0, 0.0); glVertex3d(1.8,2.2,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(1.8,2.2,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(0,2.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0,2.2,0)

    #P10
    glTexCoord2f(0.0, 0.0); glVertex3d(1.8,1.2,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(1.8,1.2,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(0,1.2,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0,1.2,0)

    #Cabeza
    glColor3f(1, 1, 1)
    #p11
    glTexCoord2f(0.0, 0.0); glVertex3d(0,2.4,0.2)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.6,0.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,1.6,0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,2.4,0.2)

    #p12
    glTexCoord2f(0.0, 0.0); glVertex3d(0,2.4,1)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.6,1)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,1.6,1)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,2.4,1)
    

    #p14
    glTexCoord2f(0.0, 0.0); glVertex3d(0,1.6,1)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,2.4,1)
    glTexCoord2f(1.0, 1.0); glVertex3d(0,2.4,0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0,1.6,0.2)
    
    #p15
    glTexCoord2f(0.0, 0.0); glVertex3d(0,1.6,1)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.6,0.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,1.6,0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,1.6,1)

    #p15
    glTexCoord2f(0.0, 0.0); glVertex3d(0,2.4,1)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,2.4,0.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,2.4,0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,2.4,1)
    glEnd()


    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, cara)

    glBegin(GL_QUADS)
    #cara
    #glVertex3d(-0.8,1.6,1)
    #glVertex3d(-0.8,2.4,1)
    #glVertex3d(-0.8,2.4,0.2)
    #glVertex3d(-0.8,1.6,0.2)
    glTexCoord2f(0.0, 0.0); glVertex3d(-0.8,1.6,1)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,2.4,1)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,2.4,0.2)
    glTexCoord2f(1.0, 0.0); glVertex3d(-0.8,1.6,0.2)

    glColor3f(1, 1, 1)
    
    glEnd()

    



def vaca(texture, vaca_patas, cara):
    pata_vaca(vaca_patas)
    cuerpo_vaca(texture, cara)


def patas_cerdito(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.8, 0.9)

    #Pata 1
    #p1
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(0,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0,0.6,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,0.6,0)

    #p2
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,0)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,0.6,0)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,0.6,0)

    #p3
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,0.6,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.4,0.6,0)
    
    #p4
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,0.6,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,0.6,0.4)

    #Pata2
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(0,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0,0.6,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,0.6,0.8)

    #p2
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,0.8)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,0.6,0.8)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,0.6,0.8)

    #p3
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,0.6,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.4,0.6,0.8)
    
    #p4
    glTexCoord2f(0.0, 0.0); glVertex3f(0,0,1.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4,0.6,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(0,0.6,1.2)

    #Pata 3
    #p1
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.4,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.4,0.6,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,0.6,0)

    #p2
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,0)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,0.6,0)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,0.6,0)

    #p3
    glTexCoord2f(0.0, 0.0); glVertex3f(1.8,0,0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,0.6,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.8,0.6,0)
    
    #p4
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,0.6,0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,0.6,0.4)

    #Pata4
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.4,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.4,0.6,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,0.6,0.8)

    #p2
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,0.8)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,0.6,0.8)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,0.6,0.8)

    #p3
    glTexCoord2f(0.0, 0.0); glVertex3f(1.8,0,0.8)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,0.6,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.8,0.6,0.8)
    
    #p4
    glTexCoord2f(0.0, 0.0); glVertex3f(1.4,0,1.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.8,0,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.8,0.6,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(1.4,0.6,1.2)


    glEnd()


def cuerpo_cerdito(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.8, 0.9)

    #p5
    glTexCoord2f(0.0, 0.0); glVertex3d(0,0.6,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.4,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(1.8,1.4,0)
    glTexCoord2f(0.0, 1.0); glVertex3d(1.8,0.6,0)

    #p6
    glTexCoord2f(0.0, 0.0); glVertex3d(0,0.6,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.4,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(0,1.4,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0,0.6,1.2)

    #p7
    glTexCoord2f(0.0, 0.0); glVertex3d(0,0.6,1.2)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.4,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(1.8,1.4,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(1.8,0.6,1.2)

    #p8
    glTexCoord2f(0.0, 0.0); glVertex3d(1.8,0.6,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(1.8,1.4,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(1.8,1.4,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(1.8,0.6,1.2)

    #P9
    glTexCoord2f(0.0, 0.0); glVertex3d(1.8,1.4,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(1.8,1.4,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(0,1.4,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0,1.4,0)

    #P10
    glTexCoord2f(0.0, 0.0); glVertex3d(1.8,0.6,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(1.8,0.6,1.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(0,0.6,1.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0,0.6,0)

    #Cabeza
    
    #p11
    glTexCoord2f(0.0, 0.0); glVertex3d(0,2,0.2)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.2,0.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,1.2,0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,2,0.2)

    #p12
    glTexCoord2f(0.0, 0.0); glVertex3d(0,2,1)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.2,1)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,1.2,1)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,2,1)
    
    #p13
    

    #cara
    #glVertex3d(-0.8,1.6,1)
    #glVertex3d(-0.8,2.4,1)
    #glVertex3d(-0.8,2.4,0.2)
    #glVertex3d(-0.8,1.6,0.2)
    glTexCoord2f(0.0, 0.0); glVertex3d(-0.8,1.2,1)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,2,1)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,2,0.2)
    glTexCoord2f(1.0, 0.0); glVertex3d(-0.8,1.2,0.2)

    

    #p14
    glTexCoord2f(0.0, 0.0); glVertex3d(0,1.2,1)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,2,1)
    glTexCoord2f(1.0, 1.0); glVertex3d(0,2,0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0,1.2,0.2)
    
    #p15
    glTexCoord2f(0.0, 0.0); glVertex3d(0,1.2,1)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.2,0.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,1.2,0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,1.2,1)

    #p15
    glTexCoord2f(0.0, 0.0); glVertex3d(0,2,1)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,2,0.2)
    glTexCoord2f(1.0, 1.0); glVertex3d(-0.8,2,0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(-0.8,2,1)
    
    glEnd()

    

def cerdito(texture):
    patas_cerdito(texture)
    cuerpo_cerdito(texture)




def pollito():
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 0.0)  # Amarillo
    patas_pollito()
    cuerpo_pollito()
    
    glEnd()


def chicken_tractor(texture):
    """
    # Verifica si la textura es válida
    if not glIsTexture(texture):
        print(f"Error: ID de textura no válido {texture}")
        return

    
    """
    glBindTexture(GL_TEXTURE_2D, texture)
    # Dibuja el tractor
    glBegin(GL_QUADS)
    glColor3f(0.36, 0.25, 0.20)
    
    
    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.1, 0)
    glTexCoord2f(1.0, 0.0); glVertex3d(5, 0.1, 0)
    glTexCoord2f(1.0, 1.0); glVertex3d(5, 0.4, 0)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 0.4, 0)

    # Parte derecha techo
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.4, 0)
    glTexCoord2f(1.0, 0.0); glVertex3d(5, 0.4, 0)
    glTexCoord2f(1.0, 1.0); glVertex3d(5, 0.4, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 0.4, 0.2)

    # Parte frontal
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.1, 0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0, 0.4, 2)
    glTexCoord2f(1.0, 1.0); glVertex3d(0, 0.1, 2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 0.4, 0)

    # Parte frontal techo
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.4, 0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0, 0.4, 2)
    glTexCoord2f(1.0, 1.0); glVertex3d(0.2, 0.4, 2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0.2, 0.4, 0)

    #Parte Trasera
    glTexCoord2f(0.0, 0.0); glVertex3d(4.5,0.1,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(4.5,0.4,2)
    glTexCoord2f(1.0, 1.0); glVertex3d(4.5,0.1,2)
    glTexCoord2f(0.0, 1.0); glVertex3d(4.5,0.4,0)

    #Parte Trasera Techo
    glTexCoord2f(0.0, 0.0); glVertex3d(4.5,0.4,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(4.5,0.4,2)
    glTexCoord2f(1.0, 1.0); glVertex3d(4.3,0.4,2)
    glTexCoord2f(0.0, 1.0); glVertex3d(4.3,0.4,0)
    
    #Parte Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.1, 2)
    glTexCoord2f(1.0, 0.0); glVertex3d(5, 0.1, 2)
    glTexCoord2f(1.0, 1.0); glVertex3d(5, 0.4, 2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 0.4, 2)
    
    #Parte Izquierda Techo
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.4, 2)
    glTexCoord2f(1.0, 0.0); glVertex3d(5, 0.4, 2)
    glTexCoord2f(1.0, 1.0); glVertex3d(5, 0.4, 1.8)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 0.4, 1.8)

    #Tubo Que Sube #1
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.1, 0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0, 1.6, 0)
    glTexCoord2f(1.0, 1.0); glVertex3d(0.2, 1.6, 0)
    glTexCoord2f(0.0, 1.0); glVertex3d(0.2, 0.1, 0)

    #Tubo Que Sube #1.1
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.1, 0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0, 1.6, 0)
    glTexCoord2f(1.0, 1.0); glVertex3d(0, 1.6, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 0.1, 0.2)

    #Tubo Frontal
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 1.6, 0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0, 1.8, 0)
    glTexCoord2f(1.0, 1.0); glVertex3d(0, 1.6, 2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 1.8, 2)

    #Tubo Frontal Techo
    glTexCoord2f(0.0, 0.0); glVertex3d(0,1.8,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(0,1.8,2)
    glTexCoord2f(1.0, 1.0); glVertex3d(0.2,1.8,2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0.2,1.8,0)

    #Tubo Izquierdo Superior
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 1.6, 2)
    glTexCoord2f(1.0, 0.0); glVertex3d(5, 1.8, 2)
    glTexCoord2f(1.0, 1.0); glVertex3d(5, 1.6, 2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 1.8, 2)

    #Tubo derecho Superior
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 1.6, 0)
    glTexCoord2f(1.0, 0.0); glVertex3d(5, 1.6, 0)
    glTexCoord2f(1.0, 1.0); glVertex3d(5, 1.8, 0)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 1.8, 0)

    #Tubo Derecho Superior Techo
    glTexCoord2f(0.0, 0.0); glVertex3d(0,1.8,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(5,1.8,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(5, 1.8, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 1.8, 0.2)

    #Tubo Izquierdo Superior Techo
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 1.8, 2)
    glTexCoord2f(1.0, 0.0); glVertex3d(5, 1.8, 2)
    glTexCoord2f(1.0, 1.0); glVertex3d(5, 1.8, 1.8)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 1.8, 1.8)

    #Tubo Que Sube #2
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.1, 2)
    glTexCoord2f(1.0, 0.0); glVertex3d(0, 1.6, 2)
    glTexCoord2f(1.0, 1.0); glVertex3d(0.2, 1.6, 2)
    glTexCoord2f(0.0, 1.0); glVertex3d(0.2, 0.1, 2)

    #Tubo Que Sube #2.1
    glTexCoord2f(0.0, 0.0); glVertex3d(0, 0.1, 2)
    glTexCoord2f(1.0, 0.0); glVertex3d(0, 1.6, 2)
    glTexCoord2f(1.0, 1.0); glVertex3d(0, 1.6, 1.8)
    glTexCoord2f(0.0, 1.0); glVertex3d(0, 0.1, 1.8)

    #Casita Parte Trasera
    glTexCoord2f(0.0, 0.0); glVertex3d(4.5 , 1.8 ,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(4.5 , 3.5 ,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(4.5 , 3.5 ,2)
    glTexCoord2f(0.0, 1.0); glVertex3d(4.5 , 1.8 ,2)

    glTexCoord2f(0.0, 0.0); glVertex3d(4.5, 1.8 ,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(4.5, 3.5 ,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(2.5, 3.5 ,0)
    glTexCoord2f(0.0, 1.0); glVertex3d(2.5, 1.8 ,0)

    glTexCoord2f(0.0, 0.0); glVertex3d(4.5, 1.8 ,2)
    glTexCoord2f(1.0, 0.0); glVertex3d(4.5, 3.5 ,2)
    glTexCoord2f(1.0, 1.0); glVertex3d(2.5, 3.5 ,2)
    glTexCoord2f(0.0, 1.0); glVertex3d(2.5, 1.8 ,2)
    
    glTexCoord2f(0.0, 0.0); glVertex3d(2.5, 1.8 ,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(2.5, 3.5 ,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(2.5, 3.5 ,2)
    glTexCoord2f(0.0, 1.0); glVertex3d(2.5, 1.8 ,2)
    
    glTexCoord2f(0.0, 0.0); glVertex3d(2.5, 3.5 ,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(2.5, 3.5 ,2)
    glTexCoord2f(1.0, 1.0); glVertex3d(4.5, 3.5 ,2)
    glTexCoord2f(0.0, 1.0); glVertex3d(4.5, 3.5 ,0)

    glTexCoord2f(0.0, 0.0); glVertex3d(1.2, 1.8, 0)
    glTexCoord2f(1.0, 0.0); glVertex3d(1.45, 1.8, 0)
    glTexCoord2f(1.0, 1.0); glVertex3d(1.45, 1.8, 2)
    glTexCoord2f(0.0, 1.0); glVertex3d(1.2, 1.8, 2)

    glTexCoord2f(0.0, 0.0); glVertex3d(3.5,0.1,0)
    glTexCoord2f(1.0, 0.0); glVertex3d(4.5,0.1,0)
    glTexCoord2f(1.0, 1.0); glVertex3d(4.5,1.8,0)
    glTexCoord2f(0.0, 1.0); glVertex3d(3.5,1.8,0)

    glTexCoord2f(0.0, 0.0); glVertex3d(3.5,0.1,2)
    glTexCoord2f(1.0, 0.0); glVertex3d(4.5,0.1,2)
    glTexCoord2f(1.0, 1.0); glVertex3d(4.5,1.8,2)
    glTexCoord2f(0.0, 1.0); glVertex3d(3.5,1.8,2)

    glEnd()



def draw_ground():
    """Dibuja un plano para representar el suelo o calle"""
    glBegin(GL_QUADS)
    glColor3f(0.13, 0.55, 0.13)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()



def draw_scene(texture, pollito_pos, vaca_texture, angulo_rot, cerdito_texture, vaca_patas, vaca_cara):
    """Dibuja toda la escena con casas"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(
        eje_x, eje_y, eje_z,
        eje_x + center_x, eje_y + center_y, eje_z + center_z,
        0.0, 1.0, 0.0
    )    # Vector hacia arriba

    # Dibujar el suelo
    draw_ground()

    glPushMatrix()
    glTranslatef(-2, 0, 0)  # Posición inicial del tractor
    chicken_tractor(texture)
    glPopMatrix()

    draw_pollito(pollito_pos, angulo_rot)

    

    glTranslate(7, 0, 7)
    vaca(vaca_texture, vaca_patas, vaca_cara)
    glTranslate(7, 10, 7)

    cerdito(cerdito_texture)

    glTranslate(eje_x, eje_y, eje_z)

    glfw.swap_buffers(window)



def avanzar_izq_der(is_izq):
    """Mueve la cámara a la izquierda o derecha"""
    global angulo_th, angulo_pi, radio
    global center_x, center_z
    global eje_x, eje_z
    global movimiento

    # Girar para la izquierda o derecha 90 grados
    if is_izq:
        angulo_th -= (math.pi / 2)
    else:
        angulo_th += (math.pi / 2)

    # Convertir coordenada esférica a rectangular (solo x y z)
    center_x = radio * math.sin(angulo_pi) * math.cos(angulo_th)
    center_z = radio * math.sin(angulo_pi) * math.sin(angulo_th)

    # Avanzar en x y z
    eje_x += center_x * movimiento
    eje_z += center_z * movimiento

    # Retornar al ángulo inicial
    if is_izq:
        angulo_th += (math.pi / 2)
    else:
        angulo_th -= (math.pi / 2)

    # Actualizar center_x y center_z
    center_x = radio * math.sin(angulo_pi) * math.cos(angulo_th)
    center_z = radio * math.sin(angulo_pi) * math.sin(angulo_th)


def key_callback(window, key, scancode, action, mods):
    """Manejo de eventos del teclado para mover la cámara"""
    global angulo_pi, angulo_th, saltos, radio
    global center_x, center_y, center_z
    global eje_x, eje_y, eje_z
    global movimiento

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:
            # Avanzar
            eje_x += center_x * movimiento
            eje_y += center_y * movimiento
            eje_z += center_z * movimiento
        elif key == glfw.KEY_S:
            # Retroceder
            eje_x -= center_x * movimiento
            eje_y -= center_y * movimiento
            eje_z -= center_z * movimiento
        elif key == glfw.KEY_A:
            # Mover a la izquierda
            avanzar_izq_der(True)
        elif key == glfw.KEY_D:
            # Mover a la derecha
            avanzar_izq_der(False)
        elif key == glfw.KEY_LEFT:
            # Girar a la izquierda
            angulo_th -= saltos
        elif key == glfw.KEY_RIGHT:
            # Girar a la derecha
            angulo_th += saltos
        elif key == glfw.KEY_UP:
            # Girar hacia arriba
            angulo_pi -= saltos
            if angulo_pi <= 0.0:
                angulo_pi = 0.001  # Evitar valor cero
        elif key == glfw.KEY_DOWN:
            # Girar hacia abajo
            angulo_pi += saltos
            if angulo_pi >= math.pi:
                angulo_pi = math.pi - 0.001  # Evitar exceder pi

        # Actualizar los valores de dirección
        center_x = radio * math.sin(angulo_pi) * math.cos(angulo_th)
        center_y = radio * math.cos(angulo_pi)
        center_z = radio * math.sin(angulo_pi) * math.sin(angulo_th)


def actualizar_posicion_pollito(pollito_pos, direccion, limite, angulo_rot):
    """Actualiza la posición del pollito y su rotación si cambia de dirección"""
    pollito_pos[0] += 0.05 * direccion[0]  # Actualizar posición en X
    if pollito_pos[0] > limite or pollito_pos[0] < -limite:  # Cambiar dirección en X
        direccion[0] *= -1  # Cambiar dirección
        angulo_rot[0] += 180  # Girar el pollito 180 grados
        angulo_rot[0] %= 360  # Asegurar que el ángulo esté en el rango [0, 360)
    return pollito_pos, direccion, angulo_rot

def draw_pollito(pollito_pos, angulo_rot):
    """Dibuja el pollito en la posición especificada con su rotación"""
    glPushMatrix()
    glTranslatef(*pollito_pos)  # Mover el pollito a su posición
    glRotatef(angulo_rot[0], 0, 1, 0)  # Rotar el pollito en el eje Y
    pollito()
    glPopMatrix()


def main():
    global window
    global radio
    global angulo_th 
    global angulo_pi
    global movimiento
    global saltos
    global eje_x
    global eje_y
    global eje_z
    global center_x
    global center_y
    global center_z

    radio = 1.0
    angulo_th = 3.9
    angulo_pi = 2.2

    saltos = 0.15
    movimiento = 0.8
    eje_x = 10.0
    eje_y = 2.0
    eje_z = 15.0

    # Inicializar la dirección inicial de la cámara
    center_x = radio * math.sin(angulo_pi) * math.cos(angulo_th)
    center_y = radio * math.cos(angulo_pi)
    center_z = radio * math.sin(angulo_pi) * math.sin(angulo_th)

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Escena con Casas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Configurar la función de callback para el teclado
    glfw.set_key_callback(window, key_callback)

    madera_tracktor_texture = load_texture('wood_tracktor.jpg') 
    vaca_cuerpo = load_texture('vaca_cuerpo.jpg')
    vaca_patas = load_texture('vaca_patas.jpg')
    vaca_cara = load_texture('vaca_cara.jpg')
    cerdito_textura = load_texture('cerdito.jpg')
    pollito_pos = [0.0, 0.0, 0.0]  # [x, y, z]
    direccion = [0.05]  # Dirección del movimiento (1 para adelante, -1 para atrás)
    limite = 1.5  # Límite de movimiento en el eje X
    angulo_rot = [180]

    # Bucle principal
    while not glfw.window_should_close(window):
        pollito_pos, direccion, angulo_rot = actualizar_posicion_pollito(pollito_pos, direccion, limite, angulo_rot)
        draw_scene(madera_tracktor_texture, pollito_pos, vaca_cuerpo, angulo_rot, cerdito_textura, vaca_patas, vaca_cara)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
