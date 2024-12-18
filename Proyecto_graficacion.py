import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import sys
from math import sin, cos, pi
import math


import numpy as np
import cv2 as cv

# Variables globales para la cámara
camera_pos = [4.0, 35.0, 30.0]  # Posición de la cámara
camera_target = [3.0, 35.0, 30.0]  # Punto al que mira
camera_up = [0.0, 1.0, 0.0]  # Vector hacia arriba

# Variables para el movimiento
camera_speed = 0.2  # Velocidad de movimiento
keys = {}  # Diccionario para controlar el estado de las teclas

def load_texture(filename):
    img = Image.open(filename).convert('RGB')
    img_data = img.tobytes("raw", "RGB", 0, -1)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    # Utilizar mipmaps
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

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
    glColor3f(0.364, 0.690, 0.066)  
    glVertex3f(-50, 0, 70)
    glVertex3f(50, 0, 70)
    glVertex3f(50, 0, -50)
    glVertex3f(-50, 0, -50)
    glEnd()
    
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.6, 0.4)  
    glVertex3f(0, 0.1, 15)
    glVertex3f(40, 0.1, 15)
    glVertex3f(40, 0.1, 20)
    glVertex3f(0, 0.1, 20)
    glEnd()
    
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.6, 0.4)  
    glVertex3f(0, 0.1, 15)
    glVertex3f(10, 0.1, 15)
    glVertex3f(10, 0.1, 45)
    glVertex3f(0, 0.1, 45)
    glEnd()

def draw_textured_quad(vertices, tex_coords, texture_id):
    """Dibuja un cuadrado con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  
    for i in range(4):
        glTexCoord2f(*tex_coords[i])
        glVertex3f(*vertices[i])
    glEnd()

def draw_house(wall_texture, roof_texture, door_texture, window_texture):
    """Dibuja una casa con texturas"""
    # Paredes de la casa 
    walls = [
        ([-3.0, 0, 3.0], [3.0, 0, 3.0], [3.0, 3, 3.0], [-3.0, 3, 3.0]),  # Frente
        ([-3.0, 0, -3.0], [3.0, 0, -3.0], [3.0, 3, -3.0], [-3.0, 3, -3.0]),  # Atrás
        ([-3.0, 0, -3.0], [-3.0, 0, 3.0], [-3.0, 3, 3.0], [-3.0, 3, -3.0]),  # Izquierda
        ([3.0, 0, -3.0], [3.0, 0, 3.0], [3.0, 3, 3.0], [3.0, 3, -3.0])   # Derecha
    ]
    tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

    for wall in walls:
        draw_textured_quad(wall, tex_coords, wall_texture)

    # Techo (ajustado para coincidir con el ancho y largo)
    roof = [
        ([-3.5, 3, 3.5], [3.5, 3, 3.5], [0, 5, 0]),  # Frente
        ([-3.5, 3, -3.5], [3.5, 3, -3.5], [0, 5, 0]),  # Atrás
        ([-3.5, 3, -3.5], [-3.5, 3, 3.5], [0, 5, 0]),  # Izquierda
        ([3.5, 3, -3.5], [3.5, 3, 3.5], [0, 5, 0])   # Derecha
    ]
    glBindTexture(GL_TEXTURE_2D, roof_texture)
    glBegin(GL_TRIANGLES)
    for tri in roof:
        for vertex in tri:
            glTexCoord2f((vertex[0] + 3.5) / 7, (vertex[2] + 3.5) / 7)
            glVertex3f(*vertex)
    glEnd()

    # Puerta (sin cambios)
    door = [(-0.5, 0, 3.01), (0.4, 0, 3.01), (0.4, 1.5, 3.01), (-0.5, 1.5, 3.01)]
    draw_textured_quad(door, tex_coords, door_texture)

    # Ventanas (ajustadas a la nueva profundidad)
    windows = [
        [(-1.8, 1.5, 3.01), (-0.9, 1.5, 3.01), (-0.9, 2.5, 3.01), (-1.8, 2.5, 3.01)],  # Izquierda
        [(0.9, 1.5, 3.01), (1.8, 1.5, 3.01), (1.8, 2.5, 3.01), (0.9, 2.5, 3.01)]   # Derecha
    ]
    for window in windows:
        draw_textured_quad(window, tex_coords, window_texture)

def draw_cobertizo(textura_pared, textura_techo, textura_puerta):
    """Dibuja una casa cuadrada más pequeña con paredes, techo plano y puerta"""
    coord_texturas = [(0, 0), (1, 0), (1, 1), (0, 1)]  # Coordenadas de textura

    # Paredes de la casa
    paredes = [
        ([-1.8, 0, 1.8], [1.8, 0, 1.8], [1.8, 1.8, 1.8], [-1.8, 1.8, 1.8]),  # Frente
        ([-1.8, 0, -1.8], [1.8, 0, -1.8], [1.8, 1.8, -1.8], [-1.8, 1.8, -1.8]),  # Atrás
        ([-1.8, 0, -1.8], [-1.8, 0, 1.8], [-1.8, 1.8, 1.8], [-1.8, 1.8, -1.8]),  # Izquierda
        ([1.8, 0, -1.8], [1.8, 0, 1.8], [1.8, 1.8, 1.8], [1.8, 1.8, -1.8])  # Derecha
    ]
    for pared in paredes:
        draw_textured_quad(pared, coord_texturas, textura_pared)

    # Techo plano
    techo = [
        [-2.0, 1.8, -2.0],  # Esquina trasera izquierda
        [-2.0, 1.8, 2.0],   # Esquina frontal izquierda
        [2.0, 1.8, 2.0],    # Esquina frontal derecha
        [2.0, 1.8, -2.0]    # Esquina trasera derecha
    ]
    draw_textured_quad(techo, coord_texturas, textura_techo)

    # Puerta
    puerta = [(-0.4, 0, 1.81), (0.4, 0, 1.81), (0.4, 1.2, 1.81), (-0.4, 1.2, 1.81)]  # Puerta
    draw_textured_quad(puerta, coord_texturas, textura_puerta)        
        
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

def draw_cylinder(texture):
    """Dibuja un cilindro usando gluCylinder"""
    glColor3f(1.0, 1.0, 1.0) 
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura
    quad = gluNewQuadric()                    # Crea el objeto cuadrático
    gluQuadricTexture(quad, GL_TRUE)          # Habilita las coordenadas de textura                 # Asegura el color blanco
    gluCylinder(quad, 2, 2, 15.0, 32, 32)  # (obj, base, top, height, slices, stacks)
    gluDeleteQuadric(quad)   

    
def draw_sphere(texture):
    """Dibuja una esfera utilizando gluSphere."""
    glColor3f(1.0, 1.0, 1.0)    
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura
    quad = gluNewQuadric()                   # Crea el objeto cuadrático
    gluQuadricTexture(quad, GL_TRUE)         # Habilita las coordenadas de textura             # Asegura el color blanco para mostrar la textura
    gluSphere(quad, 2.0, 32, 32)             # Dibuja la esfera
    gluDeleteQuadric(quad)  
    
def entrada_silo(texture, texture2):
    glColor3f(1.0, 1.0, 1.0) 
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura
    glBegin(GL_QUADS)
    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1, 3, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 3, -3)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(1, 0, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, 1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 3, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(1, 3, -3)
    glEnd()
    
    glColor3f(1.0, 1.0, 1.0) 
    glBindTexture(GL_TEXTURE_2D, texture2)
    glBegin(GL_QUADS)
    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.5, 3, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 3, -3)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 3, 1.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.5, 3, 1.5)
    glEnd()
    
def escalera(texture):
    glColor3f(1.0, 1.0, 1.0)  
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-0, 0, -0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0, 0, 0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.2, 15, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0., 15, -0)
    glEnd()
    
def draw_silo(metal_silo_texture, metal_silo2_texture):
    
    glPushMatrix()
    glTranslatef(5.0, 15.0, -10.0)
    glRotatef(90, 1.0, 0.0, 0.0)
    draw_cylinder(metal_silo2_texture)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(5.0, 15.0, -10.0)
    glRotatef(90, 1.0, 0.0, 0.0)
    draw_sphere(metal_silo_texture)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(5.0, 0.0, -5.5)
    entrada_silo(metal_silo2_texture, metal_silo_texture)
    glPopMatrix()
    
    positions = [
        (7, 0, -8.5),
        (7, 0, -8)
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(180, 0.0, 1.0, 0.0)
        escalera(metal_silo_texture)
        glPopMatrix()

def draw_suelo(texture_id):
    """Dibuja el campo de cultivo de vegetales con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, 0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, 0.5)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, -0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, -0.5)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, -0.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(1, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(1, 0.5, -0.5)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0.5, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0.5, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, 0.5)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0, 0.5)

    glEnd()

def draw_vegetal(texture_id):
    """Dibuja un vegetal con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id) # Vincula la textura
    glColor3f(1.0, 1.0, 1.0) # Color blanco para la textura
    # Dibujar tallo
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    glPushMatrix()
    glTranslatef(0.0, 0.25, 0.0)
    gluCylinder(quad, 0.05, 0.05, 0.5, 32, 32)
    glPopMatrix()

    # Dibujar hojas (esferas)
    glPushMatrix()
    glTranslatef(0.0, 0.75, 0.0)
    gluSphere(quad, 0.1, 32, 32)
    glTranslatef(0.1, 0.1, 0.0)
    gluSphere(quad, 0.1, 32, 32)
    glTranslatef(-0.2, 0.1, 0.0)
    gluSphere(quad, 0.1, 32, 32)
    glPopMatrix()

def draw_huerto(suelo_texture, vegetal_texture):
    """Dibuja un huerto de vegetales con campos de cultivo"""
    glPushMatrix()

    # Primera Fila
    glTranslatef(3, 0, 0)
    for i in range(3):
        draw_suelo(suelo_texture)
        glPushMatrix()
        glTranslatef(0.4, 0, 0)
        draw_vegetal(vegetal_texture)
        glPopMatrix()
        glTranslatef(-0.4, 0, 0)

    # Segunda Fila
    glTranslatef(0, 0, 1.5)
    for i in range(3):
        draw_suelo(suelo_texture)
        glPushMatrix()
        glTranslatef(0.4, 0, 0)
        draw_vegetal(vegetal_texture)
        glPopMatrix()
        glTranslatef(-0.4, 0, 0)

    glPopMatrix()
    
def draw_trunk(texture_id):
    """Dibuja el tronco del árbol como un cilindro con textura."""
    glPushMatrix()
    glColor3f(1, 1, 1)  
    glTranslatef(0.0, 0.0, 0.0)  
    glRotatef(-90, 1, 0, 0)  

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)  
    glPopMatrix()

def draw_foliage():
    """Dibuja las hojas del árbol como una esfera."""
    glPushMatrix()
    glColor3f(0.1, 0.8, 0.1)  
    glTranslatef(0.0, 2.0, 0.0)  
    quadric = gluNewQuadric()
    gluSphere(quadric, 1.0, 32, 32)  
    glPopMatrix()

def draw_apples():
    """Dibuja pequeñas esferas rojas representando manzanas."""
    glColor3f(1.0, 0.0, 0.0)  
    quadric = gluNewQuadric()

    apple_positions = [
        (0.5, 2.5, 0.3),
        (-0.4, 2.3, -0.5),
        (0.3, 2.7, -0.2),
        (-0.2, 2.8, 0.6),
        (0.6, 2.6, -0.4),
        (-0.5, 2.4, 0.5)
    ]

    for pos in apple_positions:
        glPushMatrix()
        glTranslatef(*pos)  
        gluSphere(quadric, 0.1, 16, 16)  
        glPopMatrix()

def draw_manzano(texture_id):
    """Dibuja un manzano completo."""
    glPushMatrix()
    draw_trunk(texture_id)  
    draw_foliage()
    draw_apples()
    glPopMatrix()

def draw_tallo_fresal():
    """Dibuja el tallo de la planta"""
    glPushMatrix()
    glColor3f(0.4, 0.8, 0.2)  # Verde claro para el tallo
    glTranslatef(0.0, 0.0, 0.0)  # Posicionar el tallo
    glRotatef(-90, 1, 0, 0)  # Rota para orientar el cilindro verticalmente
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.05, 0.05, 0.5, 32, 32)  # Tallos delgados
    glPopMatrix()

def draw_hojas_fresal():
    """Dibuja las hojas de la planta como esferas pequeñas"""
    glColor3f(0.1, 0.5, 0.1)  # Verde oscuro para las hojas
    quadric = gluNewQuadric()
    
    leaf_positions = [
        (0.2, 0.5, 0.0),   # Derecha
        (-0.2, 0.5, 0.0),  # Izquierda
        (0.0, 0.5, 0.2),   # Adelante
        (0.0, 0.5, -0.2),  # Atrás
    ]
    
    for x, y, z in leaf_positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        gluSphere(quadric, 0.2, 32, 32)  # Tamaño de las hojas
        glPopMatrix()

def draw_fresas():
    """Dibuja las fresas como pequeñas esferas rojas"""
    glColor3f(1.0, 0.0, 0.0)  # Rojo para las fresas
    quadric = gluNewQuadric()
    
    strawberry_positions = [
        (0.15, 0.3, 0.1),
        (-0.1, 0.35, -0.1),
        (0.05, 0.4, -0.15),
        (-0.15, 0.3, 0.05),
    ]
    
    for x, y, z in strawberry_positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        gluSphere(quadric, 0.1, 32, 32)  # Tamaño de las fresas
        glPopMatrix()

def draw_fresal():
    """Dibuja una planta de fresas completa"""
    glPushMatrix()
    draw_tallo_fresal()           # Dibuja el tallo
    draw_hojas_fresal()         # Dibuja las hojas
    draw_fresas()   # Dibuja las fresas
    glPopMatrix()

def draw_textured_trunk(texture_id):
    """Dibuja el tronco del pino con textura."""
    glPushMatrix()
    glColor3f(1, 1, 1)  
    glTranslatef(0.0, 0.0, 0.0)  
    glRotatef(-90, 1, 0, 0)  

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    gluCylinder(quadric, 0.75, 0.25, 5.0, 32, 32)  # Aumentado 2.5 veces
    glPopMatrix()

def draw_foliage_pine():
    """Dibuja el follaje del pino como conos apilados"""
    glColor3f(0.1, 0.6, 0.1)  # Verde oscuro para el follaje
    quadric = gluNewQuadric()

    # Dibujar tres conos de diferentes tamaños
    foliage_levels = [
        (1.5, 3.0, 2.0),  # (Radio base, Altura, Traslación en Y)
        (1.0, 2.5, 4.0),
        (0.5, 2.0, 6.0),
    ]
    
    for base, height, y_translation in foliage_levels:
        glPushMatrix()
        glTranslatef(0.0, y_translation, 0.0)  # Elevar cada cono
        glRotatef(-90, 1, 0, 0)  # Rota para orientar el cono verticalmente
        gluCylinder(quadric, base, 0.0, height, 32, 32)  # Base más grande y punta cerrada
        glPopMatrix()

def draw_pine(texture_id):
    """Dibuja un pino completo."""
    glPushMatrix()
    glScalef(2.5, 2.5, 2.5)  # Escalar todo el pino 2.5 veces
    draw_textured_trunk(texture_id)
    draw_foliage_pine()
    glPopMatrix()


def draw_caja_base_panal(textura_id):
    """ Dibuja las bases donde se colocaran los panales para asimilar una zona de Apicultura"""
    glBindTexture(GL_TEXTURE_2D, textura_id) #  Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # blanco para no alterar la textura

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, 0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 1, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 1, 0.5)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 1, -0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 1, -0.5)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.4, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.4, 1, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 1, -0.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 1, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.4, 1, -0.5)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 1, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 1, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 1, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 1, 0.5)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0, 0.5)
    glEnd()

def draw_base_inferior_panal(textura_id):
    """ Dibuja la base inferior de los panales"""
    glBindTexture(GL_TEXTURE_2D, textura_id) #  Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, -0.15, 0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, -0.15, 0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, 0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, 0.15, 0.3)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, 0.15, -0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, 0.15, -0.3)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.3, -0.15, 0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.3, 0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, 0.15, -0.3)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, -0.15, 0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, 0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.3, 0.15, -0.3)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, 0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, 0.15, -0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, 0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, 0.15, 0.3)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, -0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, -0.15, 0.3)
    glEnd()

def draw_base_intermedia_panal(textura_id):
    """ Dibuja la base intermedia de los panales"""
    glBindTexture(GL_TEXTURE_2D, textura_id) #  Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, 0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, 0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0.25, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0.25, 0.4)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, -0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0.25, -0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0.25, -0.4)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.4, 0, 0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.4, 0.25, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0.25, -0.4)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4, 0, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, 0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0.25, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.4, 0.25, -0.4)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0.25, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0.25, -0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0.25, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0.25, 0.4)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, -0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0, 0.4)
    glEnd()

def draw_base_superior_panal(textura_id):
    """ Dibuja la base superior de los panales"""
    glBindTexture(GL_TEXTURE_2D, textura_id) #  Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0, 0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.25, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.25, 0.5)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.25, -0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.25, -0.5)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.5, 0.25, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.25, -0.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.5, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.25, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.5, 0.25, -0.5)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0.25, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0.25, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.25, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.25, 0.5)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0, 0.5)
    glEnd()

def draw_panal(textura_id):
    draw_base_inferior_panal(textura_id)
    glTranslatef(0, 0.1, 0)
    draw_base_intermedia_panal(textura_id)
    glTranslatef(0, 0.2, 0)
    draw_base_superior_panal(textura_id)
    glTranslatef(0, 0.2, 0)
    draw_base_superior_panal(textura_id)
    glTranslatef(0, 0.2, 0)
    draw_base_intermedia_panal(textura_id)
    glTranslatef(0, 0.3, 0)
    draw_base_inferior_panal(textura_id)

def draw_zona_apicultura(base_panal_texturas, panal_texturas):
    """ Dibuja la zona de apicultura"""
    glPushMatrix()
    draw_caja_base_panal(base_panal_texturas)
    glTranslatef(0, 1.1, 0)
    draw_panal(panal_texturas)
    glPopMatrix()

def draw_techo_invernadero(textura_id):
    """Dibuja el techo completo del invernadero con texturas"""
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor4f(0.5, 0.9, 1.0, 0.6)  # Vidrio translúcido
    # Triángulos laterales (izquierdo y derecho)
    glBegin(GL_TRIANGLES)
    # Lado izquierdo
    glTexCoord2f(0.0, 0.0)  # Coordenadas de textura para cada vértice
    glVertex3f(-2, 2, -2)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-2, 2, 2)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0, 3, 0)
    # Lado derecho
    glTexCoord2f(0.0, 0.0)
    glVertex3f(2, 2, -2)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2, 2, 2)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0, 3, 0)
    glEnd()
    # Planos inclinados frontal y trasero
    glBegin(GL_QUADS)
    # Plano frontal
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-2, 2, 2)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2, 2, 2)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0, 3, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-2, 2, 2)
    # Plano trasero
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-2, 2, -2)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2, 2, -2)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0, 3, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-2, 2, -2)
    glEnd()
def draw_puerta_invernadero(textura_id):
    """Dibuja la puerta del invernadero con texturas"""
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor4f(0.5, 0.9, 1.0, 0.8)  # Vidrio ligeramente más opaco
    # Panel de vidrio de la puerta
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)  # Coordenadas de textura
    glVertex3f(-0.5, 0.0, 2)  # Parte inferior izquierda
    glTexCoord2f(1.0, 0.0)
    glVertex3f(0.5, 0.0, 2)   # Parte inferior derecha
    glTexCoord2f(1.0, 1.0)
    glVertex3f(0.5, 1.5, 2)   # Parte superior derecha
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-0.5, 1.5, 2)  # Parte superior izquierda
    glEnd()
    # Marco de la puerta (no tiene textura)
    glColor3f(0.3, 0.3, 0.3)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(-0.5, 0.0, 2)
    glVertex3f(-0.5, 1.5, 2)
    glVertex3f(0.5, 0.0, 2)
    glVertex3f(0.5, 1.5, 2)
    glVertex3f(-0.5, 1.5, 2)
    glVertex3f(0.5, 1.5, 2)
    glEnd()
def draw_paredes_invernadero(textura_id):
    """Dibuja todas las paredes del invernadero con texturas"""
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor4f(0.5, 0.9, 1.0, 0.6)  # Vidrio translúcido
    # Paredes laterales
    glBegin(GL_QUADS)
    # Lado izquierdo
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-2, 0.0, -2)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-2, 2, -2)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-2, 2, 2)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-2, 0.0, 2)
    # Lado derecho
    glTexCoord2f(0.0, 0.0)
    glVertex3f(2, 0.0, -2)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2, 2, -2)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(2, 2, 2)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(2, 0.0, 2)
    glEnd()
    # Pared trasera
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-2, 0.0, -2)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2, 0.0, -2)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(2, 2, -2)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-2, 2, -2)
    glEnd()
    # Pared frontal
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-2, 0.0, 2)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2, 0.0, 2)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(2, 2, 2)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-2, 2, 2)
    glEnd()
def draw_greenhouse(texture_pared_invernadero, texture_techo_invernadero, door_texture):
    """Dibuja un invernadero completo con diferentes texturas"""
    glPushMatrix()
    draw_paredes_invernadero(texture_pared_invernadero)  # Textura para paredes
    draw_techo_invernadero(texture_techo_invernadero)    # Textura para techo
    draw_puerta_invernadero(door_texture)  # Textura para puerta
    glPopMatrix()

"""
def draw_scene(wall_texture, roof_texture, door_texture, window_texture, madera_granero_texture, madera_blanca_texture, 
                   techo_granero_texture, tierra_pasto_texture, madera_valla_texture, lodo_texture, suelo_texture, vegetal_texture,
                   texture_troncoManzano, base_panal_texturas, panal_texturas, metal_silo_texture, metal_silo2_texture, textura_pared, 
                   textura_techo, textura_puerta, texture_pared_invernadero, texture_techo_invernadero):
    #Dibuja la escena completa
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
    
    position_cobertizo = (-5, 0, 18)
    glPushMatrix()
    glTranslatef(*position_cobertizo)  # Mover la casa a la posición actual
    glRotatef(90, 0.0, 1.0, 0.0)       
    draw_cobertizo(textura_pared, textura_techo, textura_puerta)
    glPopMatrix()
    
    position_granero = (20, 0, 10)
    glPushMatrix()
    glTranslatef(*position_granero)  # Mover la casa a la posición actual       
    draw_granero(madera_granero_texture, madera_blanca_texture, techo_granero_texture)
    glPopMatrix()
    
    position_corral1 = (10, 0, 10)
    glPushMatrix()
    glTranslatef(*position_corral1)
    draw_corral_oveja(tierra_pasto_texture, madera_valla_texture)
    glPopMatrix()
    
    position_corral2 = (30, 0, 10)
    glPushMatrix()
    glTranslatef(*position_corral2)
    draw_corral_cerdo(tierra_pasto_texture, madera_valla_texture, lodo_texture)
    glPopMatrix()
    
    position_silo = (15, 0, 11)
    glPushMatrix()
    glTranslatef(*position_silo)
    draw_silo(metal_silo_texture, metal_silo2_texture)   
    glPopMatrix()


    positions_huerto = [
        (40, -0.35, 40), (40, -0.35, 44), (40, -0.35, 48), (40, -0.35, 52),
        (36, -0.35, 40), (36, -0.35, 44), (36, -0.35, 48), (36, -0.35, 52),
        (32, -0.35, 40), (32, -0.35, 44), (32, -0.35, 48), (32, -0.35, 52)
    ]            
    for pos in positions_huerto:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual     
        draw_huerto(suelo_texture, vegetal_texture)
        glPopMatrix()


    positions_manzano = [
        (27, 0, 40), (27, 0, 44), (27, 0, 48), (27, 0, 52),
        (23, 0, 40), (23, 0, 44), (23, 0, 48), (23, 0, 52), 
        (19, 0, 40), (19, 0, 44), (19, 0, 48), (19, 0, 52)
    ]

    for pos in positions_manzano:
        glPushMatrix()
        glTranslatef(*pos)
        draw_manzano(texture_troncoManzano)
        glPopMatrix()

    positions_fresal = [
        (40, 0, 27), (40, 0, 25), (40, 0, 23), 
        (38, 0, 27), (38, 0, 25), (38, 0, 23),
        (36, 0, 27), (36, 0, 25), (36, 0, 23),
        (34, 0, 27), (34, 0, 25), (34, 0, 23),
        (32, 0, 27), (32, 0, 25), (32, 0, 23),
        (30, 0, 27), (30, 0, 25), (30, 0, 23),
    ]

    for pos in positions_fresal:
        glPushMatrix()
        glTranslatef(*pos)
        draw_fresal()
        glPopMatrix()

    positions_pino = [
       (-16, 0, -36),
        (45, 0, 21),(-1,0,40)
    ]

    for pos in positions_pino:
        glPushMatrix()
        glTranslatef(*pos)
        draw_pine(texture_troncoManzano)
        glPopMatrix()

    positions_base_panal = [
        (30, 0, 40), (30, 0, 44), (30, 0, 48), (30, 0, 52)
    ]

    for pos in positions_base_panal:
        glPushMatrix()
        glTranslatef(*pos)
        draw_zona_apicultura(base_panal_texturas, panal_texturas)
        glPopMatrix()
    
    positions_invernadero = [
        (2, 0, 9)
    ]

    for pos in positions_invernadero:
        glPushMatrix()
        glTranslatef(*pos)
        draw_greenhouse(texture_pared_invernadero, texture_techo_invernadero, door_texture)
        glPopMatrix()

    

    draw_ground()  # Dibuja el suelo

    glfw.swap_buffers(window)

"""
    
def draw_scene(
    texture, pollito_pos, vaca_texture, angulo_rot, cerdito_texture, vaca_patas, vaca_cara,
    wall_texture, roof_texture, door_texture, window_texture, madera_granero_texture, madera_blanca_texture,
    techo_granero_texture, tierra_pasto_texture, madera_valla_texture, lodo_texture, suelo_texture, vegetal_texture,
    texture_troncoManzano, base_panal_texturas, panal_texturas, metal_silo_texture, metal_silo2_texture, textura_pared,
    textura_techo, textura_puerta, texture_pared_invernadero, texture_techo_invernadero
):
    """Dibuja la escena completa combinando ambas funcionalidades"""

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara (usando la configuración de la segunda función)
    gluLookAt(
        eje_x, eje_y, eje_z,
        eje_x + center_x, eje_y + center_y, eje_z + center_z,
        0.0, 1.0, 0.0
    )    # Vector hacia arriba
      # Vector hacia arriba

    # ----------------------------------------------------
    # Sección proveniente de la segunda función:
    # Dibujo de casas, granero, cobertizo, corrales, silo, huerto, manzanos, fresales, pinos, apicultura, invernadero
    # ----------------------------------------------------
    
    positions_casa = [
        (-5, 0, 25)
    ]
    for pos in positions_casa:
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(90, 0.0, 1.0, 0.0)
        draw_house(wall_texture, roof_texture, door_texture, window_texture)
        glPopMatrix()
    
    position_cobertizo = (-5, 0, 18)
    glPushMatrix()
    glTranslatef(*position_cobertizo)
    glRotatef(90, 0.0, 1.0, 0.0)
    draw_cobertizo(textura_pared, textura_techo, textura_puerta)
    glPopMatrix()
    
    position_granero = (20, 0, 10)
    glPushMatrix()
    glTranslatef(*position_granero)
    draw_granero(madera_granero_texture, madera_blanca_texture, techo_granero_texture)
    glPopMatrix()
    
    position_corral1 = (10, 0, 10)
    glPushMatrix()
    glTranslatef(*position_corral1)
    draw_corral_oveja(tierra_pasto_texture, madera_valla_texture)
    glPopMatrix()
    
    position_corral2 = (30, 0, 10)
    glPushMatrix()
    glTranslatef(*position_corral2)
    draw_corral_cerdo(tierra_pasto_texture, madera_valla_texture, lodo_texture)
    glPopMatrix()
    
    position_silo = (15, 0, 11)
    glPushMatrix()
    glTranslatef(*position_silo)
    draw_silo(metal_silo_texture, metal_silo2_texture)
    glPopMatrix()
    
    positions_huerto = [
        (40, -0.35, 40), (40, -0.35, 44), (40, -0.35, 48), (40, -0.35, 52),
        (36, -0.35, 40), (36, -0.35, 44), (36, -0.35, 48), (36, -0.35, 52),
        (32, -0.35, 40), (32, -0.35, 44), (32, -0.35, 48), (32, -0.35, 52)
    ]
    for pos in positions_huerto:
        glPushMatrix()
        glTranslatef(*pos)
        draw_huerto(suelo_texture, vegetal_texture)
        glPopMatrix()

    positions_manzano = [
        (27, 0, 40), (27, 0, 44), (27, 0, 48), (27, 0, 52),
        (23, 0, 40), (23, 0, 44), (23, 0, 48), (23, 0, 52),
        (19, 0, 40), (19, 0, 44), (19, 0, 48), (19, 0, 52)
    ]
    for pos in positions_manzano:
        glPushMatrix()
        glTranslatef(*pos)
        draw_manzano(texture_troncoManzano)
        glPopMatrix()

    positions_fresal = [
        (40, 0, 27), (40, 0, 25), (40, 0, 23),
        (38, 0, 27), (38, 0, 25), (38, 0, 23),
        (36, 0, 27), (36, 0, 25), (36, 0, 23),
        (34, 0, 27), (34, 0, 25), (34, 0, 23),
        (32, 0, 27), (32, 0, 25), (32, 0, 23),
        (30, 0, 27), (30, 0, 25), (30, 0, 23),
    ]
    for pos in positions_fresal:
        glPushMatrix()
        glTranslatef(*pos)
        draw_fresal()
        glPopMatrix()
    positions_pino = [
        (-16, 0, -36), (-20, 0, -31), (-25, 0, -36), (-30, 0, -31), (-35, 0, -36), (-40, 0, -31),
        (-16, 0, -36), (-11, 0, -31), (-6, 0, -36), (-1, 0, -31), (4, 0, -36), 
        (9, 0, -31), (14, 0, -36), (19, 0, -31), (24, 0, -36), (29, 0, -31), 
        (34, 0, -36), (39, 0, -31), (44, 0, -36), (49, 0, -31),
        
        # Primera fila
        (-16, 0, -36), (-20, 0, -31), (-25, 0, -36), (-30, 0, -31), (-35, 0, -36),
        # Segunda fila
        (-16, 0, -21), (-20, 0, -26), (-25, 0, -21), (-30, 0, -26), (-35, 0, -21),
        # Tercera fila
        (-16, 0, -6), (-20, 0, -11), (-25, 0, -6), (-30, 0, -11), (-35, 0, -6),
        # Cuarta fila
        (-16, 0, 9), (-20, 0, 4), (-25, 0, 9), (-30, 0, 4), (-35, 0, 9),
        # Quinta fila
        (-16, 0, 24), (-20, 0, 19), (-25, 0, 24), (-30, 0, 19), (-35, 0, 24),
        # Sexta fila
        (-16, 0, 39), (-20, 0, 34), (-25, 0, 39), (-30, 0, 34), (-35, 0, 39),
        # Séptima fila
        (-16, 0, 54), (-20, 0, 49), (-25, 0, 54), (-30, 0, 49), (-35, 0, 54),
        # Octava fila
        (-16, 0, 69), (-20, 0, 64),

        
        
        (-16, 0, 60), (-20, 0, 62), (-25, 0, 60), (-30, 0, 62), (-35, 0, 60), (-40, 0, 62),
        (-16, 0, 60), (-11, 0, 62), (-6, 0, 60), (-1, 0, 62), (4, 0, 60), 
        (9, 0, 62), (14, 0, 60), (19, 0, 62), (24, 0, 60), (29, 0, 62), 
        (34, 0, 60), (39, 0, 62), (44, 0, 60), (49, 0, 62),
        (45, 0, 21), (-10, 0, 35)
    ]

    for pos in positions_pino:
        glPushMatrix()
        glTranslatef(*pos)
        draw_pine(texture_troncoManzano)
        glPopMatrix()

    positions_base_panal = [
        (30, 0, 40), (30, 0, 44), (30, 0, 48), (30, 0, 52)
    ]
    for pos in positions_base_panal:
        glPushMatrix()
        glTranslatef(*pos)
        draw_zona_apicultura(base_panal_texturas, panal_texturas)
        glPopMatrix()

    positions_invernadero = [
        (2, 0, 9)
    ]
    for pos in positions_invernadero:
        glPushMatrix()
        glTranslatef(*pos)
        draw_greenhouse(texture_pared_invernadero, texture_techo_invernadero, door_texture)
        glPopMatrix()

    

    # Dibujar el suelo (de la segunda función)
    draw_ground()

    # ----------------------------------------------------
    # Sección proveniente de la primera función:
    # Dibujo del tractor, pollito, vaca y cerdito.
    # Se asume que las posiciones pueden ser ajustadas según la escena.
    # ----------------------------------------------------

    glPushMatrix()
    # Ajustar la posición del tractor para que no choque con el resto de la escena
    glTranslatef(-2, 0, 0)  
    chicken_tractor(texture)
    glPopMatrix()


    draw_pollito(pollito_pos, angulo_rot)
    
    # Dibujo del pollito
    draw_pollito_estatico((0, 0, 1))


    # Posicionamiento y dibujo de la vaca y el cerdito
    positions_vacas = [
        (10, 0, 9), (13, 0 ,12), (8, 0, 9)
    ]
    for pos in positions_vacas:
        if pos == (10, 0, 9):
            glPushMatrix()
            glTranslatef(*pos)
            vaca(vaca_texture, vaca_patas, vaca_cara)
            glPopMatrix()
            
        if pos == (8, 0, 9):
            glPushMatrix()
            glTranslatef(*pos)
            glRotatef(90, 0.0, 1.0, 0.0)
            vaca(vaca_texture, vaca_patas, vaca_cara)
            glPopMatrix()
            
        if pos == (13, 0 ,12):
            glPushMatrix()
            glTranslatef(*pos)
            glRotatef(270, 0.0, 1.0, 0.0)
            vaca(vaca_texture, vaca_patas, vaca_cara)
            glPopMatrix()

    positions_cerdos = [
        (30, 0, 11), (33, 0, 8), (29, 0, 8)
    ]
    for pos in positions_cerdos:
        if pos == (30, 0,11):
            glPushMatrix()
            glTranslatef(*pos)
            glRotatef(90, 0.0, 1.0, 0.0)
            cerdito(cerdito_texture)
            glPopMatrix()
            
        if pos == (33, 0, 8):
            glPushMatrix()
            glTranslatef(*pos)
            glRotatef(270, 0.0, 1.0, 0.0)
            cerdito(cerdito_texture)
            glPopMatrix()
            
        if pos == (29, 0, 8):
            glPushMatrix()
            glTranslatef(*pos)
            glRotatef(180, 0.0, 1.0, 0.0)
            cerdito(cerdito_texture)
            glPopMatrix()


    # Finalmente, intercambio de buffers
    glfw.swap_buffers(window)




def scale_vertex(vertex):
    factor=1
    return tuple(coord * factor for coord in vertex)


def patas_pollito():
    glBegin(GL_QUADS)
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
    glEnd()


def cuerpo_pollito():
    glBegin(GL_QUADS)
    glColor3f(1, 1, 0)  # Blanco
    
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
    glEnd()


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
    patas_pollito()
    cuerpo_pollito()



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
    glColor3f(1, 1, 1)
    
    
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


def actualizar_posicion_pollito(pollito_pos, direccion, limite, angulo_rot):
    """Actualiza la posición del pollito y su rotación si cambia de dirección"""
    pollito_pos[0] += 2.25 * direccion[0]  # Actualizar posición en X
    if pollito_pos[0] > 38 or pollito_pos[0] < 2:  # Cambiar dirección en X
        direccion[0] *= -1  # Cambiar dirección
        angulo_rot[0] += 180  # Girar el pollito 180 grados
        angulo_rot[0] %= 360  # Asegurar que el ángulo esté en el rango [0, 360)
    return pollito_pos, direccion, angulo_rot



def draw_pollito_estatico(pollito_pos):
    """Dibuja el pollito en la posición especificada con su rotación"""
    glPushMatrix()
    glTranslatef(*pollito_pos)  # Mover el pollito a su posición
    pollito()
    glPopMatrix()


def draw_pollito(pollito_pos, angulo_rot):
    """Dibuja el pollito en la posición especificada con su rotación"""
    glPushMatrix()
    glTranslatef(*pollito_pos)  # Mover el pollito a su posición
    glRotatef(angulo_rot[0], 0, 1, 0)  # Rotar el pollito en el eje Y
    pollito()
    glPopMatrix()

"""

def process_input():
    #Procesa el estado de las teclas para mover la cámara
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
"""


def mover_adelante():
    global eje_x, eje_y, eje_z
    eje_x += center_x * movimiento
    eje_y += center_y * movimiento
    eje_z += center_z * movimiento

def mover_atras():
    global eje_x, eje_y, eje_z
    eje_x -= center_x * movimiento
    eje_y -= center_y * movimiento
    eje_z -= center_z * movimiento

def mover_izquierda():
    avanzar_izq_der(True)

def mover_derecha():
    avanzar_izq_der(False)

def girar_izquierda():
    global angulo_th
    angulo_th -= saltos

def girar_derecha():
    global angulo_th
    angulo_th += saltos

def girar_arriba():
    global angulo_pi
    angulo_pi -= saltos
    if angulo_pi <= 0.0:
        angulo_pi = 0.001  # Evitar valor cero

def girar_abajo():
    global angulo_pi
    angulo_pi += saltos
    if angulo_pi >= math.pi:
        angulo_pi = math.pi - 0.001  # Evitar exceder pi

def actualizar_direccion():
    global center_x, center_y, center_z
    center_x = radio * math.sin(angulo_pi) * math.cos(angulo_th)
    center_y = radio * math.cos(angulo_pi)
    center_z = radio * math.sin(angulo_pi) * math.sin(angulo_th)


def key_callback(window, key, scancode, action, mods):
    """Manejo de eventos del teclado para mover la cámara"""
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:
            mover_adelante()
        elif key == glfw.KEY_S:
            mover_atras()
        elif key == glfw.KEY_A:
            mover_izquierda()
        elif key == glfw.KEY_D:
            mover_derecha()
        elif key == glfw.KEY_LEFT:
            girar_izquierda()
        elif key == glfw.KEY_RIGHT:
            girar_derecha()
        elif key == glfw.KEY_UP:
            girar_arriba()
        elif key == glfw.KEY_DOWN:
            girar_abajo()

        # Actualizar dirección después de cualquier movimiento
        actualizar_direccion()


def init_opengl():
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


umbral_min = 5       
umbral_gesto = 20






# ... resto de importaciones y variables globales

def main():
    global window, prev_gray, p0
    global radio, angulo_th, angulo_pi, movimiento, saltos
    global eje_x, eje_y, eje_z, center_x, center_y, center_z

    # Inicializar variables de la cámara (Del primer main)
    radio = 1.0
    angulo_th = 3.9
    angulo_pi = 2.2
    saltos = 0.15
    movimiento = 3
    eje_x = 50.0
    eje_y = 35.0
    eje_z = 35.0

    # Dirección inicial de la cámara|
    center_x = radio * math.sin(angulo_pi) * math.cos(angulo_th)
    center_y = radio * math.cos(angulo_pi)
    center_z = radio * math.sin(angulo_pi) * math.sin(angulo_th)

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    width, height = 800, 600
    window = glfw.create_window(width, height, "Escena con Control Gestual y Texturas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)

    # Inicializar OpenGL (asumiendo que init_opengl() inicia todas las configuraciones necesarias)
    init_opengl()

    # ------------------------------------------------
    # Carga de todas las texturas (combinando ambos mains)
    # ------------------------------------------------

    # Texturas del tractor y animales (del primer main)
    madera_tracktor_texture = load_texture('wood_tracktor.jpg') 
    vaca_cuerpo = load_texture('vaca_cuerpo.jpg')
    vaca_patas = load_texture('vaca_patas.jpg')
    vaca_cara = load_texture('vaca_cara.jpg')
    cerdito_textura = load_texture('cerdito.jpg')

    # Texturas de la escena completa (del segundo main)
    wall_texture = load_texture("pared.jpg")           # Paredes casa
    roof_texture = load_texture("teja_cafe.jpg")      # Tejado casa
    door_texture = load_texture("puerta.jpg")          # Puerta casa
    window_texture = load_texture("ventanas.jpg")     # Ventanas casa

    textura_pared = load_texture("paredes_cobertizo.jpg")
    textura_techo = load_texture("techo_cobertizo_metal.jpg")
    textura_puerta = load_texture("porton.jpg")

    madera_granero_texture = load_texture('madera_granero.jpg')
    madera_blanca_texture = load_texture('madera_blanca.jpg')
    techo_granero_texture = load_texture("techo_cobertizo_metal.jpg")
    tierra_pasto_texture = load_texture('tierra_pasto.jpg')
    madera_valla_texture = load_texture('madera_valla.jpg')
    lodo_texture = load_texture('lodo.jpg')
    metal_silo_texture = load_texture('metal_silo.jpg')
    metal_silo2_texture = load_texture('metal_silo2.jpg')

    suelo_texture = load_texture("suelo-texture.jpg")       # Suelo del huerto
    vegetal_texture = load_texture("vegetal-texture.jpg")   # Vegetal en el huerto

    base_panal_texturas = load_texture('panal-abejas-textura.jpg')
    panal_texturas = load_texture('colmena-entrada-textura.jpg')

    texture_troncoManzano = load_texture('tree-branch-512x512.jpg')
    texture_pared_invernadero = load_texture('paredes_vidrio.jpg')
    texture_techo_invernadero = load_texture("techo_invernadero.jpeg")

    # Variables de la posición del pollito (del primer main)
    pollito_pos = [15.0, 0.0, 17.0]  # [x, y, z]
    direccion = [0.1]  # Dirección del movimiento del pollito
    limite = 30
    angulo_rot = [180]

    # Inicializar OpenCV y flujo óptico (del primer main)
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    ret, first_frame = cap.read()
    if not ret:
        print("No se pudo leer el primer frame de la cámara")
        return

    first_frame = cv.resize(first_frame, (1200, 720))
    prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
    lk_params = dict(winSize=(15, 15), maxLevel=2,
                     criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

    p0 = np.array([
        [350, 200],
        [1020, 200]
    ], dtype=np.float32)
    p0 = p0[:, np.newaxis, :]

    # Configurar callback de teclado
    glfw.set_key_callback(window, key_callback)

    # Bucle principal (combina la lógica de flujo óptico con el dibujado de la escena completa)
    while not glfw.window_should_close(window):
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv.resize(frame, (1200, 720))
        frame = cv.flip(frame, 1)
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Dibujar los puntos p0 siempre en el mismo lugar
        for px, py in p0.reshape(-1, 2):
            cv.circle(frame, (int(px), int(py)), 5, (0, 255, 0), -1)

        p1, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, p0, None, **lk_params)

        if p1 is not None and st is not None:
            bp1 = p1[st == 1]
            bp0 = p0[st == 1]

            if len(bp1) > 0:
                for i, (nv, vj) in enumerate(zip(bp1, bp0)):
                    a, b = (int(x) for x in nv.ravel())
                    c, d = (int(x) for x in vj.ravel())
                    dist_magnitud = math.sqrt((a - c)**2 + (b - d)**2)

                    if dist_magnitud > umbral_min:
                        cv.line(frame, (c, d), (a, b), (0, 125, 255), 2)
                        cv.circle(frame, (c, d), 2, (255, 255, 255), -1)
                        cv.circle(frame, (a, b), 3, (0, 0, 0), -1)

                        # Detección de gestos
                        if dist_magnitud > umbral_gesto:
                            if i == 0:
                                if a - c > umbral_gesto:
                                    mover_izquierda()
                                    
                                elif a - c < -umbral_gesto:
                                    mover_derecha()
                                    

                                if b - d > umbral_gesto:
                                    mover_adelante()
                                elif b - d < -umbral_gesto:
                                    mover_atras()
                                    
                            elif i == 1:
                                if a - c > umbral_gesto:
                                    girar_derecha()
                                    
                                elif a - c < (-umbral_gesto-5):
                                    girar_izquierda()
                                if b - d > umbral_gesto:
                                    
                                    girar_abajo()
                                elif b - d < -umbral_gesto:
                                    girar_arriba()
                                    

                            actualizar_direccion()
            else:
                # Si se pierden los puntos, reestablecer p0 a su posición original
                p0 = np.array([
                    [350, 200],
                    [1020, 200]
                ], dtype=np.float32)
                p0 = p0[:, np.newaxis, :]
                prev_gray = gray_frame.copy()
        else:
            # Si no hay p1, reiniciamos p0
            p0 = np.array([
                [350, 200],
                [1020, 200]
            ], dtype=np.float32)
            p0 = p0[:, np.newaxis, :]
            prev_gray = gray_frame.copy()

        cv.imshow("Video", frame)
        prev_gray = gray_frame.copy()

        # Actualizar posición del pollito
        pollito_pos, direccion, angulo_rot = actualizar_posicion_pollito(pollito_pos, direccion, limite, angulo_rot)

        # Dibujar la escena completa (con todos los parámetros)
        draw_scene(
            madera_tracktor_texture, pollito_pos, vaca_cuerpo, angulo_rot, cerdito_textura, vaca_patas, vaca_cara,
            wall_texture, roof_texture, door_texture, window_texture, madera_granero_texture, madera_blanca_texture,
            techo_granero_texture, tierra_pasto_texture, madera_valla_texture, lodo_texture, suelo_texture, vegetal_texture,
            texture_troncoManzano, base_panal_texturas, panal_texturas, metal_silo_texture, metal_silo2_texture, textura_pared,
            textura_techo, textura_puerta, texture_pared_invernadero, texture_techo_invernadero
        )
        

        glfw.poll_events()

        if cv.waitKey(30) & 0xFF == 27:
            break

    # Limpiar y cerrar
    glfw.terminate()
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()