import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluSphere, gluCylinder, gluQuadricTexture
import sys
import math
from PIL import Image
from math import sin, cos, pi

def load_texture(texture_file):
    img = Image.open(texture_file)
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
    
def valla_horizontal(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  
        # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0.3, 4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0.3, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 0.7, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 0.7, 4)
        
    glEnd()
    
def poste_valla(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)    

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 0, 0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 0, 0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 2.5, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 2.5, 0.2)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 0, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 0, -0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 2.5, -0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 2.5, -0.2)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 0, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.2, 0, 0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.2, 2.5, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 2.5, -0.2)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.2, 0, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 0, 0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 2.5, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.2, 2.5, -0.2)

    # Arriba  
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 2.5, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 2.5, -0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 2.5, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 2.5, 0.2)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 0, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 0, -0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 0, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 0, 0.2)
    glEnd()
    
def draw_tierra(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1) 

    glTexCoord2f(0.0, 0.0); glVertex3f(-5, 0.01, 5)
    glTexCoord2f(1.0, 0.0); glVertex3f(5, 0.01, 5)
    glTexCoord2f(1.0, 1.0); glVertex3f(5, 0.01, -5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-5, 0.01, -5)
    glEnd()
    
def draw_circle(center_x, center_y, radius, num_segments, texture):
    """Dibuja un círculo lleno acostado en el plano XZ."""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1, 1, 1) 
    glTexCoord2f(0.0, 0.0); glVertex3f(center_x, center_y, center_z)  # Centro del círculo
    for i in range(num_segments + 1):  # +1 para cerrar el círculo
        angle = 2.0 * pi * i / num_segments
        x = radius * cos(angle)
        z = radius * sin(angle)  # Usa Z en lugar de Y
        glTexCoord2f(0.5, 0.5); glVertex3f(center_x + x, center_y + 0.001, center_z + z)
    glEnd()
    
    
def draw_corral_oveja(tierra_pasto_texture, madera_valla_texture):
    positionsH = [
        (0, 0.3, 0),
        (0, 0.8, 0),
        (0, 1.3, 0),
        (0, 0.3, -8),
        (0, 0.8, -8),
        (0, 1.3, -8)
    ]
    for pos in positionsH:
        glPushMatrix()
        glTranslatef(*pos)
        valla_horizontal(madera_valla_texture)
        glPopMatrix()

    positionsV = [
        (0, 0.3, 0),
        (0, 0.8, 0),
        (0, 1.3, 0),
        (-8, 0.3, 0),
        (-8, 0.8, 0),
        (-8, 1.3, 0)
    ]
    for pos in positionsV:
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(90, 0.0, 1.0, 0.0)
        valla_horizontal(madera_valla_texture)
        glPopMatrix()
        
    positionP = [
        (3.8, 0,  0),
        (3.8, 0,  4),
        (3.8, 0,  -4),
        (-3.8, 0,  0),
        (-3.8, 0,  4),
        (-3.8, 0,  -4),
        (0, 0,  -4)
    ]
    for pos in positionP:
        glPushMatrix()
        glTranslatef(*pos)   
        poste_valla(madera_valla_texture)
        glPopMatrix()
        
    draw_tierra(tierra_pasto_texture)

    
def draw_corral_cerdo(tierra_pasto_texture, madera_valla_texture, lodo_texture):
    positionsH = [
        (0, 0.3, 0),
        (0, 0.8, 0),
        (0, 1.3, 0),
        (0, 0.3, -8),
        (0, 0.8, -8),
        (0, 1.3, -8)
    ]
    for pos in positionsH:
        glPushMatrix()
        glTranslatef(*pos)
        valla_horizontal(madera_valla_texture)
        glPopMatrix()

    positionsV = [
        (0, 0.3, 0),
        (0, 0.8, 0),
        (0, 1.3, 0),
        (-8, 0.3, 0),
        (-8, 0.8, 0),
        (-8, 1.3, 0)
    ]
    for pos in positionsV:
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(90, 0.0, 1.0, 0.0)
        valla_horizontal(madera_valla_texture)
        glPopMatrix()
        
    positionP = [
        (3.8, 0,  0),
        (3.8, 0,  4),
        (3.8, 0,  -4),
        (-3.8, 0,  0),
        (-3.8, 0,  4),
        (-3.8, 0,  -4),
        (0, 0,  -4)
    ]
    for pos in positionP:
        glPushMatrix()
        glTranslatef(*pos)   
        poste_valla(madera_valla_texture)
        glPopMatrix()
        
    draw_tierra(tierra_pasto_texture)
    
    positionC = [
        (1, 0.03,  0),
        (1, 0.03,  1.5),
        (-0.5, 0.03,  0)
    ]
    for pos in positionC:
        glPushMatrix()
        glTranslatef(*pos)   
        draw_circle(0.0, 0.0, 2, 50, lodo_texture)
        glPopMatrix()
    
    
def draw_base(texture):
    """Dibuja el cubo (base de la casa)"""
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura

    glBegin(GL_QUADS)
    glColor3f(0.717, 0.011, 0.011)  

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0, 4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 4, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 4, 4)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0, -4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 4, -4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 4, -4)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(-4, 0, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(-4, 4, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 4, -4)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(4, 0, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 4, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(4, 4, -4)

    # Arriba
    glColor3f(0.9, 0.6, 0.3)  # Color diferente para el techo
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 4, -1)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 4, -1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 4, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 4, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0, -4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 0, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 0, 4)
    glEnd()
    
def draw_base2(texture):
    """Dibuja el cubo (base de la casa)"""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(0.717, 0.011, 0.011)  

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 4, 4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 4, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(3, 7, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-3, 7, 3)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 4, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 4, -4)
    glTexCoord2f(1.0, 1.0); glVertex3f(3, 7, -3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-3, 7, -3)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 4, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(-4, 4, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(-3, 7, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-3, 7, -3)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(4, 4, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 4, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(3, 7, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(3, 7, -3)
    glEnd()

def draw_base3(texture):
    """Dibuja el cubo (base de la casa)"""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(0.717, 0.011, 0.011)  

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-3, 7, 3)
    glTexCoord2f(1.0, 0.0); glVertex3f(3, 7, 3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0, 9, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0, 9, 3)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-3, 7, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(3, 7, -3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0, 9, -3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0, 9, -3)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-3, 7, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(-3, 7, 3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0, 9, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0, 9, -3)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(3, 7, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(3, 7, 3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0, 9, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0, 9, -3)
    glEnd()
    
def draw_techo(texture):
    """Dibuja el techo (pirámide)"""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(0.254, 0.678, 0.823)  

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-4.01, 4.01, -4.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-4.01, 4.01, 4.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-3.01, 7.01, 3.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-3.01, 7.01, -3.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(4.01, 4.01, -4.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(4.01, 4.01, 4.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(3.01, 7.01, 3.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(3.01, 7.01, -3.5)
    glEnd()
    
def draw_techo2(texture):
    """Dibuja el techo (pirámide)"""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(0.254, 0.678, 0.823)  

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-3.05, 7.01, -3.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-3.05, 7.01, 3.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.01, 9.01, 3.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.01, 9.01, -3.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(3.01, 7.01, -3.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(3.01, 7.01, 3.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.01, 9.01, 3.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.01, 9.01, -3.5)
    glEnd()

def draw_puerta(texture1, texture2):
    glBindTexture(GL_TEXTURE_2D, texture1)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  
    
    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-2.7, 0, 4.1)
    glTexCoord2f(1.0, 0.0); glVertex3f(2.5, 0, 4.1)
    glTexCoord2f(1.0, 1.0); glVertex3f(2.5, 3, 4.1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-2.7, 3, 4.1)
    glEnd()
    
    # puerta izquierda
    glBindTexture(GL_TEXTURE_2D, texture2)
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)  
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-2.5, 0.2, 4.15)
    glTexCoord2f(0.0, 1.0); glVertex3f(-2.5, 2.8, 4.15)
    glTexCoord2f(1.0, 0.5); glVertex3f(-1.35, 1.4, 4.15)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)  
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-2.3, 0.2, 4.15)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.2, 0.2, 4.15)
    glTexCoord2f(0.5, 1.0); glVertex3f(-1.35, 1.2, 4.15)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)  
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-0, 0.2, 4.15)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0, 2.8, 4.15)
    glTexCoord2f(1.0, 0.5); glVertex3f(-1.25, 1.4, 4.15)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)  
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-2.3, 2.8, 4.15)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.2, 2.8, 4.15)
    glTexCoord2f(0.5, 1.0); glVertex3f(-1.25, 1.6, 4.15)
    glEnd()

    #puerta derecha
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)  
    
    glTexCoord2f(0.0, 0.0); glVertex3f(0.2, 0.2, 4.15)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.2, 2.8, 4.15)
    glTexCoord2f(1.0, 0.5); glVertex3f(1.15, 1.4, 4.15)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)  
    
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4, 0.2, 4.15)
    glTexCoord2f(1.0, 0.0); glVertex3f(2.1, 0.2, 4.15)
    glTexCoord2f(0.5, 1.0); glVertex3f(1.2, 1.2, 4.15)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)  
    
    glTexCoord2f(0.0, 0.0); glVertex3f(2.3, 0.2, 4.15)
    glTexCoord2f(0.0, 1.0); glVertex3f(2.3, 2.8, 4.15)
    glTexCoord2f(1.0, 0.5); glVertex3f(1.25, 1.4, 4.15)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)  
    
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4, 2.8, 4.15)
    glTexCoord2f(1.0, 0.0); glVertex3f(2.1, 2.8, 4.15)
    glTexCoord2f(0.5, 1.0); glVertex3f(1.2, 1.6, 4.15)
    glEnd()

def draw_ventana_enfrente(texture1, texture2):
    glBindTexture(GL_TEXTURE_2D, texture1)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 4, 4.1)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 4, 4.1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 6, 4.1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 6, 4.1)
    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, texture2)
    glBegin(GL_QUADS)
    glColor3f(0.607, 0.031, 0.031)
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.8, 4.2, 4.12)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.8, 4.2, 4.12)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.8, 5.8, 4.12)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.8, 5.8, 4.12)
    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, texture1)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.1, 4, 4.14)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.1, 4, 4.14)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.1, 6, 4.14)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.1, 6, 4.14)
    glEnd()

def draw_ventana(ventana, texture1):
    """Dibuja una ventana en una cara específica de la casa"""
    glBindTexture(GL_TEXTURE_2D, texture1)
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.8, 1.0)  # Color celeste para la ventana

    if ventana == 1:
        # Izquierda
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.01, 1.5, 1)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.01, 1.5, 2.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.01, 3.5, 2.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.01, 3.5, 1)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.05, 1.7, 1.2)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.05, 1.7, 2.3)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.05, 3.2, 2.3)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.05, 3.2, 1.2)

    elif ventana == 2:
        # Ventana izquierda 2
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.01, 1.5, -1)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.01, 1.5, 0.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.01, 3.5, 0.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.01, 3.5, -1)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.05, 1.7, -0.8)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.05, 1.7, 0.3)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.05, 3.2, 0.3)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.05, 3.2, -0.8)

    elif ventana == 3:
        # Ventana en la cara izquierda
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.01, 1.5, -3)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.01, 1.5, -1.7)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.01, 3.5, -1.7)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.01, 3.5, -3)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.05, 1.7, -2.8)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.05, 1.7, -1.9)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.05, 3.2, -1.9)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.05, 3.2, -2.8)

    elif ventana == 4:
        # Ventana derecha 1
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.01, 1.5, -1)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.01, 1.5, -2.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.01, 3.5, -2.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.01, 3.5, -1)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.05, 1.7, -1.2)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.05, 1.7, -2.3)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.05, 3.2, -2.3)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.05, 3.2, -1.2)
        
    elif ventana == 5:
        # Ventana en la cara izquierda
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.01, 1.5, 1)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.01, 1.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.01, 3.5, -0.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.01, 3.5, 1)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.05, 1.7, 0.8)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.05, 1.7, -0.3)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.05, 3.2, -0.3)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.05, 3.2, 0.8)
        
    elif ventana == 6:
        # Ventana en la cara izquierda
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.01, 1.5, 3)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.01, 1.5, 1.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.01, 3.5, 1.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.01, 3.5, 3)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.05, 1.7, 2.8)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.05, 1.7, 1.7)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.05, 3.2, 1.7)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.05, 3.2, 2.8)

    glEnd()

def draw_granero(madera_texture, madera_blanca_texture, techo_texture):
    draw_base(madera_texture)
    draw_base2(madera_texture)
    draw_base3(madera_texture)
    draw_techo(techo_texture)
    draw_techo2(techo_texture)
    draw_puerta(madera_blanca_texture, madera_texture)    
    draw_ventana_enfrente(madera_blanca_texture, madera_texture)
    draw_ventana(1, madera_blanca_texture)
    draw_ventana(2, madera_blanca_texture)
    draw_ventana(3, madera_blanca_texture)
    draw_ventana(4, madera_blanca_texture)
    draw_ventana(5, madera_blanca_texture)
    draw_ventana(6, madera_blanca_texture)


def draw_ground():
    """Dibuja un plano para representar el suelo o calle"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()

def draw_scene(madera_texture, madera_blanca_texture, techo_texture, tierra_pasto_texture, madera_valla_texture, lodo_texture):
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

    # Dibujar las casas en diferentes posiciones
    positions = [
        (0, 0, 0)
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual       
        draw_granero(madera_texture, madera_blanca_texture, techo_texture)
        glPopMatrix()
        
    
        glPushMatrix()
        glTranslatef(-10, 0, 0)
        draw_corral_oveja(tierra_pasto_texture, madera_valla_texture)
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslatef(10, 0, 0)
        draw_corral_cerdo(tierra_pasto_texture, madera_valla_texture, lodo_texture)
        glPopMatrix()
        

    glTranslate(7, 0, 7)

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
    
    madera_texture = load_texture('madera_granero.jpg')
    madera_blanca_texture = load_texture('madera_blanca.jpg')
    techo_texture = load_texture('techo.jpg')
    tierra_pasto_texture = load_texture('tierra_pasto.jpg')
    madera_valla_texture = load_texture('madera_valla.jpg')
    lodo_texture = load_texture('lodo.jpg')
    

    # Configurar la función de callback para el teclado
    glfw.set_key_callback(window, key_callback)

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_scene(madera_texture, madera_blanca_texture, techo_texture, tierra_pasto_texture, madera_valla_texture, lodo_texture)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
