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
BALL_COUNT = 5
BALL_LIM = 5

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
    def __init__(self, pos_x, pos_y, radius, ball_list):
        super().__init__()

        # Global ball objects
        self.ball = None
        self.ball_list = ball_list

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

    """ Ball Collision """
    def ball_collide(self):
        """
        Take the position of each ball, and measure it with its neighbors. 
        If the centres are too close, the balls are overlapping
        """
        # Exits if only 1 ball exists
        if not len(ball_list) > 1:
            return

        # Checks the ball to others
        for other in self.ball_list:
            if other.pos_x != self.pos_x and other.pos_y != self.pos_y:
                # Get distance to neighbors
                dist_x = other.pos_x - self.pos_x
                dist_y = other.pos_y - self.pos_y
                dist = math.hypot(dist_x, dist_y)

                # Check if there is overlap
                if dist < self.rad * 2:
                    # Retrieve the difference in overlap
                    overlap_difference = dist - 2*(dist - self.rad)

                    # Update position to avoid overlap
                    if self.pos_x > other.pos_x:
                        self.pos_x += overlap_difference / 2
                    if self.pos_x < other.pos_x:
                        self.pos_x -= overlap_difference / 2

                    if self.pos_y > other.pos_y:
                        self.pos_y += overlap_difference / 2
                    if self.pos_y < other.pos_y:
                        self.pos_y -= overlap_difference / 2


                    # Update vectors to reflect on collision
                    """ NOT IMPLEMENTED YET """

                else:
                    print('no overlap')
                       
                    
    """ Wall Collide """
    def wall_collide(self):
        # Floor
        if self.ball.bottom > self.floor:
            self.pos_y = self.floor - self.rad
            self.vy *= -1
        # Cieling
        if self.ball.top < self.cieling:
            self.pos_y = self.cieling + self.rad
            self.vy *= -1
        # Left wall
        if self.ball.left < self.wall_l:
            self.pos_x = self.wall_l + self.rad
            self.vx *= -1
        # Right wall
        if self.ball.right > self.wall_r:
            self.pos_x = self.wall_r - self.rad
            self.vx *= -1

    """ Update """
    def update(self):
        # Leaves function if theres no ball to update
        if not self.ball:
            return

        # Specialized functions
        self.wall_collide()
        self.ball_collide()

        # Apply change to position
        self.pos_x += self.vx
        self.pos_y += self.vy

        # Get total speed
        self.speed = self.vx + self.vy

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
        ball = Ball(xpos, ypos, RADIUS, ball_list)

        # Add objects to the ball list
        ball_list.append(ball)

    # Call setup for each ball
    for ball in ball_list:
        ball.setup()

    return(ball_list)

# Print control instructions
print('Press "R" to reset. \nPress "ESC" to close \nLeft click to spawn a ball at the cursor \nRight click to randomize vectors')

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
                ball = Ball(posx, posy, RADIUS, ball_list)
                ball.setup()
                if BALL_LIM == len(ball_list):
                    ball_list.pop(0)
                ball_list.append(ball)

            """ 
            TEMP CONTROL 
            Applies random values to each 
            balls vectors upon right click
            """
            if event.button == 3:
                for ball in ball_list:
                    vx = random.randint(int(-(WIN_WID / 100)), int(WIN_WID / 100)) 
                    vy = random.randint(int(-(WIN_HEI / 100)), int(WIN_HEI / 100)) 
                    ball.vx = vx
                    ball.vy = vy

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