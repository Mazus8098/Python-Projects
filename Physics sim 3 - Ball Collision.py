# Author    :Maze Elva
# Date      :3.2.2026
# Title     :Physics sim 3 - Ball Collision
# Purpose   :Create balls affected by gravity, 
#            and able to collide with each other.

# Import Packages
import pygame, math, random, sys
import pygame.key
from pygame.locals import *

# Initialize Pygame
pygame.init()

"""CONSTANTS"""
# Window Settings
WIN_WID = (1920*3/4)
WIN_HEI = (1080*3/4)
BOUNDARY_SIZE = 50
WIN_TITLE = 'Physics Sim 3 - Collision'

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
RADIUS = 25
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

""" Class for the balls """
class Ball(pygame.sprite.Sprite):
    """Initialize """
    def __init__(self, pos_x, pos_y, radius):
        super().__init__()

        # Static ball variables
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rad = radius

        # Boundaries
        self.floor = WIN_HEI - BOUNDARY_SIZE
        self.cieling = BOUNDARY_SIZE
        self.wall_r = WIN_WID - BOUNDARY_SIZE
        self.wall_l = BOUNDARY_SIZE

    """ Setup """
    def setup(self):
        # Vectors
        self.vx = 0
        self.vy = 0 

        # Package position for the draw function
        self.pos = [self.pos_x, self.pos_y]


    """ Wall Collide """
    def wall_collide(self):
        pass

    """ Ball Collide """
    def self_collide(self):
        pass

    """ Update """
    def update(self):

        # Package position for the draw function
        self.pos = self.pos_x, self.pos_y

    """ Draw """
    def draw(self, surface):
        self.ball = pygame.draw.circle(window, WHITE, self.pos, self.rad)

# Local list for balls
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
    key = pygame.key.get_just_pressed()
    for event in pygame.event.get():

        # Exit condition
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Ball spawning
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                posx, posy = pygame.mouse.get_pos()
                ball = Ball(posx, posy, RADIUS)
                ball.setup()
                if BALL_LIM == len(ball_list):
                    ball_list.pop(0)
                ball_list.append(ball)

    # Manual Exit
    if key[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Reset condition
    if key[K_r]:
        for ball in ball_list:
            ball_list.clear()
            ball_list = Reset(ball_list)

# Window Refresh
    window.fill(BLACK)
    for ball in ball_list:
        ball.update()
        ball.draw(window)

# Tickrate
    pygame.display.update()
    FRAMES_PER_SEC.tick(FPS)