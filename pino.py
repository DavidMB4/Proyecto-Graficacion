from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from PIL import Image
import glfw
import requests
from io import BytesIO

def load_texture_from_url(url):
    """Carga una textura desde una URL y la prepara para usar en OpenGL."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"No se pudo descargar la imagen desde {url}")

    img = Image.open(BytesIO(response.content))
    img = img.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL usa un origen en la esquina inferior izquierda
    img_data = img.convert("RGBA").tobytes()   # Convierte la imagen a RGBA

    texture_id = glGenTextures(1)              # Genera un ID de textura
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Enlaza la textura

    # Configuración de parámetros de la textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Enviar la textura a OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glBindTexture(GL_TEXTURE_2D, 0)  # Desenlazar la textura
    return texture_id

def draw_textured_trunk(texture_id):
    """Dibuja el tronco del pino con textura."""
    glPushMatrix()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Enlaza la textura

    glColor3f(1.0, 1.0, 1.0)  # Blanco para no alterar la textura
    glRotatef(-90, 1, 0, 0)  # Rotar el cilindro
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)  # Habilitar texturas para el quadric
    gluCylinder(quadric, 0.3, 0.1, 2.0, 32, 32)  # Dibuja el cilindro

    glBindTexture(GL_TEXTURE_2D, 0)  # Desenlaza la textura
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def draw_foliage():
    """Dibuja el follaje del pino como conos apilados"""
    glColor3f(0.1, 0.6, 0.1)  # Verde oscuro para el follaje
    quadric = gluNewQuadric()

    # Dibujar tres conos de diferentes tamaños
    foliage_levels = [
        (0.6, 1.2, 0.8),  # (Radio base, Altura, Traslación en Y)
        (0.4, 1.0, 1.6),
        (0.2, 0.8, 2.4),
    ]
    
    for base, height, y_translation in foliage_levels:
        glPushMatrix()
        glTranslatef(0.0, y_translation, 0.0)  # Elevar cada cono
        glRotatef(-90, 1, 0, 0)  # Rota para orientar el cono verticalmente
        gluCylinder(quadric, base, 0.0, height, 32, 32)  # Base más grande y punta cerrada
        glPopMatrix()

def draw_pine(texture_id):
    """Dibuja un pino completo."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(1, 1.5, 3,  # Posición de la cámara (más cerca del tronco)
          0, 1, 0,    # Punto al que mira (el centro del tronco)
          0, 1, 0)    # Dirección "arriba"

    # Dibuja el tronco
    draw_textured_trunk(texture_id)

    # Dibuja las hojas del pino (en forma de conos)
    draw_foliage()

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    width, height = 800, 600
    window = glfw.create_window(width, height, "Pino con Textura", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)

    # Configuración de OpenGL
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # URL de la textura en el repositorio
    texture_url = "https://raw.githubusercontent.com/DavidMB4/Proyecto-Graficacion/main/tree-branch-512x512.png"
    texture_id = load_texture_from_url(texture_url)

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_pine(texture_id)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
