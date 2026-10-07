"""
Obstacle: a scrolling wall pair with a gap the helicopter must fly
through.
"""

import pygame


class Obstacle:
    def __init__(self, x, gap_y, gap_height, wall_width, screen_height, speed):
        self.x = x
        self.gap_y = gap_y
        self.gap_height = gap_height
        self.wall_width = wall_width
        self.screen_height = screen_height
        self.speed = speed
        self.scored = False   # used for distance/pass tracking later
        self.cleared_walls = set()

    def clear_wall(self, side):
        """A shield impact destroys only the one wall that was struck."""
        if side not in ('top', 'bottom'):
            raise ValueError('Wall side must be top or bottom')
        self.cleared_walls.add(side)

    def update(self):
        self.x -= self.speed

    def is_off_screen(self):
        return self.x + self.wall_width < 0

    def get_top_rect(self):
        if 'top' in self.cleared_walls:
            return pygame.Rect(0, 0, 0, 0)
        top_height = self.gap_y - self.gap_height / 2
        return pygame.Rect(int(self.x), 0, self.wall_width, int(top_height))

    def get_bottom_rect(self):
        if 'bottom' in self.cleared_walls:
            return pygame.Rect(0, 0, 0, 0)
        bottom_y = self.gap_y + self.gap_height / 2
        return pygame.Rect(int(self.x), int(bottom_y), self.wall_width, int(self.screen_height - bottom_y))
