
import pygame

class Button:
    def __init__(self, color, pos, name=None):
        self.color = color
        self.x, self.y, self.x1, self.y1 = pos
        self.name = name
    
    def mouseButton(self):
        x, y = pygame.mouse.get_pos()
        if self.x < x < self.x+self.x1 and self.y < y < self.y+self.y1:
            return True
        return False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.x1, self.y1), 0)
        pygame.draw.rect(win, (200, 200, 200), (self.x, self.y, self.x1, self.y1), 1)
        font = pygame.font.SysFont('ubuntumono', 18)
        txt = font.render(self.name, True, (255, 184, 77))
        win.blit(txt, (self.x+(self.x1-txt.get_width())//2, self.y+(self.y1-txt.get_height())//2))

