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

        self.__screenSize  = (640, 480)
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

    def __createColor(self, startY):
        if startY == 35:
            # red
            color = (255, 0, 0)
        elif startY == 55:
            # orange
            color = (255, 140, 0)
        elif startY == 75:
            # yellow
            color = (255, 255, 0)
        elif startY == 95:
            # green
            color = (50, 205, 50)
        elif startY == 115:
            # light blue
            color = (0, 191, 255)
        elif startY == 135:
            # dark blue
            color = (0, 0, 205)
        else:
            # purple
            color = (148, 0, 211)
        return color

    def __createBricks(self):
        startY = 35
        for rows in range(7):
            startX = 29
            for columns in range(8):

                rowColor = self.__createColor(startY)
                self.__brick = pygame.Rect(startX, startY, 60, 15)
                self.__brick = pygame.draw.rect(self.__screen, rowColor,
                                                self.__brick)
                self.__bricks.append(self.__brick)

                startX += 75
            startY += 20

    def __findInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.__state == 0:
                self.__block.left -= 10
                if self.__block.left < 0:
                    self.__block.left = 0

                self.__ball.left -= 10
                if self.__ball.left < 23:
                    self.__ball.left = 23

            if self.__state > 0:
                self.__block.left -= 10
                if self.__block.left < 0:
                    self.__block.left = 0

        if keys[pygame.K_RIGHT]:
            if self.__state == 0:
                self.__block.left += 10
                if self.__block.right > 640:
                    self.__block.right = 640

                self.__ball.left += 10
                if self.__ball.right > 617:
                    self.__ball.right = 617

            if self.__state > 0:
                self.__block.left += 10
                if self.__block.right > 640:
                    self.__block.right = 640

        if keys[pygame.K_SPACE] and self.__state == 0:
            self.__ballVelocity = [5, -5]
            self.__state = 1
            if self.__lives < 3:
                try:
                    pygame.mixer.music.play(-1)
                except pygame.error as err:
                    print(err)

        if keys[pygame.K_q]:
            if self.__state != 2:
                self.__state = 3
            try:
                pygame.mixer.music.stop()
                gameOver = pygame.mixer.Sound(os.path.join('audio', 'GameOver.ogg'))
                gameOver.set_volume(.5)
                gameOver.play(0)
            except pygame.error as err:
                print(err)
            self.__gameOver = True

    def __moveBall(self):
        # To change the ball speed multiply the velocity by a number
        self.__ball.left += (1.2 * self.__ballVelocity[0])
        self.__ball.top += (1.2 * self.__ballVelocity[1])

        # stops the left side of ball from going further than screen on left
        if self.__ball.left <= 0:
            self.__ball.left = 0
            self.__ballVelocity[0] = -self.__ballVelocity[0]
        # stops right side of ball from going further than screen on right
        elif self.__ball.right >= 640:
            self.__ball.right = 640
            self.__ballVelocity[0] = -self.__ballVelocity[0]

        # stops the top of ball from going further than top of screen
        if self.__ball.top < 0:
            self.__ball.top = 0
            self.__ballVelocity[1] = -self.__ballVelocity[1]
        # stops the bottom of ball from going below bottom of screen
        elif self.__ball.bottom > 480:
            self.__ball.bottom = 480
            self.__ballVelocity[1] = -self.__ballVelocity[1]

    def __collision(self):
        for self.__brick in self.__bricks:
            if self.__ball.colliderect(self.__brick):
                self.__score += 1
                self.__ballVelocity[1] = -self.__ballVelocity[1]
                self.__bricks.remove(self.__brick)
                self.__brick = pygame.draw.rect(self.__screen, (0, 0, 0),
                                                self.__brick)
                try:
                    brickSmash = pygame.mixer.Sound(os.path.join('audio', 'smb_breakblock.wav'))
                    brickSmash.set_volume(.5)
                    brickSmash.play(0)
                except pygame.error as err:
                    print(err)
                break

        if len(self.__bricks) == 0:
            # state 2 = game won
            self.__state = 2
            try:
                pygame.mixer.music.stop()
                # gameWon = pygame.mixer.Sound(os.path.join('Sounds', 'World Clear.ogg'))
                # gameWon.play(0)
            except pygame.error as err:
                print(err)
            self.__gameOver = True

        if self.__ball.colliderect(self.__block):
            self.__ball.top = (445 - 14)
            self.__ballVelocity[1] = -self.__ballVelocity[1]

        elif self.__ball.bottom == 480:
            self.__lives -= 1
            if self.__lives > 0:
                try:
                    pygame.mixer.music.stop()
                except pygame.error as err:
                    print(err)
                self.__state = 0
                self.__blockX = 300
                self.__block = pygame.Rect((self.__blockX, 445, 60, 10))
                self.__ballX = self.__blockX + 20
                self.__ball = pygame.Rect(self.__ballX, 430, 7, 7)
            else:
                # state 3 = game over
                self.__state = 3
                try:
                    pygame.mixer.music.stop()
                    gameOver = pygame.mixer.Sound(os.path.join('audio', 'GameOver.ogg'))
                    gameOver.set_volume(.5)
                    gameOver.play(0)
                except pygame.error as err:
                    print(err)
                self.__gameOver = True

    def __displayScoreLives(self):
        pygame.draw.rect(self.__screen, (0, 0, 0), (0, 0, 640, 25))
        fontSurface = self.__font.render("SCORE: " + str(self.__score) +
                                         "    LIVES: " + str(self.__lives), True,
                                         (255, 255, 255))
        self.__screen.blit(fontSurface, (205, 5))

    def __message(self):
        pygame.draw.rect(self.__screen, (0, 0, 0), (40, 270, 640, 100))
        if self.__state == 0:
            directionsMsg = "Clear all the bricks by bouncing" + \
                            " the ball on the block"
            directionsMsgSurface = self.__font.render(directionsMsg, True,
                                                      (255, 255, 255))
            self.__screen.blit(directionsMsgSurface, (50, 270))

            message = "Press SPACE to launch the ball or Q to quit"

            arrowKeyMsg = "Use ARROW KEYS to move the block"
            arrowKeyMsgSurface = self.__font.render(arrowKeyMsg, True,
                                                    (255, 255, 255))
            self.__screen.blit(arrowKeyMsgSurface, (120, 330))

        elif self.__state == 2:
            if self.__mode == "Story":
                message = "You won! Press Q to continue story mode"
            else:
                message = "You won! Press ENTER to play again or Q to quit"
        else:
            message = "Game over. Press ENTER to play again or Q to quit"

        fontSurface = self.__font.render(message, True, (255, 255, 255))
        self.__screen.blit(fontSurface, (100, 300))

    def runBreakout(self):
        while not self.__completed:
            while self.__gameOver:
                self.__displayScoreLives()
                if self.__state != 1:
                    self.__message()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__gameOver = False
                        self.__completed = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.__gameOver = False
                            self.__completed = True
                        if event.key == pygame.K_RETURN and \
                                self.__state == 3:
                            self.__init__()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__state = 3
                    try:
                        pygame.mixer.music.stop()
                        gameOver = pygame.mixer.Sound(os.path.join('audio', 'GameOver.ogg'))
                        gameOver.set_volume(.5)
                        gameOver.play(0)
                    except pygame.error as err:
                        print(err)
                    self.__gameOver = True

            self.__clock.tick(50)
            self.__findInput()

            if self.__state == 1:
                pygame.draw.rect(self.__screen, (0, 0, 0), (40, 270, 640, 100))
                self.__moveBall()
                self.__collision()
            else:
                self.__message()

            self.__displayScoreLives()

            self.__block = pygame.draw.rect(self.__screen, (255, 255, 225),
                                            self.__block)
            self.__ball = pygame.draw.circle(self.__screen, (255, 105, 180),
                                             (self.__ball.left + 7,
                                              self.__ball.top + 7), 7)

            pygame.display.flip()

            self.__block = pygame.draw.rect(self.__screen, (0, 0, 0),
                                            self.__block)
            self.__ball = pygame.draw.circle(self.__screen, (0, 0, 0),
                                             (self.__ball.left + 7,
                                              self.__ball.top + 7), 7)
        pygame.mixer.stop()


if __name__ == '__main__':
    game = Breakout()
    game.runBreakout()