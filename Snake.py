
import math
import pygame
import numpy as np
from Brain import Brain
from Food import Food

class Snake:
    def __init__(self, config):
        self.config = config
        self.brain = Brain(self.config.brain_layers)
        self.food = Food()
        self.body = [(self.config.sX//2, self.config.sY//2)]
        self.vel = (1, 0)
        
        self.score = 1
        self.lifeleft = 100
        self.lifetime = 0
        self.fitness = 0
        self.vision = []
        self.last_dist = 12516126

        self.dead = False


        self.steps = 0
    
    def lookInDirection(self, vel, sX, sY): 
        look = [0, 0, 0]
        d = 1
        safe = self.body[0]

        pos_new = (self.body[0][0]+vel[0], self.body[0][1]+vel[1])
        self.body[0] = pos_new
        while not self.wallCollide(sX, sY):
            if self.bodyCollide():
                look[1] = 1/d
            if self.foodCollide():
                look[0] = 1/d

            pos_new = (self.body[0][0]+vel[0], self.body[0][1]+vel[1])
            self.body[0] = pos_new
            d += 1

        look[2] = 1/d
        self.body[0] = safe
        return look


    def look(self, sX, sY):
        
        self.vision = []
        self.vision += self.lookInDirection((0, -1), sX, sY)
        self.vision += self.lookInDirection((1, -1), sX, sY)
        self.vision += self.lookInDirection((1, 0), sX, sY)
        self.vision += self.lookInDirection((1, 1), sX, sY)
        self.vision += self.lookInDirection((0, 1), sX, sY)
        self.vision += self.lookInDirection((-1, 1), sX, sY)
        self.vision += self.lookInDirection((-1, 0), sX, sY)
        self.vision += self.lookInDirection((-1, -1), sX, sY)

        self.vision = np.array(self.vision).reshape((self.brain.layers[0], 1))

    def think_move(self):
        direction = self.brain.feedforward(self.vision)
        way = np.argmax(direction)
        if way == 0:
            self.move('U')
        elif way == 1:
            self.move('R')
        elif way == 2:
            self.move('D')
        elif way == 3:
            self.move('L')
        self.move()

    def bodyCollide(self):
        head = self.body[0]
        if self.body.count(head) > 1:
            return True
        return False

    def wallCollide(self, sX, sY):
        head = self.body[0]
        if head[0] < 0 or head[1] < 0 or head[0] >= sX or head[1] >= sY:
            return True
        return False

    def foodCollide(self):
        head = self.body[0]
        if head[0] == self.food.x and head[1] == self.food.y:
            return True
        return False

    def eatFood(self):
        self.score += 1
        if self.lifeleft < 300:
            if self.lifeleft > 200:
                self.lifeleft = 300
            else:
                self.lifeleft += 50

        tail = self.body[-1]
        self.body.append(tail)

    def move(self, d=None):
        if not self.dead:
            vel = None
            if d == 'U':
                vel = (0, -1)
            elif d == 'R':
                vel = (1, 0)
            elif d == 'D':
                vel = (0, 1)
            elif d == 'L':
                vel = (-1, 0)
            if d == None:
                pos_new = (self.body[0][0]+self.vel[0], self.body[0][1]+self.vel[1])
                self.body.insert(0, pos_new)
                self.body.pop()
                
                self.lifetime += 1
                self.lifeleft -= 1
                
                self.steps += 1

                current_dist = abs(self.body[0][0]-self.food.x)+abs(self.body[0][1]-self.food.y)
                if self.last_dist > current_dist:
                    self.fitness += 1
                else:
                    self.fitness -= 1.75
                self.last_dist = current_dist

            else:
                pos_new = (self.body[0][0]+vel[0], self.body[0][1]+vel[1])
                if (len(self.body) > 1 and pos_new != self.body[1]) or len(self.body) == 1:
                    self.vel = vel
                
    def draw(self, win, menuWidth, block):
        for p in self.body:
            if p[0] > -1 and p[1] > -1:
                pygame.draw.rect(win, (255, 255, 255), (menuWidth+p[0]*block, p[1]*block, block, block), 0)
        
