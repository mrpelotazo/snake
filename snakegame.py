"""
Name        : snakegame.py
Description : Python version of the snake game.
Author      : Adrian Antonana
Date        : 29.07.2012
"""

# imports
import sys
import pygame
from snake import Snake, BLOCK_SIZE, BLOCK_SIZE_INNER, UP, DOWN, LEFT, RIGHT
from food import Food
from colors import BLACK, BLUE, BLUE_DARK, WHITE

# screen size and game speed
WIDTH = 25
HEIGHT = 25
START_SPEED = 8
SPEED_TICK = 2
SPEED_INC = 5
SHORT = 12
LONG = 1


# pylint: disable=too-many-instance-attributes
class Game:
    """The main class that makes up the game"""

    def __init__(self):
        """Constructor"""
        self.speed = START_SPEED

        # will increase game speed every 10 times we eat
        self.eaten = 0

        # defining the outer wall blocks
        self.wallblock = pygame.Surface((
            BLOCK_SIZE,
            BLOCK_SIZE,
        ))
        self.wallblock.set_alpha(255)
        self.wallblock.fill(BLUE)

        self.wallblockdark = pygame.Surface((
            BLOCK_SIZE_INNER,
            BLOCK_SIZE_INNER,
        ))
        self.wallblockdark.set_alpha(255)
        self.wallblockdark.fill(BLUE_DARK)

        # initialize pygame, clock for game speed and screen to draw
        pygame.init()

        # initializing mixer, sounds, clock and screen
        pygame.mixer.init()
        self.eatsound = pygame.mixer.Sound("snakeeat.wav")
        self.crashsound = pygame.mixer.Sound("snakecrash.wav")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((
            (WIDTH + 2) * BLOCK_SIZE,
            (HEIGHT + 2) * BLOCK_SIZE,
        ))
        pygame.display.set_caption("snake")
        font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
        self.gameovertext = font.render("GAME OVER", 1, WHITE)
        self.starttext = font.render("PRESS ANY KEY TO START", 1, WHITE)
        self.screen.fill(BLACK)

        # we need a snake and something to eat
        self.snake = Snake(self.screen, int(WIDTH / 2), int(HEIGHT / 2))
        self.food = Food(self.screen, 1, HEIGHT + 1, 1, WIDTH + 1)

        # food should not appear where the snake is
        while self.food.get_pos() in self.snake.pos_list:
            self.food = Food(self.screen, 1, HEIGHT + 1, 1, WIDTH + 1)

        # only queue quit and and keydown events
        # pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        pygame.event.set_blocked([
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN,
        ])

    def draw_walls(self):
        """Draw all walls of the game surface"""
        # left and right walls
        for y in range(HEIGHT + 1):  # pylint: disable=invalid-name
            self.screen.blit(self.wallblock, (
                0,
                y * BLOCK_SIZE,
            ))
            self.screen.blit(self.wallblockdark, (
                5,
                y * BLOCK_SIZE + 5,
            ))
            self.screen.blit(self.wallblock, (
                (WIDTH + 1) * BLOCK_SIZE,
                y * BLOCK_SIZE,
            ))
            self.screen.blit(self.wallblockdark, (
                (WIDTH + 1) * BLOCK_SIZE + 5,
                y * BLOCK_SIZE + 5,
            ))

        # upper and bottom walls
        for x in range(WIDTH + 2):  # pylint: disable=invalid-name
            self.screen.blit(self.wallblock, (
                x * BLOCK_SIZE,
                0,
            ))
            self.screen.blit(self.wallblockdark, (
                x * BLOCK_SIZE + 5,
                5,
            ))
            self.screen.blit(self.wallblock, (
                x * BLOCK_SIZE,
                (HEIGHT + 1) * BLOCK_SIZE,
            ))
            self.screen.blit(self.wallblockdark, (
                x * BLOCK_SIZE + 5,
                (HEIGHT + 1) * BLOCK_SIZE + 5,
            ))

    def loop(self):
        """The game's main loop"""
        while True:
            # check crash or move outside the limits
            if self.snake.outside_limits(WIDTH, HEIGHT) or self.snake.crashed:
                self.crashsound.play()
                return

            # draw screen with snake and foods
            self.food.draw()
            self.snake.draw()
            self.draw_walls()
            pygame.display.flip()

            # check if snake eates
            if self.food.get_pos() == self.snake.get_head_pos():
                self.eatsound.play()
                self.snake.grow()
                # food should not appear where the snake is
                self.food = Food(self.screen, 1, HEIGHT + 1, 1, WIDTH + 1)
                while self.food.get_pos() in self.snake.pos_list:
                    self.food = Food(self.screen, 1, HEIGHT + 1, 1, WIDTH + 1)
                self.eaten += 1
                # increase game speed
                if self.eaten % SPEED_INC == 0:
                    self.speed += SPEED_TICK

            # game speed control
            self.clock.tick(self.speed)

            # get the next event on queue
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                actmotdir = self.snake.motion_dir
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_UP and actmotdir != DOWN:
                    self.snake.motion_dir = UP
                elif event.key == pygame.K_DOWN and actmotdir != UP:
                    self.snake.motion_dir = DOWN
                elif event.key == pygame.K_RIGHT and actmotdir != LEFT:
                    self.snake.motion_dir = RIGHT
                elif event.key == pygame.K_LEFT and actmotdir != RIGHT:
                    self.snake.motion_dir = LEFT

            # remove the snake and make movement
            self.snake.remove()
            self.snake.move()

    def game_over(self):
        """When crashed print "game over" and wait for Esc key"""
        self.clock.tick(LONG)
        self.snake.draw()
        self.draw_walls()

        for pos in self.snake.pos_list[1:]:
            self.screen.blit(self.snake.backblock, (
                pos[1] * BLOCK_SIZE,
                pos[0] * BLOCK_SIZE,
            ))
            pygame.display.flip()
            self.clock.tick(SHORT)

        while True:
            self.screen.blit(self.gameovertext, (
                (WIDTH - 4) * BLOCK_SIZE / 2,
                HEIGHT * BLOCK_SIZE / 2,
            ))
            pygame.display.flip()
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def start(self):
        """The game starts here"""
        # press any key to start!!!
        self.draw_walls()
        self.screen.blit(self.starttext, (
            (WIDTH - 10) * BLOCK_SIZE / 2,
            HEIGHT * BLOCK_SIZE / 2,
        ))
        pygame.display.flip()

        waiting = True
        while waiting:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                waiting = False
        self.screen.fill(BLACK)

        # main loop
        self.loop()
        self.game_over()


if __name__ == "__main__":
    Game().start()
