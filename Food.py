
import pygame
import random

class Food:
    def __init__(self):
        self.x = 0
        self.y = 0

    def createFood(self, sX, sY):
        self.x = random.randint(0, sX-1)
        self.y = random.randint(0, sY-1)

    def draw(self, win, menuWidth, block):
        pygame.draw.rect(win, (255, 10, 10), (menuWidth+self.x*block, self.y*block, block, block), 0)

