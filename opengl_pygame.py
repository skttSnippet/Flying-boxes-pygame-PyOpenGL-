#########################################################################################
'''

'''
#########################################################################################

import random

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


box_len = 2
#number stands for coordinates
vertices  = (
        ( box_len,-box_len,-box_len),
        ( box_len, box_len,-box_len),
        (-box_len, box_len,-box_len),
        (-box_len,-box_len,-box_len),
        ( box_len,-box_len, box_len),
        ( box_len, box_len, box_len),
        (-box_len, box_len, box_len),
        (-box_len,-box_len, box_len),
            )

#number stands for index in tuple  vertices
edges = (
        (0,1),
        (0,3),
        (0,4),
        (2,1),
        (2,3),
        (2,6),
        (5,1),
        (5,4),
        (5,6),
        (7,3),
        (7,4),
        (7,6),
        )

#numbers stands for index in tuple  vertices
surfaces = (
        (0,1,5,4),
        (0,3,2,1),
        (0,4,7,3),
        (6,2,1,5),
        (6,7,4,5),
        (6,2,3,7),
           )

colors = (
        (1,0,0),
        (0,1,0),
        (0,0,1),  
        (1,1,0),
        (1,0,1),
        (0,1,1),
        (1,0,0),
        (0,1,0),
        (0,0,1),  
        (1,1,0),
        (1,0,1),
        (0,1,1),
        )

# # create a ground if needed
# ground_vertices = (
#         (-10,-1.1,20),
#         (10,-1.1,20),
#         (-10,-1.1,-300),
#         (10,-1.1,-300),
#                    )
# def ground():
#     glBegin(GL_QUADS)
#     for vertex in ground_vertices:
#         glColor3fv((0,0.5,0.5))
#         glVertex3fv(vertex)
#     glEnd()



#
def setVertices(max_distance, min_distance=-20, camera_x=0, camera_y=0):
    ''''''

    camera_x = -1*int(camera_x)
    camera_y = -1*int(camera_y)

    x_value_change = random.randrange(camera_x-75,camera_x+75)
    y_value_change = random.randrange(camera_y-75,camera_y+75)
    z_value_change = random.randrange(-1*max_distance, min_distance)

    new_vertices = []

    for vert in vertices:
        new_vert = [] 

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)

    return new_vertices

#
def cube(vertices):
    ''''''
#    glBegin(GL_LINES)
#    for edge in edges:
#        for vertex in edge:
#            glVertex3fv( vertices[vertex])        
#    glEnd()

    glBegin(GL_QUADS)
    
    
    for surface in surfaces:
        x = 0    
        for vertex in surface:
            x+=1
            glColor3fv( colors[x] )
            glVertex3fv( vertices[vertex] )
    glEnd()


def main():
    ''''''
    pygame.init()
    display = (800,600)
    #need to specify OpenGL for pygame to show display
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    max_distance = 100

    #set (field of view, aspect ratio, near clipping plane, far clipping plane)
    gluPerspective(45, (display[0]/display[1]), 0.1, max_distance )

    glTranslatef(0,0,-40)

#    object_passed = False

    x_move = 0
    y_move = 0

    #current x and current y
    cur_x = 0
    cur_y = 0

    #speed at which boxes flying towards player camera
    game_speed = 2
    direction_speed = 2

    cube_dict = {}

    #populate 75 cubes with random coordinates generated by setVertices func
    for x in range(50):
        cube_dict[x] = setVertices(max_distance)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = direction_speed
                if event.key == pygame.K_RIGHT:
                    x_move = direction_speed*-1

                if event.key == pygame.K_UP:
                    y_move = direction_speed*-1
                if event.key == pygame.K_DOWN:
                    y_move = direction_speed


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0
                if event.key == pygame.K_UP   or event.key == pygame.K_DOWN:
                    y_move = 0  

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                if event.button == 4:
#                    glTranslatef(0,0,0.1)                
#                
#                if event.button == 5:
#                    glTranslatef(0,0,-0.1)                
                

        #(angle degree, axisX ,axisY, axisZ) 
        #axisXYZ defines a vector that object roatate around at angle degree
#        glRotatef(1, 1, 1, 1)

        x = glGetDoublev(GL_MODELVIEW_MATRIX)
#        print(x) #print out the matrix to keep track of it 

        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]

        cur_x += x_move
        cur_y += y_move

        #clear the frame between frames to draw a new frame
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glTranslatef(x_move, y_move, game_speed)

#        ground()

        #pass every element in cube_dict in cube func
        for each_cube in cube_dict:
            cube(cube_dict[each_cube])


        for each_cube in cube_dict:
            if camera_z <= cube_dict[each_cube][0][2]:
#                print ("passed a cube")
                new_max = int(-1*( camera_z - (max_distance*2) ))

                cube_dict[each_cube] = \
                setVertices(new_max, int(camera_z-max_distance), cur_x, cur_y)


#        pygame.display.update() # doesn't work, use .flip() instead
        pygame.display.flip()
#        pygame.time.wait(10)


main()

pygame.quit()
quit()



