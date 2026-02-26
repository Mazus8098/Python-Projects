# Author:       Maze Elva
# Date:         2.24.2026
# Title:        Physics Sim 2 - Directional Movement
# Purpose:      Create a script that will choose a point in space, 
#               and then draw and follow that path to its end.

import pygame, math, random, sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

""" CONSTANTS """
# Window Settings
WIN_WID = 1920*3/4
WIN_HEI = 1080*3/4
BOUNDARY_SIZE = 50
WIN_TITLE = 'Directional Movement'

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
BALL_COUNT = 20
BALL_LIM = 100
SPD_MULT = 2
""""""

# Window Creation
window = pygame.display.set_mode((WIN_WID, WIN_HEI))
window.fill(BLACK)
pygame.display.set_caption(WIN_TITLE)

# Testing tools
testing = False

""" Class to create the object """
class Ball(pygame.sprite.Sprite):
    """ Initialization """
    def __init__(self, pos_x, pos_y, radius):
        super().__init__()
        # Initial Ball Settings
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius

        # Boundaries
        self.floor = WIN_HEI - BOUNDARY_SIZE
        self.cieling = BOUNDARY_SIZE
        self.wall_r = WIN_WID - BOUNDARY_SIZE
        self.wall_l = BOUNDARY_SIZE

    """ Setup """
    def setup(self):
        # Ball Vectors
        self.ball_vx = 0
        self.ball_vy = 0

        self.dest_x = None
        self.dest_y = None

        # Ball Attr
        self.pos = [self.pos_x, self.pos_y]
        self.ball = None

    """ Wall Collision """
    def wall_collide(self):

        # Floor collision
        if self.ball.bottom > self.floor:
            self.pos_y = self.floor - self.radius
            self.ball_vy *= -1

        # Cieling collision
        if self.ball.top < self.cieling:
            self.pos_y = self.cieling + self.radius
            self.ball_vy *= -1

        # Right wall collision
        if self.ball.right > self.wall_r:
            self.pos_x = self.wall_r - self.radius
            self.ball_vx *= -1
        
        # Left wall collision
        if self.ball.left < self.wall_l:
            self.pos_x = self.wall_l + self.radius
            self.ball_vx *= -1

    """ Destination Selection """
    def choose_dest(self):
        # Integer values for x and y positions
        x = math.floor(self.pos_x)
        y = math.floor(self.pos_y)

        # Makes sure the selected destination is within the borders
        check = False
        while not check:
            # Sets destination
            self.dest_x = random.randint(x - 100, x + 100)
            self.dest_y = random.randint(y - 100, y + 100)
            # Checks for validity
            if (self.wall_r - self.radius > self.dest_x > self.wall_l + self.radius and
                self.floor - self.radius > self.dest_y > self.cieling + self.radius) and (
                    self.dest_x != self.pos_x and self.dest_y != self.pos_y):
                check = True

    """ Destination Movement """
    def move_to_dest(self):
        # If theres no destination, make one
        if not self.dest_x or not self.dest_y:
            self.choose_dest()
        # Get the distance in the X and Y coordinates
        dist_x = self.pos_x - self.dest_x
        dist_y = self.pos_y - self.dest_y

        # Get the direct distance
        self.dist = math.hypot(dist_x, dist_y)

        # Set the vectors
        self.ball_vx = -(dist_x / self.dist) * SPD_MULT
        self.ball_vy = -(dist_y / self.dist) * SPD_MULT

        # If close enough to the destination, choose a new one
        if -1 < self.dist < 1:
            self.choose_dest()

    """ Update """
    def update(self):
        # Makes sure there is a ball to update
        if not self.ball:
            return

        # Checks for wall collision
        self.wall_collide()
        # Moves to Destination
        self.move_to_dest()

        # Updates the position with the vectors
        self.pos_x += self.ball_vx
        self.pos_y += self.ball_vy

        # Encapsulate the position to draw
        self.pos = self.pos_x, self.pos_y

    """ Draw """
    def draw(self, surface):
        # Draw the ball
        self.ball = pygame.draw.circle(window, WHITE, self.pos, self.radius)
        # Draw the balls destination
        if self.dest_x and self.dest_y and testing:
            self.dest_ball = pygame.draw.circle(window, RED, (self.dest_x, self.dest_y), 5)

# List of balls
ball_list = []

""" Reset """
def reset(ball_list):
    # Clears the list of balls
    ball_list.clear()
    # Iterates for every ball there will be
    for ball in range (BALL_COUNT):
        # Sets the position
        xpos = random.randint(int(2 * BOUNDARY_SIZE), int(WIN_WID - (2 * BOUNDARY_SIZE)))
        ypos = random.randint(int(2 * BOUNDARY_SIZE), int(WIN_HEI - (2 * BOUNDARY_SIZE)))
        # Applies attributes to a ball object and adds it to the list
        ball = Ball(xpos, ypos, RADIUS)
        ball_list.append(ball)

    # calls setup for every ball
    for ball in ball_list:
        ball.setup()

    return(ball_list)

# Initial setup to kick off program
reset(ball_list)

# Program loop
while True:
    key = pygame.key.get_just_pressed()
    for event in pygame.event.get():
        # Checks for the program closing
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Binds ESCAPE to close the program
    if key[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Binds R to reset the program
    if key[K_r]:
        reset(ball_list)

    # Binds T to toggle testing
    if key[K_t]:
        testing = not(testing)

    # Mouse Events
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Checks for left mouse button
        if event.button == 1:
            pos_x, pos_y = pygame.mouse.get_pos()
            ball = Ball(pos_x, pos_y, RADIUS)
            ball.setup()
            # Removes the first ball created if the next one goes over the limit
            if BALL_LIM == len(ball_list):
                ball_list.pop(0)
            # Adds ball to the list
            ball_list.append(ball)

        # Checks for right mouse button
        if event.button == 3:
            dest_x, dest_y = pygame.mouse.get_pos()
            # Sets every balls destination to the new override
            for ball in ball_list:
                ball.dest_x = dest_x
                ball.dest_y = dest_y

    # Clears the screen
    window.fill(BLACK)
    # Updates and draws the balls
    for ball in ball_list:
        ball.update()
        ball.draw(window)

    # Updates the display and FPS
    pygame.display.update()
    FRAMES_PER_SEC.tick(FPS)
