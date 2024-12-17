import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PIL import Image
import sys

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)  # Prueba de profundidad
    glEnable(GL_TEXTURE_2D)  # Activar texturas
   
    # Configuración de perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 6.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

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

def draw_textured_quad(vertices, tex_coords, texture_id):
    """Dibuja un cuadrado con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for i in range(4):
        glTexCoord2f(*tex_coords[i])
        glVertex3f(*vertices[i])
    glEnd()

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
    
def draw_scene(textura_pared, textura_techo, textura_puerta):
    """Dibuja la escena completa"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(10, 8, 20, 0, 0, 0, 0, 1, 0)

    # Dibujar cobertizo
    draw_cobertizo(textura_pared, textura_techo, textura_puerta)
    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    width, height = 800, 600
    window = glfw.create_window(width, height, "Cobertizo con Techo plano", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Cargar texturas
    textura_pared = load_texture(r"paredes_cobertizo.jpg")
    textura_techo = load_texture(r"techo_cobertizo_metal.jpg")
    textura_puerta = load_texture(r"porton.jpg")

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_scene(textura_pared, textura_techo, textura_puerta)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
