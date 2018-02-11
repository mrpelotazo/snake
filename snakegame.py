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
SPEED = 8
SPEED_TICK = 2
SPEED_INC = 5
SHORT = 12
LONG = 1

# defining the outer wall blocks
wallblock = pygame.Surface((
    BLOCK_SIZE,
    BLOCK_SIZE,
))
wallblock.set_alpha(255)
wallblock.fill(BLUE)
wallblockdark = pygame.Surface((
    BLOCK_SIZE_INNER,
    BLOCK_SIZE_INNER,
))
wallblockdark.set_alpha(255)
wallblockdark.fill(BLUE_DARK)

# ============================================================================
#                             Function Definitions
# ============================================================================


# check if the snake's head is outside the limits
def in_limits(snake):
    headpos = snake.get_head_pos()
    is_outside = (
        headpos[0] < 1 or
        headpos[1] < 1 or
        headpos[0] >= HEIGHT + 1 or
        headpos[1] >= WIDTH + 1)
    return not is_outside


def draw_walls(surface):
    # left and right walls
    for y in range(HEIGHT + 1):
        surface.blit(wallblock, (
            0,
            y * BLOCK_SIZE,
        ))
        surface.blit(wallblockdark, (
            5,
            y * BLOCK_SIZE + 5,
        ))
        surface.blit(wallblock, (
            (WIDTH + 1) * BLOCK_SIZE,
            y * BLOCK_SIZE,
        ))
        surface.blit(wallblockdark, (
            (WIDTH + 1) * BLOCK_SIZE + 5,
            y * BLOCK_SIZE + 5,
        ))

    # upper and bottom walls
    for x in range(WIDTH + 2):
        surface.blit(wallblock, (
            x * BLOCK_SIZE,
            0,
        ))
        surface.blit(wallblockdark, (
            x * BLOCK_SIZE + 5,
            5,
        ))
        surface.blit(wallblock, (
            x * BLOCK_SIZE,
            (HEIGHT + 1) * BLOCK_SIZE,
        ))
        surface.blit(wallblockdark, (
            x * BLOCK_SIZE + 5,
            (HEIGHT + 1) * BLOCK_SIZE + 5,
        ))


# ============================================================================
#                               Main Game Part
# ============================================================================

# initialize pygame, clock for game speed and screen to draw
pygame.init()

# initializing mixer, sounds, clock and screen
pygame.mixer.init()
eatsound = pygame.mixer.Sound("snakeeat.wav")
crashsound = pygame.mixer.Sound("snakecrash.wav")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((
    (WIDTH + 2) * BLOCK_SIZE,
    (HEIGHT + 2) * BLOCK_SIZE,
))
pygame.display.set_caption("snake")
font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
gameovertext = font.render("GAME OVER", 1, WHITE)
starttext = font.render("PRESS ANY KEY TO START", 1, WHITE)
screen.fill(BLACK)

# we need a snake and something to eat
snake = Snake(screen, int(WIDTH / 2), int(HEIGHT / 2))
food = Food(screen, 1, HEIGHT+1, 1, WIDTH+1)

# food should not appear where the snake is
while food.get_pos() in snake.pos_list:
    food.__init__(screen, 1, HEIGHT + 1, 1, WIDTH + 1)

# only queue quit and and keydown events
# pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
pygame.event.set_blocked([
    pygame.MOUSEMOTION,
    pygame.MOUSEBUTTONUP,
    pygame.MOUSEBUTTONDOWN,
])

# will increase game speed every 10 times we eat
eaten = 0

# press any key to start!!!
draw_walls(screen)
screen.blit(starttext, (
    (WIDTH - 10) * BLOCK_SIZE / 2,
    HEIGHT * BLOCK_SIZE / 2,
))
pygame.display.flip()
waiting = True
while waiting:
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        waiting = False
screen.fill(BLACK)

# main loop
running = True
while running:

    # check crash or move outside the limits
    if not in_limits(snake) or snake.crashed:
        running = False
        crashsound.play()
    else:

        # draw screen with snake and foods
        food.draw()
        snake.draw()
        draw_walls(screen)
        pygame.display.flip()

        # check if snake eates
        if food.get_pos() == snake.get_head_pos():
            eatsound.play()
            snake.grow()
            # food should not appear where the snake is
            food.__init__(screen, 1, HEIGHT + 1, 1, WIDTH + 1)
            while food.get_pos() in snake.pos_list:
                food.__init__(screen, 1, HEIGHT + 1, 1, WIDTH + 1)
            eaten += 1
            # increase game speed
            if eaten % SPEED_INC == 0:
                SPEED += SPEED_TICK

        # game speed control
        clock.tick(SPEED)

        # get the next event on queue
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            actmotdir = snake.motion_dir
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_UP and actmotdir != DOWN:
                snake.motion_dir = UP
            elif event.key == pygame.K_DOWN and actmotdir != UP:
                snake.motion_dir = DOWN
            elif event.key == pygame.K_RIGHT and actmotdir != LEFT:
                snake.motion_dir = RIGHT
            elif event.key == pygame.K_LEFT and actmotdir != RIGHT:
                snake.motion_dir = LEFT

        # remove the snake and make movement
        snake.remove()
        snake.move()

# if crashed print "game over" and wait for esc key
clock.tick(LONG)
snake.draw()
draw_walls(screen)

for pos in snake.pos_list[1:]:
    screen.blit(snake.backblock, (
        pos[1] * BLOCK_SIZE,
        pos[0] * BLOCK_SIZE,
    ))
    pygame.display.flip()
    clock.tick(SHORT)

while True:
    screen.blit(gameovertext, (
        (WIDTH - 4) * BLOCK_SIZE / 2,
        HEIGHT * BLOCK_SIZE / 2,
    ))
    pygame.display.flip()
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            sys.exit()
