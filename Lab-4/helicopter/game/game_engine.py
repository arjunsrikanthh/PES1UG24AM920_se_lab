"""
GameEngine: owns the helicopter and all obstacles.

Movement and wall contact belong here; presentation stays in renderer.
"""

import random
import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance = 0.0

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        if not self.game_over:
            self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if key == pygame.K_r and self.game_over:
            self.__init__()
        elif key == pygame.K_SPACE and not self.game_over:
            self.helicopter.shield_active = True

    def update(self):
        if self.game_over:
            return
        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        self.distance += SCROLL_SPEED
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]
        # Expand by one pixel per edge so exact touching counts as a hit.
        body = self.helicopter.get_rect().inflate(2, 2)
        for obstacle in self.obstacles[:]:
            if body.colliderect(obstacle.get_top_rect()) or body.colliderect(obstacle.get_bottom_rect()):
                if self.helicopter.shield_active:
                    self.helicopter.shield_active = False
                    self.obstacles.remove(obstacle)
                else:
                    self.game_over = True
                    break

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.helicopter, self.obstacles)
        renderer.draw_hud(surface, font, self.distance, self.helicopter.shield_active)
        if self.game_over:
            renderer.draw_game_over(surface, font, self.distance)
