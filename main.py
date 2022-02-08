
from Game import Game
from config import Config

config = Config()
if __name__ == '__main__':
    game = Game(config)
    game.run()

