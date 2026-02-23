# Python project 2  :Pygame
# Author            :Maze Elva
# Date              :1.16.2026
# Purpose           :Playing with Pygame to learn
#                    and make something

from http.client import PRECONDITION_REQUIRED
import pygame, sys
from pygame.locals import *
import pygame.rect

pygame.init()

# Window Settings
WIN_WID = int(1200)
WIN_HEI = int(840)

# FPS
FPS = 60
frames_per_sec = pygame.time.Clock()

# Colours
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)

# Window Creation
WINDOW = pygame.display.set_mode((WIN_WID, WIN_HEI))
WINDOW.fill(WHITE)
pygame.display.set_caption("Test")

class Box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Mauricio.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (WIN_WID // 2, WIN_HEI // 2)
        
        self.box_vx= 50
        self.box_vy= -5

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        
        self.rect.move_ip(self.box_vx, self.box_vy)
        if self.rect.left > WIN_WID:
            self.rect.right = 0
        
        if self.rect.bottom < 0:
            self.rect.top = WIN_HEI

        if pressed_keys[K_DOWN] and not (self.box_vx < 1 or self.box_vy > -1):
            self.box_vx *= .9
            self.box_vy *= .9
        elif pressed_keys[K_UP]:
            self.box_vx *= 1.1
            self.box_vy *= 1.1

    def draw(self, surface):
        surface.blit(self.image, self.rect) 

box1 = Box()

# Run loop
while True:
    for event in pygame.event.get():
# Exit Check
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

# Update Mauricio
    box1.update()

# Window Refresh
    WINDOW.fill(BLACK)
    box1.draw(WINDOW)
    
# Updates And Tickrate
    pygame.display.update()
    frames_per_sec.tick(FPS)