# Author    :Maze Elva
# Date      :2.20.2026
# Title     :Physics sim 1 - Bouncing balls
# Purpose   :Create a bouncing ball that is affected by gravity

# Import Packages
import pygame, math, random, sys
import pygame.key
from pygame.locals import *

# Initialize Pygame
pygame.init()

"""CONSTANTS"""
# Window Settings
WIN_WID = (1920 * (2/3))
WIN_HEI = (1080 * (2/3))
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
DRAG = .98
BALL_LIM = 25

# Gravity
GRAVITY = .98
""""""

# Window Creation
window = pygame.display.set_mode((WIN_WID, WIN_HEI))
window.fill(BLACK)
pygame.display.set_caption(WIN_TITLE)

# Class to hold the ball object
class Ball(pygame.sprite.Sprite):
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

    def setup(self):
        # Ball Vectors
        self.ball_vx = 10
        self.ball_vy = 0

        # Ball Attr
        self.pos = [self.x_pos, self.y_pos]
        self.ball = None

    # Update Function
    def move(self):
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

            # Wall Collision(
            ## (Side Walls
            ### Right
            if self.pos_x > self.wall_r:
                self.pos[0] = self.wall_r
                self.ball_vx *= -1
                

            ### Left)
            if self.pos_x < self.wall_l:
                self.pos[0] = self.wall_r
                self.ball_vy *= -1

            ## Height Walls(
            ### Bottom
            if self.pos_y > self.floor:
                self.pos[1] = self.floor
                self.ball_vy *= .75
                self.ball_vy *= -1

            ### Top)
            elif self.pos_y <= self.ceiling:
                self.pos[1] = self.ceiling
                self.ball_vy *= -1
            # )

            # Stop if on floor
            if self.pos_y >= self.floor and -2 < self.ball_vy < 2:
                self.pos[1] = self.floor
                self.pos_x *= .75
                self.ball_vy = 0
                if -.5 < self.ball_vx < .5:
                    self.ball_vx = 0
                    
    # Draw Function
    def draw(self, surface):
        self.ball = pygame.draw.circle(window, WHITE, self.pos, self.radius)

# Local list for the ball objects
ball_list = []

# Position Reset
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

# Ball Creation
Reset(ball_list)
for ball in ball_list:
    ball.setup()

# Print control instructions
print('Press "R" to reset. \nPress "ESC" to close')

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
        ball.move()
        ball.draw(window)

# Tickrate
    pygame.display.update()
    FRAMES_PER_SEC.tick(FPS)
