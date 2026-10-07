"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4
MAX_SPEED = 5.0
DRAG = 0.8


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0
        self.shield_active = False

    def handle_input(self, keys_pressed):
        direction = int(bool(keys_pressed[pygame.K_DOWN])) - int(bool(keys_pressed[pygame.K_UP]))
        if direction:
            # Opposite input must move in the new direction on this frame.
            if self.vy * direction < 0:
                self.vy = 0.0
            self.vy = max(-MAX_SPEED, min(MAX_SPEED, self.vy + direction * THRUST))
        else:
            self.vy *= DRAG
            if abs(self.vy) < 0.05:
                self.vy = 0.0

    def update(self, height_bound):
        self.y += self.vy
        # y denotes the centre, so contain the entire body, not only its centre.
        half_height = self.height / 2
        if self.y < half_height:
            self.y = half_height
            self.vy = 0.0
        elif self.y > height_bound - half_height:
            self.y = height_bound - half_height
            self.vy = 0.0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
