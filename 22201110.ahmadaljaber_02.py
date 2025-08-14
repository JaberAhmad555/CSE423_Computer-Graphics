from OpenGL.GL import *  #graphics functions:drawing points, lines
from OpenGL.GLUT import * # For creating windows and handling keyboard/mouse input
from OpenGL.GLU import * #use it for the 2D
import time  #to make animation smooth on any computer
import random  #jejonno diamond ek ek jayga theke topkay
def draw_pixel(x,y,color):   
    glColor3f(color[0],color[1],color[2]) # Set the color for the next pixel
    glPointSize(1.0) #pixel size 1x1
    glBegin(GL_POINTS) #starts drawing point
    glVertex2f(x,y) #cordinates
    glEnd() #end draw
def find_zone(dx,dy): 
    if abs(dx)>abs(dy):  #either near x 
        if dx>=0 and dy>=0:
            return 0
        elif dx<0 and dy>=0:
            return 3
        elif dx<0 and dy<0:
            return 4
        else: 
            return 7
    else:       # or near y
        if dx>=0 and dy>=0:
            return 1
        elif dx<0 and dy>=0:
            return 2
        elif dx<0 and dy<0:
            return 5
        else: 
            return 6
def convert_to_zone0(x,y,zone):
    if zone==0:
        return x,y
    elif zone==1:
        return y,x
    elif zone==2:
        return y,-x
    elif zone==3:
        return -x,y
    elif zone==4:
        return -x,-y
    elif zone==5:
        return -y,-x
    elif zone==6:
        return -y,x
    elif zone == 7:
        return x,-y
    return x,y
def convert_from_zone0(x,y,zone):
    if zone==0:
        return x,y
    elif zone==1:
        return y,x
    elif zone==2:
        return -y,x
    elif zone==3:
        return -x,y
    elif zone==4:
        return -x,-y
    elif zone==5:
        return -y,-x
    elif zone==6:
        return y,-x
    elif zone==7:
        return x,-y
    return x,y
def draw_line_midpoint(x1,y1,x2,y2,color):
    dx =x2-x1
    dy =y2-y1
    zone =find_zone(dx,dy) 
    x1_conv, y1_conv=convert_to_zone0(x1,y1,zone)  
    x2_conv, y2_conv=convert_to_zone0(x2,y2,zone)
    if x1_conv>x2_conv: #we always draw left to right
        x1_conv,x2_conv=x2_conv,x1_conv
        y1_conv,y2_conv=y2_conv,y1_conv
    dx_conv=x2_conv-x1_conv
    dy_conv=y2_conv-y1_conv
    d =2*dy_conv-dx_conv #Helps decide the next pixel
    inc_e=2*dy_conv
    inc_ne=2*dy_conv-2*dx_conv
    x,y=x1_conv,y1_conv
    while x<=x2_conv:
        original_x, original_y = convert_from_zone0(x, y, zone)
        draw_pixel(original_x,original_y,color)
        if d>0:
            d+=inc_ne
            y+=1 #go NE
        else:
            d+=inc_e #go E
        x+=1
def draw_diamond(center_x,center_y,size,color):
    half_size=size/2
    p1=(center_x,center_y+size)
    p2=(center_x+half_size,center_y)
    p3=(center_x,center_y-size)
    p4=(center_x-half_size,center_y)
    draw_line_midpoint(p1[0],p1[1],p2[0],p2[1],color)
    draw_line_midpoint(p2[0],p2[1],p3[0],p3[1],color)
    draw_line_midpoint(p3[0],p3[1],p4[0],p4[1],color)
    draw_line_midpoint(p4[0],p4[1],p1[0],p1[1],color)
def draw_catcher(center_x,y_pos,width,height,color):
    half_width=width/2
    p1=(center_x-half_width,y_pos)
    p2=(center_x-half_width+height,y_pos+height)
    p3=(center_x+half_width-height,y_pos+height)
    p4=(center_x+half_width,y_pos)
    draw_line_midpoint(p1[0],p1[1],p2[0],p2[1],color)
    draw_line_midpoint(p2[0],p2[1],p3[0],p3[1],color)
    draw_line_midpoint(p3[0],p3[1],p4[0],p4[1],color)
    draw_line_midpoint(p1[0],p1[1],p4[0],p4[1],color)
def draw_ui_buttons():
    teal=(0, 0.8, 0.8)
    draw_line_midpoint(40,480,20,460,teal)
    draw_line_midpoint(20,460,40,440,teal)
    amber=(1.0,0.75,0.0)
    if game_state['state']=='PLAYING': 
        draw_line_midpoint(240,480,240,440,amber)
        draw_line_midpoint(260,480,260,440,amber)
    else: 
        draw_line_midpoint(240,480,260,460,amber)
        draw_line_midpoint(260,460,240,440,amber)
    red = (1.0,0.0,0.0)
    draw_line_midpoint(460,480,480,440,red)
    draw_line_midpoint(480,480,460,440,red)
WINDOW_WIDTH, WINDOW_HEIGHT =500,500
game_state = {
    'score':0,
    'state':'PLAYING',  
    'last_frame_time':0,
}
catcher = {
    'x':WINDOW_WIDTH/2,
    'y':30,
    'width':100,
    'height':20,
    'speed':400,
    'color':(1.0,1.0,1.0)
}
diamond = {
    'x':WINDOW_WIDTH/2,
    'y':WINDOW_HEIGHT,
    'size':15,
    'speed':100,
    'color':(1.0,1.0,0.0)
}
def reset_diamond():
    diamond['y']=WINDOW_HEIGHT
    diamond['x']=random.randint(30,WINDOW_WIDTH-30)
    diamond['color']=(random.random(),random.random(),random.random())
def restart_game():
    print("Starting Over")
    game_state['score']=0
    game_state['state']='PLAYING'
    catcher['color']=(1.0,1.0,1.0)
    catcher['x']=WINDOW_WIDTH/2
    diamond['speed']=100
    reset_diamond()
def has_collided(box1,box2):
    return (box1['x']<box2['x']+box2['width'] and
            box1['x']+box1['width']>box2['x'] and
            box1['y']<box2['y']+box2['height'] and
            box1['y']+box1['height']>box2['y'])
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_ui_buttons()
    draw_catcher(catcher['x'],catcher['y'],catcher['width'],catcher['height'],catcher['color'])
    if game_state['state']!='GAME_OVER':
        draw_diamond(diamond['x'],diamond['y'],diamond['size'],diamond['color'])
    glutSwapBuffers()
def animate():
    current_time =time.time()
    delta_time =current_time-game_state['last_frame_time']
    game_state['last_frame_time']=current_time
    if game_state['state']=='PLAYING':
        diamond['y']-=diamond['speed']*delta_time
        diamond_bbox={'x': diamond['x']-diamond['size']/2,'y':diamond['y']-diamond['size'], 
                        'width':diamond['size'],'height':2*diamond['size']}
        catcher_bbox ={'x':catcher['x']-catcher['width']/2,'y':catcher['y'], 
                        'width':catcher['width'],'height':catcher['height']}
        if has_collided(diamond_bbox,catcher_bbox):
            game_state['score']+=1
            print(f"Score:{game_state['score']}")
            diamond['speed']+=10 
            reset_diamond()
        if diamond['y']<0:
            game_state['state']='GAME_OVER'
            catcher['color']=(1.0, 0.0, 0.0)
            print(f"Game Over! Score:{game_state['score']}")
    glutPostRedisplay()
def special_input(key,x,y):
    move_dist=catcher['speed']*0.05 
    if game_state['state']=='PLAYING':
        if key==GLUT_KEY_LEFT:
            catcher['x']-=move_dist
            if catcher['x']-catcher['width']/2 < 0:
                catcher['x']=catcher['width']/2
        elif key==GLUT_KEY_RIGHT:
            catcher['x']+=move_dist
            if catcher['x']+catcher['width']/2>WINDOW_WIDTH:
                catcher['x']=WINDOW_WIDTH-catcher['width']/2
def mouse_click(button,state,x,y):
    y =WINDOW_HEIGHT-y
    if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
        if 10<x<50 and 430<y<490:
            restart_game()
        elif 230<x<270 and 430<y<490:
            if game_state['state']=='PLAYING':
                game_state['state']='PAUSED'
            elif game_state['state']=='PAUSED':
                game_state['state']='PLAYING'
        elif 450<x<490 and 430<y<490:
            print(f"Goodbye! Final Score: {game_state['score']}")
            glutLeaveMainLoop()
def main():
    print("Catch the Diamonds! Game Started.")
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH,0,WINDOW_HEIGHT)
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_input)
    glutMouseFunc(mouse_click)
    game_state['last_frame_time'] =time.time()
    glutMainLoop()
if __name__ == "__main__":
    main()