import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluSphere, gluCylinder, gluQuadricTexture
from PIL import Image
import sys
from math import sin, cos, pi
import math

# Variables globales para la cámara
camera_pos = [4.0, 3.0, 8.0]  # Posición de la cámara
camera_target = [0.0, 3.0, 0.0]  # Punto al que mira
camera_up = [0.0, 1.0, 0.0]  # Vector hacia arriba

# Variables para el movimiento
camera_speed = 0.2  # Velocidad de movimiento
keys = {}  # Diccionario para controlar el estado de las teclas

def load_texture(filename):
    """Carga una textura desde un archivo de imagen"""
    img = Image.open(filename)
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
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)



def draw_ground():
    """Dibuja un plano para representar el suelo"""
    glBegin(GL_QUADS)
    glVertex3f(-100, 0, 100)
    glVertex3f(100, 0, 100)
    glVertex3f(100, 0, -100)
    glVertex3f(-100, 0, -100)
    glEnd()

def draw_textured_quad(vertices, tex_coords, texture_id):
    """Dibuja un cuadrado con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for i in range(4):
        glTexCoord2f(*tex_coords[i])
        glVertex3f(*vertices[i])
    glEnd()

def draw_house(wall_texture, roof_texture, door_texture, window_texture):
    """Dibuja una casa con texturas"""
    # Paredes de la casa 
    walls = [
        ([-3.0, 0, 1], [3.0, 0, 1], [3.0, 3, 1], [-3.0, 3, 1]),  # Frente
        ([-3.0, 0, -1], [3.0, 0, -1], [3.0, 3, -1], [-3.0, 3, -1]),  # Atrás
        ([-3.0, 0, -1], [-3.0, 0, 1], [-3.0, 3, 1], [-3.0, 3, -1]),  # Izquierda
        ([3.0, 0, -1], [3.0, 0, 1], [3.0, 3, 1], [3.0, 3, -1])   # Derecha
    ]
    tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

    for wall in walls:
        draw_textured_quad(wall, tex_coords, wall_texture)

    # Techo 
    roof = [
        ([-3.5, 3, 1], [3.5, 3, 1], [0, 5, 0]),  # Frente
        ([-3.5, 3, -1], [3.5, 3, -1], [0, 5, 0]),  # Atrás
        ([-3.5, 3, -1], [-3.5, 3, 1], [0, 5, 0]),  # Izquierda
        ([3.5, 3, -1], [3.5, 3, 1], [0, 5, 0])   # Derecha
    ]
    glBindTexture(GL_TEXTURE_2D, roof_texture)
    glBegin(GL_TRIANGLES)
    for tri in roof:
        for vertex in tri:
            glTexCoord2f((vertex[0] + 3.5) / 7, (vertex[2] + 1) / 2)
            glVertex3f(*vertex)
    glEnd()

    # Puerta
    door = [(-0.5, 0, 1.01), (0.4, 0, 1.01), (0.4, 1.5, 1.01), (-0.5, 1.5, 1.01)]
    draw_textured_quad(door, tex_coords, door_texture)

    # Ventanas
    windows = [
        [(-1.8, 1.5, 1.01), (-0.9, 1.5, 1.01), (-0.9, 2.5, 1.01), (-1.8, 2.5, 1.01)],  # Izquierda
        [(0.9, 1.5, 1.01), (1.8, 1.5, 1.01), (1.8, 2.5, 1.01), (0.9, 2.5, 1.01)]   # Derecha
    ]
    for window in windows:
        draw_textured_quad(window, tex_coords, window_texture)
        
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
    
def draw_lodo(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1) 

    glTexCoord2f(0.0, 0.0); glVertex3f(-2, 0.01, 2)
    glTexCoord2f(1.0, 0.0); glVertex3f(2, 0.01, 2)
    glTexCoord2f(1.0, 1.0); glVertex3f(2, 0.01, -2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-2, 0.01, -2)
    glEnd()

    
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
    
    glTranslatef(0.6, 0.03,  0)   
    draw_lodo(lodo_texture)
    
    
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
    
def puerta_triangulo(texture2):    
    glBindTexture(GL_TEXTURE_2D, texture2)
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)    
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-2.3, 0.2, 4.15)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.2, 0.2, 4.15)
    glTexCoord2f(0.5, 1.0); glVertex3f(-1.35, 1.2, 4.15)
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
    
    position = [
        (0, 0, 0),
        (2.6, 0, 0),
        (-2.7, 3, 0),
        (-0.1, 3, 0),
        (0, 2.8, 0),
        (2.5, 2.8, 0),
        (-2.7, 0.1, 0),
        (0, 0.1, 0)
    ]
    
    # abajo
    for pos in position:
        if pos == (0, 0,  0) or pos == (2.6, 0,  0):
            glPushMatrix()
            glTranslatef(*pos)   
            puerta_triangulo(texture2)
            glPopMatrix()
        # arriba
        elif pos == (-2.7, 3, 0) or pos == (-0.1, 3, 0):
            glPushMatrix()
            glTranslatef(*pos)   
            glRotatef(180, 0.0, 0.0, 1.0)
            puerta_triangulo(texture2)
            glPopMatrix()
        # derecha
        elif pos == (0, 2.8, 0) or pos == (2.5, 2.8, 0):
            glPushMatrix()
            glTranslatef(*pos)   
            glRotatef(90, 0.0, 0.0, 1.0)
            puerta_triangulo(texture2)
            glPopMatrix()
        # izquierda
        elif pos == (-2.7, 0.1, 0) or pos == (0, 0.1, 0):
            glPushMatrix()
            glTranslatef(*pos)   
            glRotatef(270, 0.0, 0.0, 1.0)
            puerta_triangulo(texture2)
            glPopMatrix()

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

def draw_scene(wall_texture, roof_texture, door_texture, window_texture, madera_granero_texture, madera_blanca_texture, 
                   techo_granero_texture, tierra_pasto_texture, madera_valla_texture, lodo_texture):
    """Dibuja la escena completa"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],  # Posición de la cámara
              camera_target[0], camera_target[1], camera_target[2],  # Punto al que mira
              camera_up[0], camera_up[1], camera_up[2])  # Vector hacia arriba
    
    positions_casa = [
        (-5, 0, 25)
    ]
    for pos in positions_casa:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual    
        glRotatef(90, 0.0, 1.0, 0.0)   
        draw_house(wall_texture, roof_texture, door_texture, window_texture)
        glPopMatrix()
    
    positions_granero_corral = [
        (20, 0, 10),
        (10, 0, 10),
        (30, 0, 10)
    ]
    for pos in positions_granero_corral:
        if pos == (20, 0, 10):
            glPushMatrix()
            glTranslatef(*pos)  # Mover la casa a la posición actual       
            draw_granero(madera_granero_texture, madera_blanca_texture, techo_granero_texture)
            glPopMatrix()
        
        if pos == (10, 0, 10):
            glPushMatrix()
            glTranslatef(*pos)
            draw_corral_oveja(tierra_pasto_texture, madera_valla_texture)
            glPopMatrix()
        
        if pos == (30, 0, 10):
            glPushMatrix()
            glTranslatef(*pos)
            draw_corral_cerdo(tierra_pasto_texture, madera_valla_texture, lodo_texture)
            glPopMatrix()

    draw_ground()  # Dibuja el suelo

    glfw.swap_buffers(window)


def process_input():
    """Procesa el estado de las teclas para mover la cámara"""
    global camera_pos

    if keys.get(glfw.KEY_W, False):  # Mover hacia adelante
        camera_pos[2] -= camera_speed
    if keys.get(glfw.KEY_S, False):  # Mover hacia atrás
        camera_pos[2] += camera_speed
    if keys.get(glfw.KEY_A, False):  # Mover a la izquierda
        camera_pos[0] -= camera_speed
    if keys.get(glfw.KEY_D, False):  # Mover a la derecha
        camera_pos[0] += camera_speed
    if keys.get(glfw.KEY_UP, False):  # Subir
        camera_pos[1] += camera_speed
    if keys.get(glfw.KEY_DOWN, False):  # Bajar
        camera_pos[1] -= camera_speed


def key_callback(window, key, scancode, action, mods):
    """Actualiza el estado de las teclas"""
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Mover Escena Completa", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    wall_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\pared.jpg") #paredes
    roof_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\teja_cafe.jpeg") #tejado
    door_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\puerta.jpg") #puerta
    window_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\ventanas.jpeg") #ventanas

    madera_granero_texture = load_texture('madera_granero.jpg')
    madera_blanca_texture = load_texture('madera_blanca.jpg')
    techo_granero_texture = load_texture('techo.jpg')
    tierra_pasto_texture = load_texture('tierra_pasto.jpg')
    madera_valla_texture = load_texture('madera_valla.jpg')
    lodo_texture = load_texture('lodo.jpg')
    
    # Configurar callback de teclado
    glfw.set_key_callback(window, key_callback)

    # Bucle principal
    while not glfw.window_should_close(window):
        process_input()  # Procesar teclas presionadas
        draw_scene(wall_texture, roof_texture, door_texture, window_texture, madera_granero_texture, madera_blanca_texture, 
                   techo_granero_texture, tierra_pasto_texture, madera_valla_texture, lodo_texture)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()