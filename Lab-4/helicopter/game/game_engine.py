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
        self.shield_hit_frames = 0

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

    def _wall_contacts(self):
        body = self.helicopter.get_rect()
        contacts = set()
        for obstacle in self.obstacles:
            for side, wall in (('top', obstacle.get_top_rect()),
                               ('bottom', obstacle.get_bottom_rect())):
                if not wall.width or not wall.height:
                    continue
                # Rect.colliderect excludes exact edges; the task says touching.
                if (body.left <= wall.right and body.right >= wall.left
                        and body.top <= wall.bottom and body.bottom >= wall.top):
                    contacts.add((obstacle, side))
        return contacts

    def update(self):
        if self.game_over:
            return
        self.shield_hit_frames = max(0, self.shield_hit_frames - 1)
        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        self.distance += SCROLL_SPEED
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]
        contacts = self._wall_contacts()
        for obstacle, side in contacts:
            if self.helicopter.shield_active:
                self.helicopter.shield_active = False
                obstacle.clear_wall(side)
                self.shield_hit_frames = 60
            else:
                self.game_over = True
                break

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.helicopter, self.obstacles)
        renderer.draw_hud(surface, font, self.distance, self.helicopter.shield_active,
                          self.shield_hit_frames > 0)
        if self.game_over:
            renderer.draw_game_over(surface, font, self.distance)
