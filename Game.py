
import os
import pygame
import pickle
from Snake import Snake
from Button import Button
from Population import Population
pygame.font.init()

class Game:
    def __init__(self, config):
        self.config = config
        self.WIN_WIDTH = self.config.WIN_WIDTH
        self.WIN_HEIGHT = self.config.WIN_HEIGHT
        self.menuWidth = self.config.menuWidth
        self.block = self.config.block
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.buttons = [(-1, Button((100, 100, 100), ((self.menuWidth-2*80-5)//2, 10, 80, 30), 'Restart')),
                        (-1, Button((100, 100, 100), ((self.menuWidth-2*80-5)//2+85, 10, 80, 30), 'Quit')),
                        (0, Button((100, 100, 100), ((self.menuWidth-2*80-5)//2, 45, 80, 30), 'Save')),
                        (0, Button((100, 100, 100), ((self.menuWidth-2*80-5)//2+85, 45, 80, 30), 'Load'))]
        pygame.display.set_caption('SnakeAI')
        self.humanPlay = self.config.humanPlay
        self.RUN = True
        self.sX = self.config.sX
        self.sY = self.config.sY
        self.FPS = self.config.FPS
        self.pause = False
        
        if self.humanPlay:
            self.snake = Snake(self.config)
            self.snake.food.createFood(self.sX, self.sY)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.All = False
            self.mutationRate = self.config.mutationRate
            self.pop = Population(self.config.POP_SIZE, self.config)
            self.pop.createFoods(self.sX, self.sY)

    def update(self, events):
        if self.humanPlay:
            if not self.snake.dead:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            self.snake.move('U')
                            break
                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.snake.move('R')
                            break
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            self.snake.move('D')
                            break
                        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.snake.move('L')
                            break
                self.snake.move()
            
                if self.snake.bodyCollide():
                    self.snake.dead = True
                if self.snake.wallCollide(self.sX, self.sY):
                    self.snake.dead = True
                if self.snake.foodCollide():
                    self.snake.eatFood()
                    self.snake.food.createFood(self.sX, self.sY)
                    while((self.snake.food.x, self.snake.food.y) in self.snake.body):
                        self.snake.food.createFood(self.sX, self.sY)
                
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if self.All:
                            self.All = False
                        else:
                            self.All = True
                    if event.key == pygame.K_s:
                        self.save()
                    if event.key == pygame.K_l:
                        self.load()

            if self.pop.done():
                self.pop.naturalSelection(self.mutationRate)
                self.pop.createFoods(self.sX, self.sY)
            else:
                self.pop.update(self.sX, self.sY)

    def draw_window(self):
        self.win.fill((0, 0, 0))
        
        if self.humanPlay:
            self.snake.draw(self.win, self.menuWidth, self.block)
            self.snake.food.draw(self.win, self.menuWidth, self.block)
        else:
            self.pop.draw(self.win, self.menuWidth, self.block, self.All)

        for i in range(1, (self.WIN_WIDTH-self.menuWidth)//self.block):
            pygame.draw.line(self.win, (65, 65, 65), (self.menuWidth+i*self.block, 0), (self.menuWidth+i*self.block, self.WIN_HEIGHT), 1)
        for i in range(1, self.WIN_HEIGHT//self.block):
            pygame.draw.line(self.win, (65, 65, 65), (self.menuWidth, i*self.block), (self.WIN_WIDTH, i*self.block), 1)
        pygame.draw.rect(self.win, (150, 100, 100), (0, 0, self.menuWidth-2, self.WIN_HEIGHT), 2)
        pygame.draw.rect(self.win, (150, 150, 150), (200, 0, self.WIN_WIDTH-self.menuWidth, self.WIN_HEIGHT), 3)
        
        if self.humanPlay:
            if self.snake.dead:
                font = pygame.font.SysFont('ubuntumono', 50)
                txt = font.render("Dead", True, (10, 255, 10))
                self.win.blit(txt, (self.menuWidth+(self.WIN_WIDTH-self.menuWidth-txt.get_width())//2, (self.WIN_HEIGHT-txt.get_height())//2))
            font = pygame.font.SysFont('ubuntumono', 28)
            txt = font.render("Score: " + str(self.snake.score), True, (200, 200, 200))
            self.win.blit(txt, (5, 45))
        else:
            font = pygame.font.SysFont('ubuntumono', 28)
            txt = font.render("Gen: " + str(self.pop.gen), True, (200, 200, 200))
            self.win.blit(txt, (5, 75))
            txt = font.render("Score: " + str(self.pop.snakes[self.pop.idx].score), True, (200, 200, 200))
            self.win.blit(txt, (5, 100))
            txt = font.render("BScore: " + str(self.pop.bestScore), True, (200, 200, 200))
            self.win.blit(txt, (5, 125))

        for button in self.buttons:
            if self.humanPlay == button[0] or button[0] == -1:
                button[1].draw(self.win)

        pygame.display.update()

    def run(self):
        pos_aux = None
        while self.RUN:
            self.clock.tick(self.FPS)
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.RUN = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.RUN = False
                    if event.key == pygame.K_r:
                        self.__init__(self.config)
                    if event.key == pygame.K_SPACE:
                        self.pause = bool(1-int(self.pause))
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    for i, button in enumerate(self.buttons):
                        if button[1].mouseButton():
                            pos_aux = i
                            break
                if event.type == pygame.MOUSEBUTTONUP and pos_aux != None:
                    for i, button in enumerate(self.buttons):
                        if button[1].mouseButton() and pos_aux == i:
                            if button[1].name == 'Restart':
                                self.__init__(self.config)
                            elif button[1].name == 'Quit':
                                self.RUN = False
                            if self.humanPlay == button[0]:
                                if button[1].name == 'Save':
                                    self.save()
                                elif button[1].name == 'Load':
                                    self.load()
                    pos_aux = None
            
            if not self.pause:
                self.update(events)

            self.draw_window()
    
    def save(self):
        with open(self.config.save_load_filename, 'wb') as f:
            pickle.dump(self.pop, f)
        print("Saved")

    def load(self):
        if os.path.isfile(self.config.save_load_filename):
            with open(self.config.save_load_filename, 'rb') as f:
                self.pop = pickle.load(f)
            print("Loaded")
        else:
            print("File not found")








