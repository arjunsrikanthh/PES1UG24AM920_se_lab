import os
import random
import sys
import unittest
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

SOURCE_DIR = Path(__file__).resolve().parents[1]
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

import pygame

from game.game_engine import GAP_HEIGHT, SCROLL_SPEED, GameEngine
from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import HEIGHT


def keys(*pressed):
    state = defaultdict(bool)
    state.update({key: True for key in pressed})
    return state


class HelicopterMovementTests(unittest.TestCase):
    def test_vertical_speed_is_capped_in_both_directions(self):
        helicopter = Helicopter(100, 250)

        for _ in range(30):
            helicopter.handle_input(keys(pygame.K_UP))
        self.assertEqual(helicopter.vy, -5)

        for _ in range(30):
            helicopter.handle_input(keys(pygame.K_DOWN))
        self.assertEqual(helicopter.vy, 5)

    def test_direction_reversal_discards_old_velocity(self):
        helicopter = Helicopter(100, 250)
        helicopter.vy = 5
        helicopter.handle_input(keys(pygame.K_UP))
        self.assertEqual(helicopter.vy, -0.4)

        helicopter.vy = -5
        helicopter.handle_input(keys(pygame.K_DOWN))
        self.assertEqual(helicopter.vy, 0.4)

    def test_update_clamps_both_screen_boundaries_using_body_height(self):
        helicopter = Helicopter(100, 10)
        helicopter.vy = -5
        helicopter.update(HEIGHT)
        self.assertEqual(helicopter.y, helicopter.height / 2)
        self.assertEqual(helicopter.get_rect().top, 0)

        helicopter.y = HEIGHT - 10
        helicopter.vy = 5
        helicopter.update(HEIGHT)
        self.assertEqual(helicopter.y, HEIGHT - helicopter.height / 2)
        self.assertEqual(helicopter.get_rect().bottom, HEIGHT)

    def test_releasing_keys_damps_velocity(self):
        helicopter = Helicopter(100, 250)
        helicopter.vy = 5
        helicopter.handle_input(keys())
        first_speed = abs(helicopter.vy)
        helicopter.handle_input(keys())
        second_speed = abs(helicopter.vy)
        self.assertGreater(first_speed, second_speed)
        self.assertGreaterEqual(second_speed, 0)


class GameEngineTests(unittest.TestCase):
    def setUp(self):
        random.seed(7)
        self.engine = GameEngine()
        self.engine.frames_until_spawn = 1_000_000

    def obstacle(self, gap_y=250):
        return Obstacle(
            x=100,
            gap_y=gap_y,
            gap_height=GAP_HEIGHT,
            wall_width=60,
            screen_height=HEIGHT,
            speed=0,
        )

    def collide_with_top_wall(self):
        self.engine.helicopter.y = 100
        self.engine.obstacles = [self.obstacle()]
        self.engine.update()

    def collide_with_bottom_wall(self):
        self.engine.helicopter.y = 400
        self.engine.obstacles = [self.obstacle()]
        self.engine.update()

    def test_top_and_bottom_wall_collisions_end_the_game(self):
        self.collide_with_top_wall()
        self.assertTrue(self.engine.game_over)

        self.setUp()
        self.collide_with_bottom_wall()
        self.assertTrue(self.engine.game_over)

    def test_helicopter_fits_safely_at_both_gap_margins(self):
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 188
        self.engine.update()
        self.assertFalse(self.engine.game_over)

        self.engine.helicopter.y = 312
        self.engine.update()
        self.assertFalse(self.engine.game_over)

    def test_exact_touching_of_either_wall_is_collision(self):
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 187
        self.engine.update()
        self.assertTrue(self.engine.game_over)

        self.setUp()
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 337
        self.engine.update()
        self.assertTrue(self.engine.game_over)

    def test_game_over_freezes_updates_until_restart(self):
        self.collide_with_top_wall()
        obstacle_x = self.engine.obstacles[0].x
        heli_rect = self.engine.helicopter.get_rect().copy()
        distance = self.engine.distance

        self.engine.update()
        self.assertEqual(self.engine.obstacles[0].x, obstacle_x)
        self.assertEqual(self.engine.helicopter.get_rect(), heli_rect)
        self.assertEqual(self.engine.distance, distance)

    def test_restart_clears_game_over_obstacles_and_distance(self):
        self.collide_with_top_wall()
        self.engine.distance = 42.0
        self.engine.handle_keydown(pygame.K_r)
        self.assertFalse(self.engine.game_over)
        self.assertEqual(self.engine.distance, 0.0)
        self.assertEqual(self.engine.obstacles, [])

    def test_distance_accumulates_by_scroll_speed_and_resets(self):
        self.engine.update()
        self.engine.update()
        self.assertEqual(self.engine.distance, 2 * SCROLL_SPEED)

        self.collide_with_top_wall()
        self.engine.handle_keydown(pygame.K_r)
        self.assertEqual(self.engine.distance, 0.0)

    def test_shield_is_consumed_by_one_contiguous_wall_contact(self):
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 100
        self.engine.handle_keydown(pygame.K_SPACE)
        self.assertTrue(self.engine.helicopter.shield_active)

        self.engine.update()
        self.assertFalse(self.engine.game_over)
        self.assertFalse(self.engine.helicopter.shield_active)

        self.engine.update()
        self.assertFalse(self.engine.game_over)

    def test_reentry_after_separation_is_lethal_without_rearming(self):
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 100
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.update()
        self.assertFalse(self.engine.game_over)

        self.engine.obstacles[0].x = 500
        self.engine.update()
        self.engine.obstacles[0].x = 100
        self.engine.update()
        self.assertTrue(self.engine.game_over)

    def test_second_distinct_wall_is_lethal_after_shield_is_consumed(self):
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 100
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.update()
        self.assertFalse(self.engine.game_over)

        self.engine.helicopter.y = 400
        self.engine.update()
        self.assertTrue(self.engine.game_over)

    def test_space_can_rearm_shield_during_play(self):
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 100
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.update()
        self.assertFalse(self.engine.helicopter.shield_active)

        self.engine.handle_keydown(pygame.K_SPACE)
        self.assertTrue(self.engine.helicopter.shield_active)
        self.engine.helicopter.y = 400
        self.engine.update()
        self.assertFalse(self.engine.game_over)
        self.assertFalse(self.engine.helicopter.shield_active)


if __name__ == "__main__":
    unittest.main()
