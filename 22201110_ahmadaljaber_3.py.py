from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

player_location=[0,0,30]
player_rotation=90.0
player_health=10
game_score=0
bullets_missed=0
game_is_over=False
bullets=[]
enemies=[]

camera_orbit_angle=0.0
camera_z_pos=500.0
first_person_view=False
field_of_view_y=120

auto_spin_cheat=False
auto_aim_cheat=False

ARENA_SIZE=600
PLAYER_SPEED=6.8
BULLET_SPEED=22.0
ENEMY_COUNT=5
ENEMY_SPEED=0.55

def initialize_enemies():
    global enemies
    enemies=[]
    for i in range(ENEMY_COUNT):
        enemies.append({
            "pos":[random.uniform(-ARENA_SIZE,ARENA_SIZE),random.uniform(-ARENA_SIZE,ARENA_SIZE),30],
            "scale":1.0,"scale_dir":1
        })

def restart_game():
    global player_location,player_rotation,player_health,game_score,bullets_missed,game_is_over,bullets,auto_spin_cheat,auto_aim_cheat
    player_location=[0,0,30]
    player_rotation=90.0
    player_health=10
    game_score=0
    bullets_missed=0
    game_is_over=False
    bullets=[]
    auto_spin_cheat=False
    auto_aim_cheat=False
    initialize_enemies()

def draw_text(x,y,text,font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0,1000,0,800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x,y)
    for character in text:
        glutBitmapCharacter(font,ord(character))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_player_model():
    glPushMatrix()
    glTranslatef(player_location[0],player_location[1],player_location[2])
    glRotatef(player_rotation-90,0,0,1)
    if game_is_over:
        glRotatef(90,0,1,0)
        glTranslatef(0,-30,0)
    glColor3f(0.8,0.4,0.1)
    glPushMatrix()
    glScalef(40,60,20)
    glutSolidCube(1)
    glPopMatrix()
    glColor3f(1,0.8,0.6)
    glPushMatrix()
    glTranslatef(0,0,45)
    glutSolidSphere(15,20,20)
    glPopMatrix()
    glColor3f(0.2,0.2,0.2)
    glPushMatrix()
    glTranslatef(30,0,20)
    glRotatef(90,0,1,0)
    gluCylinder(gluNewQuadric(),5,5,40,10,10)
    glPopMatrix()
    glColor3f(0.1,0.2,0.6)
    glPushMatrix()
    glTranslatef(-15,0,-30)
    gluCylinder(gluNewQuadric(),8,8,30,10,10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(15,0,-30)
    gluCylinder(gluNewQuadric(),8,8,30,10,10)
    glPopMatrix()
    glPopMatrix()

def draw_all_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy["pos"][0],enemy["pos"][1],enemy["pos"][2])
        glColor3f(1,0,0)
        glutSolidSphere(20*enemy["scale"],20,20)
        glTranslatef(0,0,15*enemy["scale"])
        glColor3f(0.1,0.1,0.1)
        glutSolidSphere(10*enemy["scale"],20,20)
        glPopMatrix()

def draw_all_bullets():
    glColor3f(1,1,0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet["pos"][0],bullet["pos"][1],bullet["pos"][2])
        glutSolidCube(10)
        glPopMatrix()

def draw_world_boundaries():
    glColor3f(0.2,0.6,0.2)
    boundary_height=100
    glPushMatrix()
    glTranslatef(0,ARENA_SIZE,boundary_height/2)
    glScalef(ARENA_SIZE*2,10,boundary_height)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0,-ARENA_SIZE,boundary_height/2)
    glScalef(ARENA_SIZE*2,10,boundary_height)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(ARENA_SIZE,0,boundary_height/2)
    glScalef(10,ARENA_SIZE*2,boundary_height)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-ARENA_SIZE,0,boundary_height/2)
    glScalef(10,ARENA_SIZE*2,boundary_height)
    glutSolidCube(1)
    glPopMatrix()

def keyboardListener(key,x,y):
    global player_rotation,auto_spin_cheat,auto_aim_cheat
    if game_is_over:
        if key==b'r':
            restart_game()
        return
    angle_rad=math.radians(player_rotation)
    move_x=math.cos(angle_rad)*PLAYER_SPEED
    move_y=math.sin(angle_rad)*PLAYER_SPEED
    if key==b'w':
        player_location[0]+=move_x
        player_location[1]+=move_y
    if key==b's':
        player_location[0]-=move_x
        player_location[1]-=move_y
    if key==b'a':
        player_rotation+=3.5
    if key==b'd':
        player_rotation-=3.5
    if key==b'c':
        auto_spin_cheat=not auto_spin_cheat
    if key==b'v' and first_person_view:
        auto_aim_cheat=not auto_aim_cheat

def specialKeyListener(key,x,y):
    global camera_z_pos,camera_orbit_angle
    if not first_person_view:
        if key==GLUT_KEY_UP:
            camera_z_pos=min(800,camera_z_pos+20)
        if key==GLUT_KEY_DOWN:
            camera_z_pos=max(50.0,camera_z_pos-20)
        if key==GLUT_KEY_LEFT:
            camera_orbit_angle-=5
        if key==GLUT_KEY_RIGHT:
            camera_orbit_angle+=5

def mouseListener(button,state,x,y):
    global first_person_view
    if not game_is_over and state==GLUT_DOWN:
        if button==GLUT_LEFT_BUTTON:
            fire_bullet()
        if button==GLUT_RIGHT_BUTTON:
            first_person_view=not first_person_view

def fire_bullet():
    bullets.append({"pos":list(player_location),"angle":player_rotation})

def update_bullets():
    global bullets_missed
    for bullet in bullets[:]:
        angle_rad=math.radians(bullet["angle"])
        bullet["pos"][0]+=math.cos(angle_rad)*BULLET_SPEED
        bullet["pos"][1]+=math.sin(angle_rad)*BULLET_SPEED
        if not (-ARENA_SIZE<bullet["pos"][0]<ARENA_SIZE and -ARENA_SIZE<bullet["pos"][1]<ARENA_SIZE):
            bullets.remove(bullet)
            bullets_missed+=1

def update_enemies():
    for enemy in enemies:
        change_x=player_location[0]-enemy["pos"][0]
        change_y=player_location[1]-enemy["pos"][1]
        dist=math.hypot(change_x,change_y)
        if dist!=0:
            enemy["pos"][0]+=(change_x/dist)*ENEMY_SPEED
            enemy["pos"][1]+=(change_y/dist)*ENEMY_SPEED
        enemy["scale"]+=0.01*enemy["scale_dir"]
        if enemy["scale"]>1.25 or enemy["scale"]<0.75:
            enemy["scale_dir"]*=-1

def collision_detection():
    global game_score,player_health
    for bullet in bullets[:]:
        for enemy in enemies:
            if math.hypot(bullet["pos"][0]-enemy["pos"][0],bullet["pos"][1]-enemy["pos"][1])<25:
                if bullet in bullets:
                    bullets.remove(bullet)
                enemy["pos"]=[random.uniform(-ARENA_SIZE,ARENA_SIZE),random.uniform(-ARENA_SIZE,ARENA_SIZE),30]
                game_score+=1
                break
    for enemy in enemies:
        if math.hypot(player_location[0]-enemy["pos"][0],player_location[1]-enemy["pos"][1])<40:
            player_health-=1
            enemy["pos"]=[random.uniform(-ARENA_SIZE,ARENA_SIZE),random.uniform(-ARENA_SIZE,ARENA_SIZE),30]

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(field_of_view_y,1.25,1,2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if first_person_view:
        angle_rad=math.radians(player_rotation)
        look_at_x=player_location[0]+100*math.cos(angle_rad)
        look_at_y=player_location[1]+100*math.sin(angle_rad)
        gluLookAt(player_location[0],player_location[1],player_location[2]+20,look_at_x,look_at_y,player_location[2]+20,0,0,1)
    else:
        camera_distance=380
        cam_x=player_location[0]-camera_distance*math.cos(math.radians(camera_orbit_angle))
        cam_y=player_location[1]-camera_distance*math.sin(math.radians(camera_orbit_angle))
        gluLookAt(cam_x,cam_y,camera_z_pos,player_location[0],player_location[1],player_location[2],0,0,1)

def idle():
    global game_is_over,player_rotation
    if not game_is_over:
        update_bullets()
        update_enemies()
        collision_detection()
        if auto_aim_cheat and first_person_view and enemies:
            closest_enemy=min(enemies,key=lambda e:math.hypot(player_location[0]-e["pos"][0],player_location[1]-e["pos"][1]))
            player_rotation=math.degrees(math.atan2(closest_enemy["pos"][1]-player_location[1],closest_enemy["pos"][0]-player_location[0]))
        elif auto_spin_cheat:
            player_rotation+=1.5
            for enemy in enemies:
                angle_to_enemy=math.degrees(math.atan2(enemy["pos"][1]-player_location[1],enemy["pos"][0]-player_location[0]))
                if abs((player_rotation%360)-(angle_to_enemy%360))<5:
                    fire_bullet()
        if player_health<=0 or bullets_missed>=50:
            game_is_over=True
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0,0,1000,800)
    setupCamera()
    glBegin(GL_QUADS)
    for i in range(-ARENA_SIZE,ARENA_SIZE,50):
        for j in range(-ARENA_SIZE,ARENA_SIZE,50):
            if (i//50+j//50)%2==0:
                glColor3f(0.9,0.9,0.9)
            else:
                glColor3f(0.8,0.6,1.0)
            glVertex3f(i,j,0)
            glVertex3f(i,j+50,0)
            glVertex3f(i+50,j+50,0)
            glVertex3f(i+50,j,0)
    glEnd()
    draw_world_boundaries()
    draw_all_enemies()
    draw_all_bullets()
    if not first_person_view:
        draw_player_model()
    draw_text(10,770,f"Player Life Remaining: {player_health}")
    draw_text(10,740,f"Game Score: {game_score}")
    draw_text(10,710,f"Player Bullet Missed: {bullets_missed}")
    if game_is_over:
        draw_text(400,400,"GAME OVER",GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(380,370,"Press 'R' to Restart",GLUT_BITMAP_HELVETICA_18)
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE|GL_RGB|GL_DEPTH)
    glutInitWindowSize(1000,800)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b"3D Shooter Game")
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1,0.0,0.1,1.0)
    initialize_enemies()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__=="__main__":
    main()