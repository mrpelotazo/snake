"""
Name        : snake.py
Description : The snake class definition for the snake game.
Author      : Adrian Antonana
Date        : 29.07.2012
"""

# imports
import pygame
from colors import BLACK, GREEN, GREEN_DARK

# motion direction constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# block sizes and colors
BLOCK_SIZE = 30
BLOCK_SIZE_INNER = 20


# pylint: disable=too-many-instance-attributes
class Snake:
    """Snake class definition"""

    def __init__(self, surface, headposx=10, headposy=10):
        """Constructor"""
        self.surface = surface
        self.length = 10
        self.pos_list = [(headposx, y) for y in reversed(
            range(
                headposy - self.length + 1,
                headposy + 1)
            )]
        self.motion_dir = RIGHT
        self.crashed = False

        # for drawing the snake
        self.snakeblock = pygame.Surface((
            BLOCK_SIZE,
            BLOCK_SIZE,
        ))
        self.snakeblock.set_alpha(255)
        self.snakeblock.fill(GREEN)
        self.snakeblockdark = pygame.Surface((
            BLOCK_SIZE_INNER,
            BLOCK_SIZE_INNER,
        ))
        self.snakeblockdark.set_alpha(255)
        self.snakeblockdark.fill(GREEN_DARK)

        # for removing the snake
        self.backblock = pygame.Surface((
            BLOCK_SIZE,
            BLOCK_SIZE,
        ))
        self.backblock.set_alpha(255)
        self.backblock.fill(BLACK)

    def get_head_pos(self):
        """Get snake's head position"""
        return self.pos_list[0]

    def outside_limits(self, width, height):
        """Check if the snake's head is outside the limits"""
        headpos = self.get_head_pos()
        is_outside = (
            headpos[0] < 1 or
            headpos[1] < 1 or
            headpos[0] >= height + 1 or
            headpos[1] >= width + 1)
        return is_outside

    def move(self):
        """Update the positions list and check if the snake has crashed"""
        motdir = self.motion_dir
        headpos = self.get_head_pos()

        # update positions
        if motdir == UP:
            poslist = [(headpos[0] - 1, headpos[1])]
        elif motdir == DOWN:
            poslist = [(headpos[0] + 1, headpos[1])]
        elif motdir == LEFT:
            poslist = [(headpos[0], headpos[1] - 1)]
        elif motdir == RIGHT:
            poslist = [(headpos[0], headpos[1] + 1)]

        poslist.extend(self.pos_list[:-1])
        self.pos_list = poslist

        # check if crashed
        if self.get_head_pos() in self.pos_list[1:]:
            self.crashed = True

    def grow(self):
        """Grow the snake. add a new position at the end"""
        lastpos = self.pos_list[-1]
        self.length += 1
        self.pos_list.append((lastpos[0] - 1, lastpos[1]))

    def draw(self):
        """Draw the snake"""
        for blockpos in self.pos_list:
            self.surface.blit(self.snakeblock, (
                blockpos[1] * BLOCK_SIZE,
                blockpos[0] * BLOCK_SIZE,
            ))
            self.surface.blit(self.snakeblockdark, (
                blockpos[1] * BLOCK_SIZE + 5,
                blockpos[0] * BLOCK_SIZE + 5,
            ))

    def remove(self):
        """Delete the snake"""
        for blockpos in self.pos_list:
            # draw block for every snake position
            self.surface.blit(self.backblock, (
                blockpos[1] * BLOCK_SIZE,
                blockpos[0] * BLOCK_SIZE,
            ))
