'''# Task 1:

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
Width, Height = 800, 600
Rain_count = 150
rains = []
rain_speed = 2.5
rain_slant = 0.0  # Using ONE name for this variable
# Day/night factor: 0.0 is night, 1.0 is day
day_night_checker = 0.0
def init_raindrops():
    global rains  
    rains = []    
    for i in range(Rain_count):
        x = random.uniform(0, Width)
        y = random.uniform(0, Height)
        rains.append([x, y]) 
def init_gl():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, Width, 0.0, Height, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
def house_coordinates():
    # Walls
    glColor3f(0.69, 0.55, 0.25)
    glBegin(GL_TRIANGLES)
    # Rectangle=triangle1+triangle2
    # Triangle 1
    glVertex2f(250, 100)
    glVertex2f(550, 100)
    glVertex2f(550, 300)
    # Triangle 2
    glVertex2f(250, 100)
    glVertex2f(550, 300)
    glVertex2f(250, 300)
    glEnd()
    # Roof
    glColor3f(0.6, 0.2, 0.2)
    glBegin(GL_TRIANGLES)
    # Roof=1 triangle
    glVertex2f(250, 300)
    glVertex2f(550, 300)
    glVertex2f(400, 450)
    glEnd()
    # Door
    glColor3f(0.4, 0.2, 0.0)
    glBegin(GL_TRIANGLES)
    # Rectangle diye doors
    # Triangle 1
    glVertex2f(325, 100)
    glVertex2f(375, 100)
    glVertex2f(375, 200)
    # Triangle 2
    glVertex2f(325, 100)
    glVertex2f(375, 200)
    glVertex2f(325, 200)
    glEnd()
    # Window
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    # Rectangle diye window
    # Triangle 1
    glVertex2f(425, 200)
    glVertex2f(475, 200)
    glVertex2f(475, 250)
    # Triangle 2
    glVertex2f(425, 200)
    glVertex2f(475, 250)
    glVertex2f(425, 250)
    glEnd()
def rain_coordinates():
    if day_night_checker > 0.5:
        glColor3f(0.0, 0.0, 0.0)
    else:
        glColor3f(0.8, 0.8, 0.8)
    glLineWidth(1)
    glBegin(GL_LINES)
    for i in rains:
        glVertex2f(i[0], i[1])
        glVertex2f(i[0] + rain_slant, i[1] - 10)
    glEnd()
def animate():
    global rains
    for i in range(Rain_count):
        rains[i][1] -= rain_speed
        rains[i][0] += rain_slant
        if rains[i][1] < 0:
            rains[i][1] = Height
            rains[i][0] = random.uniform(0, Width)
        if rains[i][0] > Width:
            rains[i][0] = 0
        if rains[i][0] < 0:
            rains[i][0] = Width
    glutPostRedisplay()
def specialKeycommands(key, x, y):
    global rain_slant
    if key == GLUT_KEY_RIGHT:
        rain_slant += 0.2
    if key == GLUT_KEY_LEFT:
        rain_slant -= 0.2
def keyboardcommands(key, x, y):
    global day_night_checker
    if key == b'd':
        day_night_checker = min(1.0, day_night_checker + 0.1)
    if key == b'n':
        day_night_checker= max(0.0, day_night_checker - 0.1)
    if key == b'\x1b':
        glutLeaveMainLoop()
    glutPostRedisplay()
def display_house():
    current = day_night_checker
    glClearColor(current, current, current, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    house_coordinates()
    rain_coordinates()
    glutSwapBuffers()
if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(Width, Height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"House in rain")
    init_gl()
    init_raindrops()
    glutDisplayFunc(display_house)
    glutIdleFunc(animate)
    glutSpecialFunc(specialKeycommands)
    glutKeyboardFunc(keyboardcommands)
    glutMainLoop()
'''






'''# Task 2:
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
width, height = 900, 700
limits = 250
points = []
speed = 1.0
froze = False
blinks = False
def init_gl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-limits, limits, -limits, limits, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
def set_limits():
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-limits, -limits)
    glVertex2f(limits, -limits)
    glVertex2f(limits, limits)
    glVertex2f(-limits, limits)
    glEnd()
def set_points():
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in points:
        if blinks:
            glColor3f(0.0, 0.0, 0.0)
        else:
            glColor3f(p['r'], p['g'], p['b'])
        glVertex2f(p['x'], p['y'])
    glEnd()
def animate():
    if froze:
        return
    for p in points:
        p['x'] += p['dx'] * speed
        p['y'] += p['dy'] * speed
        if p['x'] >= limits or p['x'] <= -limits:
            p['dx'] *= -1
        if p['y'] >= limits or p['y'] <= -limits:
            p['dy'] *= -1
    glutPostRedisplay()
def mousecommands(button, state, x, y):
    global blinks
    if froze:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        gl_x = (x / width) * (2 * limits) - limits
        gl_y = limits - (y / height) * (2 * limits)
        new_point = {
            'x': gl_x, 'y': gl_y,
            'dx': random.choice([-1, 1]), 'dy': random.choice([-1, 1]),
            'r': random.random(), 'g': random.random(), 'b': random.random()
        }
        points.append(new_point)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blinks = not blinks
def specialKeycommands(key, x, y):
    global speed
    if froze:
        return
    if key == GLUT_KEY_UP:
        speed += 0.5
    if key == GLUT_KEY_DOWN:
        if speed > 0.5:
            speed -= 0.5
def keyboardcommands(key, x, y):
    global froze
    if key == b' ':
        froze = not froze
    if key == b'\x1b':
        glutLeaveMainLoop()
def display_box():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    set_limits()
    set_points()
    glutSwapBuffers()
if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(150, 150)
    glutCreateWindow(b"The Amazing Box ")
    init_gl()
    glutDisplayFunc(display_box)
    glutIdleFunc(animate)
    glutMouseFunc(mousecommands)
    glutSpecialFunc(specialKeycommands)
    glutKeyboardFunc(keyboardcommands)
    glutMainLoop()
'''