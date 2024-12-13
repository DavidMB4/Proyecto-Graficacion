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

def draw_cube_base(texture_id):
    """Dibuja el cubo (plataforma pequeña del panal)"""
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # blanco para no alterar la textura

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, 0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, -0.5, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.5, 0.5)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, -0.5, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.5, -0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.5, -0.5)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.5, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.5, -0.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.5, -0.5, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, -0.5, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.5, 0.5, -0.5)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0.5, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0.5, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.5, 0.5)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, -0.5, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, -0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, -0.5, 0.5)
    glEnd()

def draw_cube_intermedio(texture_id):
    """Dibuja el cubo (plataforma intermedia del panal)"""
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glTranslatef(0, 0.5, 0)
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # Amarillo

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.75, 0, 0.75)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.75, 0, 0.75)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.75, 0.5, 0.75)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.75, 0.5, 0.75)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.75, 0, -0.75)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.75, 0, -0.75)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.75, 0.5, -0.75)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.75, 0.5, -0.75)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.75, 0, -0.75)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.75, 0, 0.75)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.75, 0.5, 0.75)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.75, 0.5, -0.75)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.75, 0, -0.75)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.75, 0, 0.75)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.75, 0.5, 0.75)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.75, 0.5, -0.75)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.75, 0.5, -0.75)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.75, 0.5, -0.75)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.75, 0.5, 0.75)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.75, 0.5, 0.75)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.75, 0, -0.75)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.75, 0, -0.75)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.75, 0, 0.75)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.75, 0, 0.75)
    glEnd()

def draw_cube_superior(texture_id):
    """Dibuja el cubo (plataforma superior del panal)"""
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glTranslatef(0, 0.5, 0)
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # Amarillo

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, 1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, 1)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -1)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, -1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, -1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, -1)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -1)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1, 0.5, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, -1)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(1, 0, -1)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, 1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(1, 0.5, -1)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0.5, -1)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0.5, -1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, 1)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -1)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, -1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0, 1)
    glEnd()

def draw_ground():
    """Dibuja un plano para representar el suelo o calle"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_panal(panal_texture):
    """Dibuja una casa sobre un plano"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(4, 3, 8,  # Posición de la cámara
              0, 1, 0,  # Punto al que mira
              0, 1, 0)  # Vector hacia arriba

    draw_ground()  # Dibuja el suelo
    draw_cube_base(panal_texture)    # Dibuja la base del panal
    draw_cube_intermedio(panal_texture)    # Dibuja la base intermedia del panal
    draw_cube_superior(panal_texture)    # Dibuja la base superior del panal
    draw_cube_superior(panal_texture)    # Dibuja la base superior del panal
    draw_cube_intermedio(panal_texture)    # Dibuja la base intermedia del panal
    glTranslatef(0, 0.5, 0)
    draw_cube_base(panal_texture)    # Dibuja la base del panal

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Panal de abejas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Carga de texturas
    panal_texture = load_texture(r"D:\Sexto Semestre\Graficacion\proyecto-final\colmena-entrada-textura.jpg") # Panal de abejas texturas

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_panal(panal_texture)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()