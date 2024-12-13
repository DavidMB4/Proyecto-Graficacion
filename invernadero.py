import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad
    glEnable(GL_BLEND)                # Habilitar transparencia
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión
    glMatrixMode(GL_MODELVIEW)

def draw_ground():
    """Dibuja un plano verde para representar el césped"""
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.8, 0.2)  # Verde césped
    glVertex3f(-10, 0, -10)
    glVertex3f(10, 0, -10)
    glVertex3f(10, 0, 10)
    glVertex3f(-10, 0, 10)
    glEnd()

def draw_base():
    """Dibuja la base sólida del invernadero"""
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.2, 0.1)  # Marrón para la base
    glVertex3f(-2, 0.1, -2)  # Aumenta la coordenada Y a 0.1
    glVertex3f(2, 0.1, -2)   # Aumenta la coordenada Y a 0.1
    glVertex3f(2, 0.1, 2)    # Aumenta la coordenada Y a 0.1
    glVertex3f(-2, 0.1, 2)   # Aumenta la coordenada Y a 0.1
    glEnd()

def draw_walls():
    """Dibuja las paredes del invernadero"""
    glColor4f(0.5, 0.9, 1.0, 0.6)  # Vidrio translúcido

    # Lados
    glBegin(GL_QUADS)
    walls = [
        (-2, 0.5, -2), (-2, 2, -2), (-2, 2, 2), (-2, 0.5, 2),  # Lado izquierdo
        (2, 0.5, -2), (2, 2, -2), (2, 2, 2), (2, 0.5, 2),      # Lado derecho
    ]
    for v in walls:
        glVertex3f(*v)
    glEnd()

    # Parte trasera
    glBegin(GL_QUADS)
    glVertex3f(-2, 0.5, -2)
    glVertex3f(2, 0.5, -2)
    glVertex3f(2, 2, -2)
    glVertex3f(-2, 2, -2)
    glEnd()

def draw_roof():
    """Dibuja el techo del invernadero"""
    glColor4f(0.5, 0.9, 1.0, 0.6)  # Vidrio translúcido

    glBegin(GL_TRIANGLES)
    # Lado izquierdo
    glVertex3f(-2, 2, -2)
    glVertex3f(-2, 2, 2)
    glVertex3f(0, 3, 0)

    # Lado derecho
    glVertex3f(2, 2, -2)
    glVertex3f(2, 2, 2)
    glVertex3f(0, 3, 0)
    glEnd()

def draw_door():
    """Dibuja la puerta del invernadero"""
    glColor4f(0.5, 0.9, 1.0, 0.8)  # Vidrio ligeramente más opaco
    glBegin(GL_QUADS)
    glVertex3f(-0.5, 0.0, 2)  # Parte inferior izquierda
    glVertex3f(0.5, 0.0, 2)   # Parte inferior derecha
    glVertex3f(0.5, 1.5, 2)   # Parte superior derecha
    glVertex3f(-0.5, 1.5, 2)  # Parte superior izquierda
    glEnd()

    # Marco de la puerta
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

def draw_greenhouse():
    """Dibuja un invernadero completo"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(6, 4, 10,  # Posición de la cámara
              0, 1, 0,   # Punto al que mira
              0, 1, 0)   # Vector hacia arriba

    draw_ground()  # Suelo verde (césped)
    draw_base()    # Base sólida
    draw_walls()   # Paredes laterales y trasera
    draw_roof()    # Techo triangular
    draw_door()    # Puerta frontal

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Invernadero con Césped", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_greenhouse()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
