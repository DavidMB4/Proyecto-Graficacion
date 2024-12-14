import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PIL import Image
import sys

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad
    glEnable(GL_LIGHTING)             # Activar luces
    glEnable(GL_LIGHT0)               # Luz básica
    glEnable(GL_COLOR_MATERIAL)       # Materiales de color para reflejar luz
    glShadeModel(GL_SMOOTH)           # Sombreado suave

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_TEXTURE_2D) # Activar texturas

    # Luz ambiental y difusa
    light_pos = [10, 10, 10, 1.0]  # Posición de la luz
    light_ambient = [0.3, 0.3, 0.3, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

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

def draw_columna(texture_id):
    """Dibuja el rectangulo de columna de la valla (delimitadores de la granja)"""
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # blanco para no alterar la textura

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, 0, 0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, 3, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, 3, 0.5)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, 3, -0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, 3, -0.5)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.25, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.25, 3, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, 3, -0.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.25, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, 3, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.25, 3, -0.5)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, 3, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, 3, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, 3, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, 3, 0.5)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, 0, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, 0, 0.5)
    glEnd()

def draw_valla(texture_id):
    """Dibuja el rectangulo del tablon del valla (delimitadores de la granja)"""
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # blanco para no alterar la textura

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, 0, 1.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, 0, 1.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, .3, 1.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, .3, 1.5)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, 0, -1.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, 0, -1.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, .3, -1.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, .3, -1.5)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, 0, -1.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.25, 0, 1.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.25, .3, 1.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, .3, -1.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.25, 0, -1.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, 0, 1.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, .3, 1.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.25, .3, -1.5)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, .3, -1.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, .3, -1.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, .3, 1.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, .3, 1.5)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.25, 0, -1.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.25, 0, -1.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.25, 0, 1.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.25, 0, 1.5)
    glEnd()

def draw_delimitador(madera_delimitador_textura):
    """Dibuja una valla delimitador de la granja"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(4, 3, 8,  # Posición de la cámara
              0, 1, 0,  # Punto al que mira
              0, 1, 0)  # Vector hacia arriba

    glTranslatef(0, 0, -1)
    draw_columna(madera_delimitador_textura) # Dibuja la columna de la valla
    glTranslatef(0.5, 2.3, 3)
    draw_valla(madera_delimitador_textura) # Dibuja el tablon de la valla
    glTranslatef(0, -0.5, 0)
    draw_valla(madera_delimitador_textura)
    glTranslatef(0, -0.5, 0)
    draw_valla(madera_delimitador_textura)
    glTranslatef(0, -1.3, 2)
    draw_columna(madera_delimitador_textura)

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Valla delimitadora de la granja", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Cargar texturas
    madera_delimitador_textura = load_texture(r"D:\Sexto Semestre\Graficacion\proyecto-final\panal-abejas-textura.jpg")

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_delimitador(madera_delimitador_textura)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()