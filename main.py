import os
from os.path import abspath, dirname
import pygame


class Breakout:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.music.load(os.path.join('audio', 'game_theme'))
            pygame.mixer.music.set_volume(2)
            pygame.mixer.music.play(-1)
        except pygame.error as err:
            print(err)

        self.__screenSize  = (640, 500)
        self.__screen = pygame.display.set_mode(self.__screenSize)
        pygame.display.set_caption("Breakout, Atari Inc.")

        self.__clock = pygame.time.Clock()
        self.__score = 0
        self.__lives = 3
        self.__state = 0

        self.__blockX = 300
        self.__block = pygame.Rect((self.__blockX, 445, 60, 10))
        self.__ballX = self.__blockX + 23
        self.__ball = pygame.Rect((self.__ballX, 430, 7, 7))
        self.__ballVelocity = [5,-5]
        self.__bricks = []
        self.__brick = None

        self.__completed = False
        self.__gameOver = False

        FONT = abspath(dirname(__file__)) + '/font/' + 'pixelar.ttf'
        self.__font = pygame.font.SysFont(FONT, 20, bold=True, italic=False)

        self.__createBricks()

    def __createBricks(self):
        pass

    def runBreakout(self):
        print("Breakout")


if __name__ == '__main__':
    game = Breakout()
    game.runBreakout()