"""
Name        : food.py
Description : Food class definition for the snake game
Author      : Adrian Antonana
Date        : 29.07.2012
"""

# imports
import random
import pygame
from colors import RED, RED_DARK

# block sizes
BLOCK_SIZE = 30
BLOCK_SIZE_INNER = 20


class Food:
    """Food class definition"""

    # pylint: disable=too-many-arguments
    def __init__(self, surface, minx, maxx, miny, maxy):
        """Class constructor"""
        self.surface = surface
        self.posx = random.randint(minx, maxx - 1)
        self.posy = random.randint(miny, maxy - 1)

        # for drawing the food
        self.foodblock = pygame.Surface((
            BLOCK_SIZE,
            BLOCK_SIZE,
        ))
        self.foodblock.set_alpha(255)
        self.foodblock.fill(RED)
        self.foodblockdark = pygame.Surface((
            BLOCK_SIZE_INNER,
            BLOCK_SIZE_INNER,
        ))
        self.foodblockdark.set_alpha(255)
        self.foodblockdark.fill(RED_DARK)

    def get_pos(self):
        """Get food position"""
        return self.posx, self.posy

    def draw(self):
        """Draw the food"""
        # food is just two blocks
        self.surface.blit(self.foodblock, (
            self.posy * BLOCK_SIZE,
            self.posx * BLOCK_SIZE,
        ))
        self.surface.blit(self.foodblockdark, (
            self.posy * BLOCK_SIZE + 5,
            self.posx * BLOCK_SIZE + 5,
        ))
