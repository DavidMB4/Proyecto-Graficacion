import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluSphere, gluCylinder

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)

def draw_stem():
    """Dibuja el tallo de la planta"""
    glPushMatrix()
    glColor3f(0.4, 0.8, 0.2)  # Verde claro para el tallo
    glTranslatef(0.0, 0.0, 0.0)  # Posicionar el tallo
    glRotatef(-90, 1, 0, 0)  # Rota para orientar el cilindro verticalmente
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.05, 0.05, 0.5, 32, 32)  # Tallos delgados
    glPopMatrix()

def draw_leaves():
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

def draw_strawberries():
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

def draw_ground():
    """Dibuja un plano para representar el suelo"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para el suelo
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_strawberry_plant():
    """Dibuja una planta de fresas completa"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(4, 3, 8,  # Posición de la cámara
              0, 1, 0,  # Punto al que mira
              0, 1, 0)  # Vector hacia arriba

    draw_ground()         # Dibuja el suelo
    draw_stem()           # Dibuja el tallo
    draw_leaves()         # Dibuja las hojas
    draw_strawberries()   # Dibuja las fresas

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Planta de fresas 3D", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_strawberry_plant()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
