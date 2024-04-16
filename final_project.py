"""
Pong pro 1 hráče
Mikuláš Ptáček, 1.ročník
Zimní semestr 2022/23
Programování 1 NPRG030
"""

import sys
import pygame
import random

pygame.init()

#window parameters
window_width = 1000
window_height = 700
window_height_margin = 50
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("PONG pro 1 hráče")

# some nice colors
red = (220,20,60)
black = (0,0,0)
dark = (30,30,30)
white = (255,255,255)
green = (173,255,47)
yellow = (255,255,51)

# platform parameters
rect_normal_size = (100,20)
rect_width = 100
rect_height = 20
rect_x = window_width // 2
rect_y = window_height - rect_height - window_height_margin
rect_movement_x = 0
platform_speed = 3

#rectangle generation and borders
def platform(window,x,y):
    #left border
    if x <= 0:
        x = 0
    #right border
    elif x >= (window_width - rect_width):
        x = window_width - rect_width
    #generation
    pygame.draw.rect(window,yellow,[x,y,rect_width,rect_height])


#dot parameters
dot_radius = 10
dot_x = window_width / 2
dot_y = 0
dot_normal_speed = 2.5
dot_movement_y = dot_normal_speed
dot_movement_x = dot_normal_speed

#definition of borders
dot_lower_limit_rect_y = (window_height - window_height_margin)
dot_upper_limit_rect_y = (window_height - rect_height - window_height_margin)

#game difficulty
milestone_first = 4
milestone_second = 8
#randomization of the dot
def randomness_dot_x(positive):
    if positive == True:
       dot_movement_x = random.randrange(2,4)
    else:
        dot_movement_x = random.randrange(-4,-2)
    return (dot_movement_x)

def randomness_dot_y(positive):
    if positive == True:
        dot_movement_y = random.randrange(2,4)
    else:
            dot_movement_y = random.randrange(-4,-2)
    return (dot_movement_y)
#randomization of the rect
def randomness_rect_size():
    rect_width = random.randrange(rect_normal_size[0] / 2,rect_normal_size[0] * 2)
    return (rect_width)
def randomness_rect_speed():
    rect_movement_x = random.randint(platform_speed, 2 * platform_speed)
    return(rect_movement_x)

#game parameters   
FPS = 144
score = 0
highest = 0
clock = pygame.time.Clock()


#Main function (loop)
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        #end of the program
        if event.type == pygame.QUIT:
            running = False
            break
        #controls
        elif event.type == pygame.KEYDOWN: 
            #left keystroke     
            if event.key == pygame.K_LEFT:
                if score < milestone_first:
                    rect_movement_x = -platform_speed #movement left
                #randomness of the rect movement
                else:
                    rect_movement_x = -randomness_rect_speed()
            #right keystroke
            elif event.key == pygame.K_RIGHT:
                if score < milestone_first:
                    rect_movement_x = platform_speed #movement right
                #randomness of the rect movement
                else:
                    rect_movement_x = randomness_rect_speed()
        #key release
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                rect_movement_x = 0 #stop of the movement
    #updation position by movement
    rect_x += rect_movement_x
    
#bouncing of the dot
    #left border
    if dot_x < 0:
        dot_x = 0
        dot_movement_x = dot_movement_x * -1 #bounce right
    #right border
    elif dot_x > (window_width - dot_radius):
        dot_x = (window_width - dot_radius)
        dot_movement_x = dot_movement_x * -1 #bounce left
    #top border
    elif dot_y < 0:
        dot_y = 0
        dot_movement_y = dot_movement_y * -1 
    #bottom border
    elif dot_y > (window_height - dot_radius):
        dot_y = (window_height - dot_radius)
        dot_movement_y = dot_movement_y * -1
    #updating position by movement
    dot_x += dot_movement_x
    dot_y += dot_movement_y

#dot and platform interaction
    #dot hit from above
    if dot_x >= rect_x and dot_x <= (rect_x + rect_width) and dot_y == dot_upper_limit_rect_y:
        dot_movement_y = dot_movement_y * -1 #bounce up
        #score counter
        score += 1
        #randomization of the game by score count
        if score > milestone_first:
            rect_width = randomness_rect_size()
            if score > milestone_second:
                if dot_movement_x < 0:
                    dot_movent_x = randomness_dot_x(False)
                else:
                    dot_movent_x = randomness_dot_x(True)
                if dot_movement_y < 0:
                    dot_movent_y = randomness_dot_y(False)
                else:
                    dot_movent_y = randomness_dot_y(True)
    #dot hit from below    
    elif dot_x >= rect_x and dot_x <= (rect_x + rect_width) and dot_y == dot_lower_limit_rect_y:
        dot_movement_y = dot_movement_y * -1
    #dot hit from sides
    elif dot_x >= rect_x and dot_x <= (rect_x + rect_width) and (dot_y > dot_upper_limit_rect_y and dot_y < dot_lower_limit_rect_y):
        dot_movement_x = dot_movement_x * -1 #bounce to the sides
#dot hits bottom and resets the game
    elif dot_y > window_height - dot_radius - 1:
        #game reset
        if score > highest:
            highest = score
        score = 0
        rect_width = rect_normal_size[0]
        if dot_movement_x < 0:
            dot_movement_x = -dot_normal_speed
        else:
            dot_movement_x = dot_normal_speed
        dot_movement_y = dot_movement_y * -1

#object generation
    #screen
    window.fill(dark)
        #text
    printing = pygame.font.SysFont('Tickerbit', 30, False, False)
    points = printing.render("Score = " + str(score), True, green)
    most_points = printing.render("Highest score = " + str(highest), True, green)
    window.blit(points,[50,100])
    window.blit(most_points,[50,70])
    #platform
    platform(window, rect_x, rect_y)
    #dot
    pygame.draw.rect(window,red,[dot_x,dot_y,dot_radius,dot_radius])
       
    #regeneration of the screen
    pygame.display.flip()

    

pygame.quit()
