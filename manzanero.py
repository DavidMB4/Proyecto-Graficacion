import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluCylinder, gluSphere
from PIL import Image
import sys

# Ruta de la imagen en tu repositorio de GitHub
TRONCO_TEXTURE_PATH = "https://raw.githubusercontent.com/DavidMB4/Proyecto-Graficacion/main/tree-branch-512x512.png"

def load_texture(file_path):
    """Carga una textura desde un archivo y la aplica."""
    try:
        texture_image = Image.open(file_path).transpose(Image.FLIP_TOP_BOTTOM)
        texture_data = texture_image.tobytes()
        width, height = texture_image.size

        # Generar y configurar la textura
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id
    except Exception as e:
        print(f"Error al cargar la textura: {e}")
        sys.exit(1)

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0) 
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)  

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  
    glMatrixMode(GL_MODELVIEW)

def draw_trunk(texture_id):
    """Dibuja el tronco del árbol como un cilindro con textura."""
    glPushMatrix()
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

def draw_ground():
    """Dibuja un plano para representar el suelo."""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3) 
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_tree(texture_id):
    """Dibuja un árbol completo con textura en el tronco y manzanas."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(4, 5, 8,  
              0, 1, 0, 
              0, 1, 0)  

    draw_ground()
    draw_trunk(texture_id)  
    draw_foliage() 
    draw_apples()   

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Manzanero 3D con Tronco Texturizado", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Cargar textura del tronco
    texture_id = load_texture(TRONCO_TEXTURE_PATH)

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_tree(texture_id)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
