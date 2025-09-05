

# Open GL libraries import kortesi first e
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random #eta diye corals, enemies, hearts etc egula generate korbo
import math
import time #speed, delay eshob er jonno

# egula basically kontar por kon page shajaisi oitar sequence
STATE_SUB_SELECT = 0
STATE_WORD_SELECT = 1
STATE_PLAYING = 2
STATE_PAUSED = 3
STATE_GAME_OVER = 4
STATE_YOU_WIN = 5
#erpor code run korle game ei page diye start hobe
game_state = STATE_SUB_SELECT

#words gula list e dhukaisi word hunt er jonno
WORDS = ["FISH", "SEA", "OCEAN", "SHARK", "OCTOPUS", "TURTLE", "SHIP"]

#run korar porer state
selected_sub = 0 #player kon submarine select korse
selected_word_index = 0 #player kon word select korse
animation_angle = 0.0 #submarine page er angle
start_time = 0.0 #time suhuru

#PLAYER  er VARIABLES
player_pos = [0, 150, 0] # player submarine er position (x, y, z coordinates)
player_rotation_y = 0.0 # submarine er facing direction y axis e
player_speed = 10.0 # player movement er speed
initial_speed = 10.0 # shuru te je speed thakbe

#CAMERAr variable
camera_angle_h = 0.0 # camera horizontal ghurano angle
camera_angle_v = 20.0 # camera vertical angle (slightly up/down)
camera_distance = 250 # camera distance from submarine
is_first_person = False # default e third person, jodi true kori tahole first person view

# scores gula
score = 100 # player er score start e 100 thake
hearts_collected = 0 # koyta heart collect korse
jellyfish_collisions = 0 #jellyfish er shthe koybar collissions hoise

# target letter gula
target_word = "" # jokhon ekta word select hoy, oita ekhane store hoy
target_letter_index = 0 #koto no. letter porjonto collect korsi 
target_letter_obj = None #current letter jeta lagbe sheta screen e ase ki na
letter_spawn_timer = 0 #letter spawn timing er jonno

# background er jinish gula
#ei lists er moddhe onek objects rakha hobe
hearts, jellyfish, fish_small, fish_large, seaweed, seabed_rocks, corals = [], [], [], [], [], [], []

#win korar por animation
victory_angle = 0.0 # win korle rotation animation er angle
barrel_roll_angle = 0.0 # submarine barrel roll animation er jonno

#speed
jellyfish_speed_multiplier = 1.0 # jellyfish koto fast move korbe
jellyfish_direction_change_base = 100  # koto frame por por jellyfish er direction change hobe (base value)
#ekhan theke functions shuru
def initialize_game():
    #word selection e rpor shob variable reset kora thake
    global game_state, selected_sub, selected_word_index, jellyfish_speed_multiplier
    game_state = STATE_SUB_SELECT # abar shuru korle first page e (submarine select)
    selected_sub = 0  # submarine select reset
    selected_word_index = 0 # word select reset
    jellyfish_speed_multiplier = 1.0 # jellyfish er speed reset
    reset_level() # new level er setup call

def reset_level():

    global player_pos, player_rotation_y, score, hearts, jellyfish, hearts_collected, jellyfish_collisions, target_letter_index, target_letter_obj, start_time, is_first_person, fish_small, fish_large, seaweed, seabed_rocks, corals, player_speed, victory_angle, barrel_roll_angle, jellyfish_speed_multiplier
    player_pos = [0, 150, 0]  # submarine abar starting position e chole ashbe
    player_rotation_y = 0.0 # submarine abar straight facing thakbe
    score = 100  # score reset
    hearts_collected = 0 # hearts reset
    jellyfish_collisions = 0 # collision reset
    target_letter_index = 0 # word er shuru theke abar
    target_letter_obj = None # kono letter screen e nai
    is_first_person = False # camera abar third person view
    player_speed = initial_speed # speed reset to starting speed
    victory_angle = 0.0 # victory animation reset
    barrel_roll_angle = 0.0 # barrel roll reset
    jellyfish_speed_multiplier = 1.0 # jellyfish speed reset
    start_time = time.time() # notun level start time store
     #ekhon shob environment object lists clear korbo
    hearts.clear(); jellyfish.clear(); fish_small.clear(); fish_large.clear(); seaweed.clear(); seabed_rocks.clear(); corals.clear()
    #karon notun level shuru korar age environment ke reset korte hoy


 
    #ekhon notun objects banabo jate pura environment abar fill hoy
    #player jekhane thakbe tar sathe z-position change hobe
    # Initial spawn range for objects
    spawn_range_z = [-4000, 0] # objects player er pichoner theke shamne porjonto thakbe
    spawn_range_x = [-2000, 2000] # x-direction e kototuku spread korbe
    spawn_range_y_hearts = [50, 250] # hearts koto height e spawn hobe
    spawn_range_y_jellyfish = [50, 250] # jellyfish er height range
    spawn_range_y_fish = [50, 350] # small fish er height range
    spawn_range_y_large_fish = [100, 300] # large fish er height range
    
    for _ in range(40): # 40 ta heart spawn korbo
        hearts.append({
            'pos': [random.uniform(spawn_range_x[0], spawn_range_x[1]), # random x position
                   random.uniform(spawn_range_y_hearts[0], spawn_range_y_hearts[1]), # random y (height) 
                   random.uniform(spawn_range_z[0], spawn_range_z[1])], # random z (depth)
            'type': 'red' if random.random() > 0.2 else 'pink', # 80% chance red heart, 20% pink heart
            'pump_phase': random.uniform(0, 2 * math.pi),  # For pumping animation
            'pump_speed': random.uniform(0.05, 0.1),  # Speed of pumping
        })
    
    for _ in range(25): # 25 ta jellyfish spawn korbo
        jellyfish.append({
            'pos': [random.uniform(spawn_range_x[0], spawn_range_x[1]), # random x
                   random.uniform(spawn_range_y_jellyfish[0], spawn_range_y_jellyfish[1]), # random y 
                   random.uniform(spawn_range_z[0], spawn_range_z[1])], # random z
            'type': 'purple' if random.random() > 0.3 else 'red', # 70% purple, 30% red
            'bob_speed': random.uniform(0.2, 0.5), # up-down bobbing er speed 
            'tentacle_speed': random.uniform(2,4), # tentacle movement er speed
            'vel': [random.uniform(-1.5, 1.5), random.uniform(-0.8, 0.8), random.uniform(-1.5, 1.5)], #jellyfish er velocity
            'direction_change_timer': random.randint(0, 120), # koto time por por direction change hobe
            'pulse_phase': random.uniform(0, 2 * math.pi),  # pulse animation er phase
            'base_speed': random.uniform(0.8, 1.2), # jellyfish er base speed
            'aggression': random.uniform(0.5, 0.9),  #player er dike ashar chance
        })
    
    for _ in range(50): # 50 ta small fish spawn
        fish_small.append({
            'pos': [random.uniform(spawn_range_x[0], spawn_range_x[1]), 
                   random.uniform(spawn_range_y_fish[0], spawn_range_y_fish[1]), 
                   random.uniform(spawn_range_z[0], spawn_range_z[1])], 
            'speed': random.uniform(1.0, 2.0), 
            'color': [random.uniform(0.5,1), 0.5, 0.2], 
            'size': random.uniform(4,6) # chhoto size (4-6)
        })
    
    for _ in range(10): # 10 ta boro fish spawn
        fish_large.append({
            'pos': [random.uniform(spawn_range_x[0], spawn_range_x[1]), 
                   random.uniform(spawn_range_y_large_fish[0], spawn_range_y_large_fish[1]), 
                   random.uniform(spawn_range_z[0], spawn_range_z[1])], 
            'speed': random.uniform(0.5, 1.0), 
            'color': [0.2, 0.6, random.uniform(0.5,1)], 
            'size': random.uniform(12,18) # boro size (12-18)
        })
    
    # nicher seaplants gula
    seabed_spawn_range_z = [-5000, 5000] # seaplants jate continuous lage, huge z range
    seabed_spawn_range_x = [-5000, 5000]
    
    #seaweed baracchi
    for i in range(3000): # 1200 chilo, ekhon 3000 seaweed jate seabed beshi dense lage
        seaweed.append({
            'pos': [random.uniform(seabed_spawn_range_x[0], seabed_spawn_range_x[1]), 
                   -50, 
                   random.uniform(seabed_spawn_range_z[0], seabed_spawn_range_z[1])],
            'height': random.uniform(50, 200), 
            'sway': random.uniform(5, 20),
            'sway_phase': random.uniform(0, 2 * math.pi)  # For individual sway animation
        })
    
    for _ in range(200): # 200 ta rock dilam niche
        seabed_rocks.append({
            'pos': [random.uniform(seabed_spawn_range_x[0], seabed_spawn_range_x[1]), 
                   -45, 
                   random.uniform(seabed_spawn_range_z[0], seabed_spawn_range_z[1])], 
            'size': random.uniform(8,15)
        })
    
    for _ in range(150): # 150 ta coral
        corals.append({
            'pos': [random.uniform(seabed_spawn_range_x[0], seabed_spawn_range_x[1]), 
                   -50, 
                   random.uniform(seabed_spawn_range_z[0], seabed_spawn_range_z[1])], 
            'color': [random.uniform(0.8,1), random.uniform(0.2,0.4), random.uniform(0.2,0.4)]
        })

# submarine akbo
def draw_submarine(sub_id, is_selected=False, victory_mode=False):
    #sub id mane kon submarine akbo, erporer ta select hoise naki na oita bujhay
    glPushMatrix()
    if is_selected: glScalef(1.1, 1.1, 1.1) # If this submarine is selected, make it 10% bigger
    
    # Victory barrel roll er animation
    if victory_mode:
        glRotatef(barrel_roll_angle, 0, 0, 1) #z axix e rotate korbo
    
    if sub_id == 0: # Red
        glColor3f(0.9, 0.1, 0.1); glPushMatrix(); glScalef(2.0, 0.8, 0.9); glutSolidSphere(30, 30, 30); glPopMatrix()
        glColor3f(1, 1, 1); glPushMatrix(); glTranslatef(40, 10, 0); glScalef(0.8, 0.6, 0.6); glutSolidSphere(25, 20, 20); glPopMatrix()
        glColor3f(1, 1, 1); glPushMatrix(); glTranslatef(-65, 0, 0); glScalef(1, 4, 0.3); glutSolidCube(10); glPopMatrix()
    elif sub_id == 1: # Yellow
        glColor3f(1.0, 0.84, 0.0); glPushMatrix(); glScalef(1.5, 1, 1); glutSolidSphere(30, 30, 30); glPopMatrix()
        glColor3f(0.5, 0.8, 1.0); glPushMatrix(); glTranslatef(0, 0, 30); gluDisk(gluNewQuadric(), 0, 15, 20, 1); glPopMatrix()
        glColor3f(0.5, 0.8, 1.0); glPushMatrix(); glTranslatef(0, 30, 0); glScalef(1, 1, 0.8); glutSolidCube(20); glPopMatrix()
    elif sub_id == 2: # Green
        glColor3f(0.1, 0.4, 0.2); glPushMatrix(); glScalef(2.5, 0.6, 0.7); glutSolidCube(30); glPopMatrix()
        glColor3f(0.1, 0.1, 0.1); glPushMatrix(); glTranslatef(-20, 0, 0); glScalef(2, 0.2, 5); glutSolidCube(10); glPopMatrix()
        glColor3f(0.5, 1.0, 0.5); glPushMatrix(); glTranslatef(60, 0, 0); gluSphere(gluNewQuadric(), 12, 20, 20); glPopMatrix()
    glPopMatrix()


#fish akbo
def draw_fish_model(size, color):
   
    glPushMatrix()
    glColor3fv(color)
    # Body 
    glPushMatrix(); glScalef(2.0, 1.0, 1.0); glutSolidSphere(size, 15, 15); glPopMatrix()
    # Tail Fin 
    glColor3f(color[0]*0.8, color[1]*0.8, color[2]*0.8) # Slightly darker color
    glPushMatrix(); glTranslatef(-size*1.8, 0, 0); glRotatef(90, 0,1,0); glScalef(1, 1.5, 0.2); glutSolidCone(size, size*1.5, 10, 5); glPopMatrix()
    # chikhon tube type
    glPushMatrix(); glTranslatef(0, size*0.8, 0); glScalef(1.2, 0.6, 0.1); glutSolidCube(size*2); glPopMatrix()
    # Eyes
    glColor3f(0,0,0)
    glPushMatrix(); glTranslatef(size*1.5, size*0.3, size*0.5); glutSolidSphere(size*0.15, 8, 8); glPopMatrix()
    glPushMatrix(); glTranslatef(size*1.5, size*0.3, -size*0.5); glutSolidSphere(size*0.15, 8, 8); glPopMatrix()
    glPopMatrix()


#jellyfish akbo
def draw_jellyfish_model(jelly):
   
    global animation_angle
    glPushMatrix()
    
    # jelly fish er pumping effect ta
    pulse = math.sin(animation_angle * jelly['bob_speed'] + jelly['pulse_phase']) * 15
    bob_offset = math.sin(animation_angle * jelly['bob_speed']) * 10
    
    glTranslatef(jelly['pos'][0], jelly['pos'][1] + bob_offset + pulse, jelly['pos'][2]) #hellyfish ke move krbo
    
    #solid colors ditesi
    if jelly['type'] == 'purple':
        glColor3f(0.8, 0.5, 1.0)
    else:
        glColor3f(1.0, 0.3, 0.3) #red
    
    glPushMatrix(); glScalef(1, 1, 0.7); glutSolidSphere(25, 20, 20); glPopMatrix()
    
    # Eyes
    glColor3f(0,0,0)
    glPushMatrix(); glTranslatef(10, 5, 15); glutSolidSphere(3, 10, 10); glPopMatrix()
    glPushMatrix(); glTranslatef(-10, 5, 15); glutSolidSphere(3, 10, 10); glPopMatrix()
    
    # Tentacles 
    if jelly['type'] == 'purple':
        glColor3f(0.7, 0.4, 0.9)  
    else:
        glColor3f(0.9, 0.2, 0.2) 
    
    for i in range(8):
        glPushMatrix()
        glRotatef(i * 45, 0, 0, 1) #tentacles gula rotate hote thakbe
        glTranslatef(15, 0, 0)
        sway = math.sin(animation_angle * jelly['tentacle_speed'] + i) * 20 # Move tentacle outwards
        glRotatef(sway, 1, 0, 0)
        glScalef(0.5, 0.5, 10)
        glutSolidCube(5)
        glPopMatrix()
    glPopMatrix()

#heart akbo
def draw_heart_shape(scale_factor=1.0):
    
    glPushMatrix()
    glScalef(scale_factor, scale_factor, scale_factor)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0.5) # Top point
    for i in range(100):
        angle = 2 * math.pi * i / 100
        x = 0.6 * math.sin(angle)**3
        y = 0.5 * (13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle)) / 16
        glVertex2f(x, y + 0.5) #
    glEnd()
    glPopMatrix()

# draw function gula
def draw_environment():
    # Hearts with pumping animation
    for heart in hearts:
        glPushMatrix()
        glTranslatef(*heart['pos'])
        
        # Calculate pump scale for animation
        pump_scale = 1.0 + 0.2 * math.sin(animation_angle * heart['pump_speed'] + heart['pump_phase'])
        glScalef(35 * pump_scale, 35 * pump_scale, 35 * pump_scale)
        
        if heart['type'] == 'red':
            glColor3f(1.0, 0.2, 0.2)
        else: # pink
            glColor3f(1.0, 0.5, 1.0)
        draw_heart_shape()
        glPopMatrix()
    
    # Fish with new models
    for fish in fish_small:
        glPushMatrix(); glTranslatef(*fish['pos']); glRotatef(90, 0,1,0); draw_fish_model(fish['size'], fish['color']); glPopMatrix()
    for fish in fish_large:
        glPushMatrix(); glTranslatef(*fish['pos']); glRotatef(90, 0,1,0); draw_fish_model(fish['size'], fish['color']); glPopMatrix()
    
    #seaweed
    glColor3f(0.1, 0.6, 0.3)
    for sw in seaweed:
        glPushMatrix(); 
        glTranslatef(sw['pos'][0], sw['pos'][1], sw['pos'][2])
        
        #sway animation seaweed er jonno
        sway_amount = math.sin(animation_angle * 0.5 + sw['sway_phase']) * sw['sway']
        glRotatef(sway_amount, 0, 0, 1)
        glRotatef(-90, 1, 0, 0)
        
        # Draw seaweed with varying thickness
        base_radius = random.uniform(2, 4)
        gluCylinder(gluNewQuadric(), base_radius, 0, sw['height'], 8, 5)
        glPopMatrix()
    
    # Add additional seaweed clusters for denser appearance
    glColor3f(0.05, 0.5, 0.2)  # Slightly darker seaweed

    for _ in range(1000):  #ektu variety color seaweed er
        x = random.uniform(-5000, 5000)
        z = random.uniform(-5000, 5000)
        height = random.uniform(30, 150)
        sway = random.uniform(3, 15)
        
        glPushMatrix()
        glTranslatef(x, -50, z)
        glRotatef(math.sin(animation_angle * 0.3 + x) * sway, 0, 0, 1)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), random.uniform(1, 3), 0, height, 6, 4)
        glPopMatrix()
    
    #rocks
    glColor3f(0.4, 0.4, 0.4)
    for rock in seabed_rocks:
        glPushMatrix(); glTranslatef(*rock['pos']); glutSolidSphere(rock['size'], 5, 5); glPopMatrix()
    #corals
    for coral in corals:
        glPushMatrix(); glTranslatef(coral['pos'][0], coral['pos'][1], coral['pos'][2]); glColor3fv(coral['color'])
        for i in range(3):
            glTranslatef(0, 10, 0)
            glutSolidSphere(8 - i*2, 10, 10)
        glPopMatrix()
    
    # Jellyfish 
    for jelly in jellyfish:
        draw_jellyfish_model(jelly)

#letter akbo
def draw_letter(letter_obj):
    if not letter_obj: return
    glPushMatrix(); glTranslatef(*letter_obj['pos']); glColor3f(1.0, 1.0, 0.0); glScalef(0.3, 0.3, 0.3)
    glLineWidth(5); glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(letter_obj['char'])); glPopMatrix()

def draw_border():
    color = [0,0,0]
    if score > 100: color = [0.1, 0.7, 0.1] # Green if score > 100
    elif score >= 20: color = [0.9, 0.9, 0.1] #should be >= 20 for yellow
    else: color = [0.8, 0.1, 0.1] # Red if score < 20
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0, 100, 0, 100); glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity(); glDisable(GL_DEPTH_TEST); glLineWidth(10); glColor3fv(color)
    glBegin(GL_LINE_LOOP); glVertex2f(1, 1); glVertex2f(99, 1); glVertex2f(99, 99); glVertex2f(1, 99); glEnd()
    glEnable(GL_DEPTH_TEST); glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)

#1st person view er jonno cockpit akbo
def draw_cockpit_view():
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0, 1000, 0, 800); glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity(); glDisable(GL_DEPTH_TEST)
    
    #dark border at top and bottom e
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    # Top border
    glVertex2f(0, 700); glVertex2f(1000, 700); glVertex2f(1000, 800); glVertex2f(0, 800)
    # Bottom border
    glVertex2f(0, 0); glVertex2f(1000, 0); glVertex2f(1000, 100); glVertex2f(0, 100)
    glEnd()
    
    #frame around the viewport
    glColor3f(0.3, 0.3, 0.3)
    glLineWidth(3.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(0, 100)
    glVertex2f(1000, 100)
    glVertex2f(1000, 700)
    glVertex2f(0, 700)
    glEnd()
    
    # cockpit details gula
    glColor3f(0.2, 0.2, 0.2)
    # Left side panel
    glBegin(GL_QUADS)
    glVertex2f(0, 100); glVertex2f(50, 100); glVertex2f(50, 700); glVertex2f(0, 700)
    glEnd()
    # Right side panel
    glBegin(GL_QUADS)
    glVertex2f(950, 100); glVertex2f(1000, 100); glVertex2f(1000, 700); glVertex2f(950, 700)
    glEnd()
    
    #cockpit instruments
    glColor3f(0.4, 0.4, 0.4)
    # Compass
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(100, 650)
    # Center
    for i in range(20):
        angle = 2 * math.pi * i / 20
        x = 30 * math.cos(angle)
        y = 30 * math.sin(angle)
        glVertex2f(100 + x, 650 + y)
    glEnd()
    
    # Depth gauge
    glBegin(GL_QUADS)
    glVertex2f(850, 150); glVertex2f(900, 150); glVertex2f(900, 250); glVertex2f(850, 250)
    glEnd()
    
    # indicator
    glBegin(GL_QUADS)
    glVertex2f(850, 300); glVertex2f(900, 300); glVertex2f(900, 400); glVertex2f(850, 400)
    glEnd()
    
    glEnable(GL_DEPTH_TEST); glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, center=False):
    if center: #text ke center kora
        text_width = sum(glutBitmapWidth(font, ord(ch)) for ch in text); 
        x -= text_width / 2
    glColor3f(1, 1, 1); glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0, 1000, 0, 800); glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity(); glDisable(GL_DEPTH_TEST); glRasterPos2f(x, y)
    
    # Prottek character draw kora
    for ch in text: 
        glutBitmapCharacter(font, ord(ch))
    glEnable(GL_DEPTH_TEST); glMatrixMode(GL_MODELVIEW); glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)

#keyboardfuncc
def keyboardListener(key, x, y):
    global game_state, target_word, player_pos, player_rotation_y
    # Game restart or exit
    if key == b'r' and (game_state == STATE_GAME_OVER or game_state == STATE_YOU_WIN): 
        initialize_game()
    if key == b'c' and (game_state == STATE_GAME_OVER or game_state == STATE_YOU_WIN): 
        glutLeaveMainLoop()

    # Pause/play     
    if key == b' ' and game_state == STATE_PLAYING: 
        game_state = STATE_PAUSED
    elif key == b' ' and game_state == STATE_PAUSED: 
        game_state = STATE_PLAYING
    #Enter key menu navigation er jonno
    if key == b'\r': #restart shob abar shurute niye gese reset e
        if game_state == STATE_SUB_SELECT:
            game_state = STATE_WORD_SELECT
        elif game_state == STATE_WORD_SELECT:
            target_word = WORDS[selected_word_index]
            reset_level()
            game_state = STATE_PLAYING
    if game_state == STATE_PLAYING:
        # Movement relative to player's current orientation
        # player_rotation_y is the yaw (rotation around Y-axis)
        angle_rad = math.radians(player_rotation_y)
        strafe_speed = 6.0

        # A & D key diye left-right movement
        if key == b'a': # Move lft 
            player_pos[0] -= math.cos(angle_rad) * strafe_speed
            player_pos[2] -= math.sin(angle_rad) * strafe_speed
        if key == b'd': # Move rt
            player_pos[0] += math.cos(angle_rad) * strafe_speed
            player_pos[2] += math.sin(angle_rad) * strafe_speed
        
        # W and S for up/down
        if key == b'w': 
            player_pos[1] = min(350, player_pos[1] + 8)  # Move up with limit
        if key == b's': 
            player_pos[1] = max(50, player_pos[1] - 8)   # Move down with limit

#arrow gula
def specialKeyListener(key, x, y):
    global selected_sub, selected_word_index, game_state, target_word, camera_angle_h, camera_angle_v, player_rotation_y
    # Submarine select menu te
    if game_state == STATE_SUB_SELECT:
        if key == GLUT_KEY_RIGHT:
            selected_sub = (selected_sub + 1) % 3
        elif key == GLUT_KEY_LEFT:
            selected_sub = (selected_sub - 1 + 3) % 3
        elif key == GLUT_KEY_RETURN:  # Enter key support
            game_state = STATE_WORD_SELECT

    # Word select menu        
    elif game_state == STATE_WORD_SELECT:
        if key == GLUT_KEY_DOWN:
            selected_word_index = (selected_word_index + 1) % len(WORDS)
        elif key == GLUT_KEY_UP:
            selected_word_index = (selected_word_index - 1 + len(WORDS)) % len(WORDS)
        elif key == GLUT_KEY_RETURN: # Enter key
            target_word = WORDS[selected_word_index]
            reset_level()
            game_state = STATE_PLAYING
    #Playing mode: left-right arrow diye submarine rotate        
    elif game_state == STATE_PLAYING:
        
        if key == GLUT_KEY_LEFT:
            player_rotation_y = (player_rotation_y + 5) % 360
        elif key == GLUT_KEY_RIGHT:
            player_rotation_y = (player_rotation_y - 5 + 360) % 360

#mouse er kaaj
def mouseListener(button, state, x, y):
    global is_first_person, game_state

    #mouse e rright click korle first person view
    if game_state == STATE_SUB_SELECT and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN: 
        game_state = STATE_WORD_SELECT
    elif game_state == STATE_PLAYING and button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN: 
        is_first_person = not is_first_person

# view
def setupCamera():
    glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(75, 1.25, 1.0, 5000.0); glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    if game_state == STATE_SUB_SELECT or game_state == STATE_WORD_SELECT:
        gluLookAt(0, 150, 400, 0, 150, 0, 0, 1, 0); return
    # Victory camera
    if game_state == STATE_YOU_WIN:
        orbit_radius = 200
        cam_x = player_pos[0] + math.sin(victory_angle) * orbit_radius
        cam_z = player_pos[2] + math.cos(victory_angle) * orbit_radius
        cam_y = player_pos[1] + 50
        gluLookAt(cam_x, cam_y, cam_z, player_pos[0], player_pos[1], player_pos[2], 0, 1, 0)
        return
        
    # Playing mode camera calculation
    player_rotation_y_rad = math.radians(player_rotation_y)
    forward_x = -math.sin(player_rotation_y_rad)
    forward_z = -math.cos(player_rotation_y_rad)
    if is_first_person:
        # First-person view
        cam_x = player_pos[0] + forward_x * 10 # Small offset forward
        cam_y = player_pos[1] + 10 # Eye level
        cam_z = player_pos[2] + forward_z * 10 # Small offset forward
        look_at_x = player_pos[0] + forward_x * 100
        look_at_y = player_pos[1] + 10
        look_at_z = player_pos[2] + forward_z * 100
        
        gluLookAt(cam_x, cam_y, cam_z, look_at_x, look_at_y, look_at_z, 0, 1, 0)
    else:
        # Third-person view
        cam_x = player_pos[0] - forward_x * camera_distance
        cam_y = player_pos[1] + camera_distance * 0.7 # Slightly above
        cam_z = player_pos[2] - forward_z * camera_distance
        # Look at the player's position
        gluLookAt(cam_x, cam_y, cam_z, player_pos[0], player_pos[1], player_pos[2], 0, 1, 0)

#movement gula or animation
def idle():
    global animation_angle, player_pos, score, game_state, target_letter_obj, target_letter_index, letter_spawn_timer, hearts_collected, jellyfish_collisions, player_speed, victory_angle, barrel_roll_angle, jellyfish_speed_multiplier
    animation_angle += 0.02
    # Victory animations
    if game_state == STATE_YOU_WIN:
        victory_angle += 0.03  # Orbit kortesi camera around submarine
        barrel_roll_angle += 8  # Barrel roll animation
        if barrel_roll_angle >= 360:
            barrel_roll_angle = 0
        glutPostRedisplay()
        return
        
    if game_state != STATE_PLAYING: 
        glutPostRedisplay()
        return
    
    #time calculate kori
    elapsed_time = time.time() - start_time
    
    #time er upor depend kore speed barai
    player_speed = initial_speed + (elapsed_time * 0.2)  # Speed increases by 0.2 every second
    
    #jelly fish er speed bartese
    jellyfish_speed_multiplier = 1.0 + (elapsed_time * 0.05)  # Increases by 0.05 every second
    
    #submarine nije nije shamne jacche nonstop
    player_rotation_y_rad = math.radians(player_rotation_y)
    player_pos[0] += -math.sin(player_rotation_y_rad) * player_speed # Move along X
    player_pos[2] += -math.cos(player_rotation_y_rad) * player_speed # Move along Z

    for jelly in jellyfish:
        current_speed = jelly['base_speed'] * jellyfish_speed_multiplier
        
        # Calculate kortesi direction to player
        dx = player_pos[0] - jelly['pos'][0]
        dy = player_pos[1] - jelly['pos'][1]
        dz = player_pos[2] - jelly['pos'][2]
        distance_to_player = math.sqrt(dx*dx + dy*dy + dz*dz)
        forward_x = -math.sin(player_rotation_y_rad)
        forward_z = -math.cos(player_rotation_y_rad)
        
        if distance_to_player > 0:
            dx /= distance_to_player
            dy /= distance_to_player
            dz /= distance_to_player
        
       #jellyfish ki submarine er shamne naki
        dot_product = forward_x * dx + forward_z * dz
        
       # Player samne thakle chase
        if dot_product > 0.3:  # In front field of view
            #time-based difficulty barai(0 to 1 over 60 seconds)
            difficulty_factor = min(1.0, elapsed_time / 60.0)
            
            # Apply attraction force towards player based on aggression and difficulty
            base_attraction = 0.03
            attraction_strength = jelly['aggression'] * base_attraction * (0.3 + 0.7 * difficulty_factor)
            
            jelly['vel'][0] += dx * attraction_strength
            jelly['vel'][1] += dy * attraction_strength
            jelly['vel'][2] += dz * attraction_strength
            
            # If very close to player, increase agano
            if distance_to_player < 200:
                jelly['vel'][0] += dx * 0.02 * difficulty_factor
                jelly['vel'][1] += dy * 0.02 * difficulty_factor
                jelly['vel'][2] += dz * 0.02 * difficulty_factor
        else:
            # Player pichone thakle random move
            jelly['direction_change_timer'] += 1
            if jelly['direction_change_timer'] > 60:  # Change direction more frequently when behind
                jelly['vel'][0] = random.uniform(-1.0, 1.0)
                jelly['vel'][1] = random.uniform(-0.5, 0.5)
                jelly['vel'][2] = random.uniform(-1.0, 1.0)
                jelly['direction_change_timer'] = 0
        
        # Velocity limit
        max_velocity = 1.5 + (elapsed_time * 0.08)  
        vel_magnitude = math.sqrt(jelly['vel'][0]**2 + jelly['vel'][1]**2 + jelly['vel'][2]**2)
        if vel_magnitude > max_velocity:
            jelly['vel'][0] = (jelly['vel'][0] / vel_magnitude) * max_velocity
            jelly['vel'][1] = (jelly['vel'][1] / vel_magnitude) * max_velocity
            jelly['vel'][2] = (jelly['vel'][2] / vel_magnitude) * max_velocity
        
        # Update position speed er shthe shthe
        jelly['pos'][0] += jelly['vel'][0] * current_speed
        jelly['pos'][1] += jelly['vel'][1] * current_speed
        jelly['pos'][2] += jelly['vel'][2] * current_speed
        
       
        jelly['direction_change_timer'] += 1
        
        
        direction_change_interval = max(30, jellyfish_direction_change_base - (elapsed_time * 2))
        
        # Change korbo direction when timer exceeds interval
        if jelly['direction_change_timer'] > direction_change_interval:
            # player ke shamne rekhe randomness add korchi
            if dot_product > 0.3:
                random_factor = 0.6  # Keep some forward momentum
                jelly['vel'][0] = jelly['vel'][0] * (1-random_factor) + random.uniform(-1.5, 1.5) * random_factor
                jelly['vel'][1] = jelly['vel'][1] * (1-random_factor) + random.uniform(-0.8, 0.8) * random_factor
                jelly['vel'][2] = jelly['vel'][2] * (1-random_factor) + random.uniform(-1.5, 1.5) * random_factor
            else:
                jelly['vel'][0] = random.uniform(-1.5, 1.5)
                jelly['vel'][1] = random.uniform(-0.8, 0.8)
                jelly['vel'][2] = random.uniform(-1.5, 1.5)
            jelly['direction_change_timer'] = 0
        
        # Boundary checks to keep jellyfish in play area
        # X boundary
        if jelly['pos'][0] < player_pos[0] - 1500 or jelly['pos'][0] > player_pos[0] + 1500:
            jelly['vel'][0] *= -1
        
        # Y boundary (keep within water column)
        if jelly['pos'][1] < 50 or jelly['pos'][1] > 250:
            jelly['vel'][1] *= -1
    
    # Respawn hearts and jellyfish
    for obj_list, spawn_y_range in [(hearts, [50, 250]), (jellyfish, [50, 250])]:
        for obj in obj_list:
            # If object is too far behind, move it far ahead
            if obj['pos'][2] > player_pos[2] + 500: # If it's passed the player and is now behind the camera view
                obj['pos'][2] = player_pos[2] - 3000 + random.uniform(-500, 500) # Move it far ahead
                obj['pos'][0] = player_pos[0] + random.uniform(-1500, 1500)
                obj['pos'][1] = random.uniform(spawn_y_range[0], spawn_y_range[1])
                # If it's a jellyfish, reset movement properties
                if obj in jellyfish:
                    obj['vel'] = [random.uniform(-1.5, 1.5), random.uniform(-0.8, 0.8), random.uniform(-1.5, 1.5)]
                    obj['direction_change_timer'] = random.randint(0, 120)
                    obj['pulse_phase'] = random.uniform(0, 2 * math.pi)
                    obj['base_speed'] = random.uniform(0.8, 1.2)
                    obj['aggression'] = random.uniform(0.2, 0.5)
                # If it's a heart, reset pump animation
                elif obj in hearts:
                    obj['pump_phase'] = random.uniform(0, 2 * math.pi)
                    obj['pump_speed'] = random.uniform(0.05, 0.1)
            # If object is too far ahead, move it back into view (shouldn't happen with current logic, but good for robustness)
            elif obj['pos'][2] < player_pos[2] - 4000:
                obj['pos'][2] = player_pos[2] + 1000 + random.uniform(-500, 500)
                obj['pos'][0] = player_pos[0] + random.uniform(-1500, 1500)
                obj['pos'][1] = random.uniform(spawn_y_range[0], spawn_y_range[1])
                if obj in jellyfish:
                    obj['vel'] = [random.uniform(-1.5, 1.5), random.uniform(-0.8, 0.8), random.uniform(-1.5, 1.5)]
                    obj['direction_change_timer'] = random.randint(0, 120)
                    obj['pulse_phase'] = random.uniform(0, 2 * math.pi)
                    obj['base_speed'] = random.uniform(0.8, 1.2)
                    obj['aggression'] = random.uniform(0.2, 0.5)
                elif obj in hearts:
                    obj['pump_phase'] = random.uniform(0, 2 * math.pi)
                    obj['pump_speed'] = random.uniform(0.05, 0.1)
    
    # Respawn fish
    for fish_list, spawn_y_range in [(fish_small, [50, 350]), (fish_large, [100, 300])]:
        for fish in fish_list:
            if fish['pos'][2] > player_pos[2] + 500:
                fish['pos'][2] = player_pos[2] - 3000 + random.uniform(-500, 500)
                fish['pos'][0] = player_pos[0] + random.uniform(-2000, 2000)
                fish['pos'][1] = random.uniform(spawn_y_range[0], spawn_y_range[1])
            elif fish['pos'][2] < player_pos[2] - 4000:
                fish['pos'][2] = player_pos[2] + 1000 + random.uniform(-500, 500)
                fish['pos'][0] = player_pos[0] + random.uniform(-2000, 2000)
                fish['pos'][1] = random.uniform(spawn_y_range[0], spawn_y_range[1])
            
    # Respawn seabed objects (seaweed, rocks, corals)
    # # These need a larger and more robust recycling mechanism
    for obj_list in [seaweed, seabed_rocks, corals]:
        for obj in obj_list:
            # If object is too far behind, move it far ahead
            if obj['pos'][2] > player_pos[2] + 2000: # Check if it's well behind the player's current view
                obj['pos'][2] = player_pos[2] - 5000 + random.uniform(-1000, 1000) # Move it to the far end of the "active" zone
                obj['pos'][0] = player_pos[0] + random.uniform(-5000, 5000)
                # If it's seaweed, reset sway animation
                if obj in seaweed and 'sway_phase' in obj:
                    obj['sway_phase'] = random.uniform(0, 2 * math.pi)
            # If object is too far ahead, move it back (less likely but for completeness)
            elif obj['pos'][2] < player_pos[2] - 5000:
                obj['pos'][2] = player_pos[2] + 2000 + random.uniform(-1000, 1000)
                obj['pos'][0] = player_pos[0] + random.uniform(-5000, 5000)
                if obj in seaweed and 'sway_phase' in obj:
                    obj['sway_phase'] = random.uniform(0, 2 * math.pi)
    
    if not target_letter_obj and target_letter_index < len(target_word):
        letter_spawn_timer += 1
        if letter_spawn_timer > 120:
            letter_spawn_timer = 0
            char_to_spawn = target_word[target_letter_index]
            # Spawn letter relative to player's current position, ahead of them
            target_letter_obj = {'char': char_to_spawn, 'pos': [player_pos[0] + random.uniform(-200, 200), random.uniform(100, 200), player_pos[2] - 1000]}
            
    if target_letter_obj:
        distance = math.sqrt(sum([(pc - lc)**2 for pc, lc in zip(player_pos, target_letter_obj['pos'])]))
        if distance < 60:
            target_letter_index += 1
            target_letter_obj = None
            if target_letter_index >= len(target_word): 
                game_state = STATE_YOU_WIN
        # If letter passes the player (is now behind them), despawn it
        elif target_letter_obj['pos'][2] > player_pos[2] + 50: 
            target_letter_obj = None
            
    for heart in hearts[:]:
        distance = math.sqrt(sum([(pc - hc)**2 for pc, hc in zip(player_pos, heart['pos'])]))
        if distance < 50: 
            score += 50 if heart['type'] == 'pink' else 10
            hearts_collected += 1
            hearts.remove(heart)
            # Respawn a new heart
            hearts.append({
                'pos': [player_pos[0] + random.uniform(-1500, 1500), 
                       random.uniform(50, 250), 
                       player_pos[2] - 3000 + random.uniform(-500, 500)], 
                'type': 'red' if random.random() > 0.2 else 'pink',
                'pump_phase': random.uniform(0, 2 * math.pi),
                'pump_speed': random.uniform(0.05, 0.1)
            })
            
    for jelly in jellyfish[:]:
        distance = math.sqrt(sum([(pc - jc)**2 for pc, jc in zip(player_pos, jelly['pos'])]))
        if distance < 50:
            # Updated scoring: -100 for red jellyfish, -50 for purple jellyfish
            if jelly['type'] == 'red':
                score -= 100
            else:  # purple
                score -= 50
                
            jellyfish_collisions += 1
            jellyfish.remove(jelly)
            # Respawn a new jellyfish
            jellyfish.append({
                'pos': [player_pos[0] + random.uniform(-1500, 1500), 
                       random.uniform(50, 250), 
                       player_pos[2] - 3000 + random.uniform(-500, 500)], 
                'type': 'purple' if random.random() > 0.3 else 'red', 
                'bob_speed': random.uniform(0.2, 0.5), 
                'tentacle_speed': random.uniform(2,4),
                'vel': [random.uniform(-1.5, 1.5), random.uniform(-0.8, 0.8), random.uniform(-1.5, 1.5)],
                'direction_change_timer': random.randint(0, 120),
                'pulse_phase': random.uniform(0, 2 * math.pi),
                'base_speed': random.uniform(0.8, 1.2),
                'aggression': random.uniform(0.2, 0.5)
            })
            if score < 0: 
                game_state = STATE_GAME_OVER
                
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Background Gradient (Dynamic based on depth)
    glDisable(GL_DEPTH_TEST); glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0,1,0,1); glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    
    # Calculate depth factor (0 at surface, 1 at max depth)
    depth_factor = 1.0 - ((player_pos[1] - 50) / (350 - 50)) #submarine er position theke depth calculate
    depth_factor = max(0.0, min(1.0, depth_factor)) # Clamp between 0 and 1
    # Bottom color 
    bottom_r = 0.1 * (1 - depth_factor) + 0.0 * depth_factor
    bottom_g = 0.2 * (1 - depth_factor) + 0.0 * depth_factor
    bottom_b = 0.5 * (1 - depth_factor) + 0.1 * depth_factor
    # Top color 
    top_r = 0.4 * (1 - depth_factor) + 0.05 * depth_factor
    top_g = 0.7 * (1 - depth_factor) + 0.05 * depth_factor
    top_b = 1.0 * (1 - depth_factor) + 0.2 * depth_factor
    glBegin(GL_QUADS) # 2D rectangle draw kora
    glColor3f(bottom_r, bottom_g, bottom_b); glVertex2f(0,0)
    glColor3f(bottom_r, bottom_g, bottom_b); glVertex2f(1,0)
    glColor3f(top_r, top_g, top_b); glVertex2f(1,1)
    glColor3f(top_r, top_g, top_b); glVertex2f(0,1)
    glEnd()
    glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW); glEnable(GL_DEPTH_TEST)
    
    setupCamera()
    #main logic
    if game_state == STATE_SUB_SELECT: # Sub selection screen
        # Left sub
        glPushMatrix(); glTranslatef(-250, 150, 0); draw_submarine(0, selected_sub == 0); glPopMatrix()
        # Middle sub
        glPushMatrix(); glTranslatef(0, 150, 0);   draw_submarine(1, selected_sub == 1); glPopMatrix()
        # Right sub
        glPushMatrix(); glTranslatef(250, 150, 0);  draw_submarine(2, selected_sub == 2); glPopMatrix()
    elif game_state in [STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER, STATE_YOU_WIN, STATE_WORD_SELECT]:
        draw_environment() # Pura sea environment draw kora

        if game_state in [STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER, STATE_YOU_WIN]:
            draw_letter(target_letter_obj)   #Target letter draw kora
            glPushMatrix()
            glTranslatef(*player_pos)
            glRotatef(player_rotation_y, 0,1,0) 

            # First person na hole sub draw

            if not is_first_person:
                draw_submarine(selected_sub, False, game_state == STATE_YOU_WIN)
            glPopMatrix()
            
            if is_first_person and game_state == STATE_PLAYING:
                draw_cockpit_view()
    #borders
    if game_state == STATE_PLAYING:
        draw_border()
    
    if game_state == STATE_PAUSED:
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity(); glDisable(GL_DEPTH_TEST)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(1000, 0)
        glVertex2f(1000, 800)
        glVertex2f(0, 800)
        glEnd()
        
        # Draw grid 
        glColor3f(0.2, 0.2, 0.2)
        glLineWidth(1.0)
        grid_size = 20
        glBegin(GL_LINES)

        # Vertical lines
        for x in range(0, 1001, grid_size):
            glVertex2f(x, 0)
            glVertex2f(x, 800)
        # Horizontal lines
        for y in range(0, 801, grid_size):
            glVertex2f(0, y)
            glVertex2f(1000, y)
        glEnd()
        
        glEnable(GL_DEPTH_TEST); glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)
    
    # Text-based ja amra dekhbo
    if game_state == STATE_SUB_SELECT:
        draw_text(500, 750, "CHOOSE YOUR SUBMARINE", font=GLUT_BITMAP_TIMES_ROMAN_24, center=True)
        draw_text(500, 50, "Use Arrow Keys to Select and press Enter", center=True)
    elif game_state == STATE_WORD_SELECT:
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0, 1000, 0, 800);
        glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity();
        glDisable(GL_DEPTH_TEST)
        draw_text(500, 750, "CHOOSE YOUR TARGET WORD", font=GLUT_BITMAP_TIMES_ROMAN_24, center=True)
        draw_text(500, 50, "Use Up/Down Arrows to Select, Enter to Continue", center=True)
        
        for i, word in enumerate(WORDS): # Word width calculate
            glPushMatrix()
            text_width = sum(glutStrokeWidth(GLUT_STROKE_ROMAN, ord(ch)) for ch in word)
            
            if i == selected_word_index:
                scale = 0.2
                glTranslatef(500 - (text_width * scale / 2), 600 - i * 60, 0)
                glColor3f(1.0, 1.0, 1.0)
                glLineWidth(3.0)
                glScalef(scale, scale, scale)
            else:
                scale = 0.15
                glTranslatef(500 - (text_width * scale / 2), 600 - i * 60, 0)
                glColor3f(0.7, 0.7, 0.7)
                glLineWidth(1.0)
                glScalef(scale, scale, scale)
            for ch in word:
                glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
            glPopMatrix()
        
        glEnable(GL_DEPTH_TEST); glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)
    elif game_state in [STATE_PLAYING, STATE_PAUSED]:
        draw_text(10, 770, f"Score: {score}")
        draw_text(10, 740, f"Target: {target_word} ({target_letter_index}/{len(target_word)})")
        draw_text(10, 710, f"Speed: {player_speed:.1f}")
        draw_text(10, 680, f"Jellyfish Speed: {jellyfish_speed_multiplier:.1f}x")
        
        if game_state == STATE_PAUSED:
            draw_text(500, 500, "PAUSED", font=GLUT_BITMAP_TIMES_ROMAN_24, center=True)
            draw_text(500, 450, "CONTROLS:", font=GLUT_BITMAP_HELVETICA_18, center=True)
            draw_text(500, 420, "A - Move Right, D - Move Left", center=True)
            draw_text(500, 390, "W - Move Up, S - Move Down", center=True)
            draw_text(500, 360, "Arrow Keys - Rotate Submarine (Yaw)", center=True)
            draw_text(500, 330, "Right Click - Toggle First Person View", center=True)
            draw_text(500, 300, "Space - Resume Game", center=True)
    #game over hole ja ja lekha thakbe       
    elif game_state == STATE_GAME_OVER:
        time_survived = int(time.time() - start_time)
        draw_text(500, 550, "GAME OVER", font=GLUT_BITMAP_TIMES_ROMAN_24, center=True)
        draw_text(500, 500, f"Final Score: {score}", center=True)
        draw_text(500, 470, f"Time Survived: {time_survived}s", center=True)
        draw_text(500, 440, f"Hearts Collected: {hearts_collected}", center=True)
        draw_text(500, 410, f"Jellyfish Collisions: {jellyfish_collisions}", center=True)
        draw_text(500, 380, f"Target Progress: {target_letter_index}/{len(target_word)}", center=True)
        draw_text(500, 350, f"Max Jellyfish Speed: {jellyfish_speed_multiplier:.1f}x", center=True)
        draw_text(500, 300, "Press 'R' to Restart or 'C' to Close", center=True)
    #game win hole ja lekha thakbe    
    elif game_state == STATE_YOU_WIN:
        time_taken = int(time.time() - start_time)
        draw_text(500, 550, "VICTORY!", font=GLUT_BITMAP_TIMES_ROMAN_24, center=True)
        draw_text(500, 500, f"Word Completed: {target_word}", center=True)
        draw_text(500, 470, f"Final Score: {score}", center=True)
        draw_text(500, 440, f"Time Taken: {time_taken}s", center=True)
        draw_text(500, 410, f"Hearts Collected: {hearts_collected}", center=True)
        draw_text(500, 380, f"Jellyfish Avoided: {25 - jellyfish_collisions}", center=True) # Assuming 25 jellyfish initially
        draw_text(500, 350, f"Max Jellyfish Speed: {jellyfish_speed_multiplier:.1f}x", center=True)
        draw_text(500, 300, "Press 'R' to Play Again or 'C' to Close", center=True)
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1200, 800)
    glutInitWindowPosition(50, 50)
    wind = glutCreateWindow(b"Submarine Word Hunt ")
    glEnable(GL_DEPTH_TEST)
    initialize_game()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()