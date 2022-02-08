
class Config:
    WIN_WIDTH = 800
    WIN_HEIGHT = 600
    menuWidth = 200
    block = 25
    
    humanPlay = False
    POP_SIZE = 1000
    mutationRate = 0.1
    brain_layers = [24, 18, 18, 4]
    save_load_filename = 'saved/popObject'
    sX = (WIN_WIDTH-menuWidth)//block
    sY = WIN_HEIGHT//block
    FPS = 0
    
    def __init__(self):
        if self.humanPlay:
            self.FPS = 10
        else:
            self.FPS = 60
        if self.WIN_WIDTH <= self.menuWidth:
            raise Exception("Invalid window dimensions")
    



