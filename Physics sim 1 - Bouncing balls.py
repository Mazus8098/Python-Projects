# Author    :Maze Elva
# Date      :2.20.2026
# Title     :Physics sim 1 - Bouncing balls
# Purpose   :Create bouncing balls repeatedly that 
#           start with a random velocity, and 
#           become affected by Gravity and Drag

# Import Packages
import pygame, math, random, sys
import pygame.key
from pygame.locals import *

# Change that means nothing

# Initialize Pygame
pygame.init()

"""CONSTANTS"""
# Window Settings
WIN_WID = (1920*3/4)
WIN_HEI = (1080*3/4)
BOUNDARY_SIZE = 50
WIN_TITLE = 'Physics Sim 1'

# FPS
FPS = 60
FRAMES_PER_SEC = pygame.time.Clock()

# Colours
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)

# Ball Constants
RADIUS = 10
BALL_COUNT = 10
BALL_LIM = 25

# Forces
DRAG = .98
GRAVITY = .98
""""""

# Window Creation
window = pygame.display.set_mode((WIN_WID, WIN_HEI))
window.fill(BLACK)
pygame.display.set_caption(WIN_TITLE)

""" Class to hold the ball object """
class Ball(pygame.sprite.Sprite):
    """ Initialization """
    def __init__(self, x_pos, y_pos, radius):
        super().__init__()  
        # Local variables for the position and radius
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        
        # Boundaries
        self.floor = WIN_HEI -BOUNDARY_SIZE
        self.ceiling = BOUNDARY_SIZE
        self.wall_r = WIN_WID -BOUNDARY_SIZE
        self.wall_l = BOUNDARY_SIZE

    """ Setup """
    def setup(self):
        # Ball Vectors
        self.ball_vx = random.randint(-25, 25)
        self.ball_vy = random.randint(-25, 0)

        # Ball Attr
        self.pos = [self.x_pos, self.y_pos]
        self.ball = None

    """ Wall Collision """
    def wall_collide(self, pos_x, pos_y, vec_x, vec_y):
            #Side Walls
            ## Right
            if pos_x > self.wall_r:
                pos_x = self.wall_r
                vec_x *= -1
            ## Left
            if pos_x < self.wall_l:
                pos_x = self.wall_l
                vec_x *= -1

            # Height Walls
            ## Bottom
            if pos_y > self.floor:
                pos_y = self.floor
                vec_y *= -1
            ## Top
            elif pos_y <= self.ceiling:
                pos_y = self.ceiling
                vec_y *= -1

            # Stop if on floor
            if pos_y >= self.floor and -2 < vec_y < 2:
                pos_y = self.floor
                vec_y = 0
                vec_x *= .75
                if -.5 < vec_x < .5:
                    vec_x = 0

            return(pos_x, pos_y, vec_x, vec_y)

    
    """ Update Function """
    def update(self):
        # Only runs if the ball exits first
        if self.ball:

            # Sets the position to 2 X and Y values
            self.pos_x = float(self.pos[0])
            self.pos_y = float(self.pos[1])

            # Applies Gravity to the vectors
            self.ball_vy += GRAVITY
            
            # Movement
            self.pos[0] += self.ball_vx
            self.pos[1] += self.ball_vy
            self.ball_vx *= DRAG
            self.ball_vy *= DRAG

            self.pos[0], self.pos[1], self.ball_vx, self.ball_vy = (
                self.wall_collide(self.pos[0], self.pos[1], self.ball_vx, self.ball_vy))     

    """ Draw Function """
    def draw(self, surface):
        self.ball = pygame.draw.circle(window, WHITE, self.pos, self.radius)

# Local list for the ball objects
ball_list = []

""" Position Reset """
def Reset(ball_list):
    # Clear the list of balls
    ball_list.clear()
    for i in range(BALL_COUNT):
        # Create positions and apply those to objects
        xpos = random.randint(int(BOUNDARY_SIZE+RADIUS), int(WIN_WID-BOUNDARY_SIZE-RADIUS))
        ypos = random.randint(int(BOUNDARY_SIZE+RADIUS), int(WIN_HEI-BOUNDARY_SIZE-RADIUS))
        ball = Ball(xpos, ypos, RADIUS)
        # Add objects to the ball list
        ball_list.append(ball)
    # Call setup for each ball
    for ball in ball_list:
        ball.setup()
    return(ball_list)

# Print control instructions
print('Press "R" to reset. \nPress "ESC" to close \nClick to spawn a ball at the cursor')

""" Ball Creation """
Reset(ball_list)
for ball in ball_list:
    ball.setup()

# Run loop
while True:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        # Exit condition
        if key[K_ESCAPE] or event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Reset condition
        if key[K_r]:
            for ball in ball_list:
                ball_list.clear()
                ball_list = Reset(ball_list)

        # Ball spawning
        if event.type == pygame.MOUSEBUTTONDOWN and len(ball_list) < BALL_LIM:
            if event.button == 1:
                posx, posy = pygame.mouse.get_pos()
                ball = Ball(posx, posy, RADIUS)
                ball.setup()
                ball_list.append(ball)

# Window Refresh
    window.fill(BLACK)
    for ball in ball_list:
        ball.update()
        ball.draw(window)
    if all(ball.ball_vx == 0 and ball.ball_vy == 0 for ball in ball_list):
        Reset(ball_list)
        print('Resetting \n')
# Tickrate
    pygame.display.update()
    FRAMES_PER_SEC.tick(FPS)
