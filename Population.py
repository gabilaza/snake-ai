
import os
import copy
import random
from Snake import Snake

class Population:
    def __init__(self, size, config):
        self.gen = 1
        self.config = config
        self.size = size
        self.bestScore = 1
        self.snakes = [Snake(self.config) for _ in range(size)]
        self.best_snakes = None
        self.idx = 0
    
    def ordBestFit(self):
        for snake in self.snakes:
            snake.fitness = snake.steps+(2**snake.score+(snake.score**(2.1))*500)-((snake.score**(1.2))*((0.25*snake.steps)**(1.3)))
        #for snake in self.snakes:
        #    snake.fitness = 0.65*snake.score+0.35*((snake.fitness)/10)
        self.snakes.sort(key=lambda snake:snake.fitness, reverse=True)

    def update(self, sX, sY):
        for snake in self.snakes:
            snake.look(sX, sY)
            snake.think_move()
            if snake.lifeleft == 0:
                snake.dead = True
            if snake.bodyCollide():
                snake.dead = True
            if snake.wallCollide(sX, sY):
                snake.dead = True
            if snake.foodCollide():
                snake.eatFood()
                snake.food.createFood(sX, sY)
                while((snake.food.x, snake.food.y) in snake.body):
                    snake.food.createFood(sX, sY)
    
    def done(self):
        for snake in self.snakes:
            if not snake.dead:
                return False
        self.idx = 0
        self.gen += 1
        for snake in self.snakes:
            if self.bestScore < snake.score:
                self.bestScore = snake.score

        return True
    
    def naturalSelection(self, mutationRate):
        
        if self.best_snakes is not None:
            self.snakes.extend(self.best_snakes)
        self.ordBestFit()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Gen:", self.gen-1)
        print("Snakes:")
        for snake in self.snakes[:4]:
            print("Score:", snake.score, "   Fitness:", snake.fitness, "   Lifetime:", snake.lifetime)
        if self.best_snakes is not None:
            print("Best Snakes:")
            for snake in self.best_snakes[:4]:
                print("Score:", snake.score, "   Fitness:", snake.fitness, "   Lifetime:", snake.lifetime)

        self.best_snakes = []
        s = int((5*self.size)/100)

        for i in range(s):
            self.best_snakes.append(Snake(self.config))
            self.best_snakes[-1].brain = copy.deepcopy(self.snakes[i].brain)
            self.best_snakes[-1].fitness = self.snakes[i].fitness
            self.best_snakes[-1].score = self.snakes[i].score
        
        for i in range(s):
            self.best_snakes.append(Snake(self.config))
            self.best_snakes[-1].brain = random.choice(self.best_snakes[:s]).brain.crossover(random.choice(self.best_snakes[:s]).brain)
        
        self.snakes = []
        for _ in range(self.size//(s*2)):
            for b_snake in self.best_snakes:
                self.snakes.append(Snake(self.config))
                self.snakes[-1].brain = copy.deepcopy(b_snake.brain)

                self.snakes[-1].brain.mutate(mutationRate)

    def createFoods(self, sX, sY):
        for snake in self.snakes:
            snake.food.createFood(sX, sY)

    def draw(self, win, menuWidth, block, All=False):
        if All:
            for snake in self.snakes:
                snake.draw(win, menuWidth, block)
                snake.food.draw(win, menuWidth, block)
        else:
            while self.snakes[self.idx].dead and self.idx < self.size-1:
                self.idx += 1
            self.snakes[self.idx].draw(win, menuWidth, block)
            self.snakes[self.idx].food.draw(win, menuWidth, block)
    
