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

    def test_shield_absorbs_one_obstacle_and_is_consumed(self):
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 100
        self.engine.handle_keydown(pygame.K_SPACE)
        self.assertTrue(self.engine.helicopter.shield_active)

        self.engine.update()
        self.assertFalse(self.engine.game_over)
        self.assertFalse(self.engine.helicopter.shield_active)
        self.assertEqual(self.engine.obstacles, [])

        self.engine.update()
        self.assertFalse(self.engine.game_over)

    def test_next_uncleared_obstacle_is_lethal_without_rearming(self):
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 100
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.update()
        self.assertFalse(self.engine.game_over)

        self.engine.obstacles.append(self.obstacle())
        self.engine.update()
        self.assertTrue(self.engine.game_over)

    def test_two_obstacle_hits_cannot_be_absorbed_by_one_shield(self):
        self.engine.obstacles = [self.obstacle(), self.obstacle()]
        self.engine.helicopter.y = 100
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.update()
        self.assertTrue(self.engine.game_over)
        self.assertFalse(self.engine.helicopter.shield_active)
        self.assertEqual(len(self.engine.obstacles), 1)

    def test_space_can_rearm_shield_during_play(self):
        self.engine.obstacles = [self.obstacle()]
        self.engine.helicopter.y = 100
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.update()
        self.assertFalse(self.engine.helicopter.shield_active)

        self.engine.handle_keydown(pygame.K_SPACE)
        self.assertTrue(self.engine.helicopter.shield_active)
        self.engine.helicopter.y = 400
        self.engine.obstacles.append(self.obstacle())
        self.engine.update()
        self.assertFalse(self.engine.game_over)
        self.assertFalse(self.engine.helicopter.shield_active)

    def test_bottom_wall_hit_also_consumes_the_shield(self):
        wall = self.obstacle()
        self.engine.obstacles = [wall]
        self.engine.helicopter.y = 400
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.update()
        self.assertFalse(self.engine.game_over)
        self.assertEqual(self.engine.obstacles, [])
        self.assertFalse(self.engine.helicopter.shield_active)

    def test_long_held_keys_cannot_leave_either_screen_edge(self):
        for direction in (pygame.K_UP, pygame.K_DOWN, pygame.K_UP):
            for _ in range(600):
                self.engine.handle_input(keys(direction))
                self.engine.update()
                body = self.engine.helicopter.get_rect()
                self.assertGreaterEqual(body.top, 0)
                self.assertLessEqual(body.bottom, HEIGHT)

    def test_unprotected_scrolling_wall_cannot_pass_through_player(self):
        self.engine.helicopter.y = 100
        wall = self.obstacle()
        wall.x = 300
        wall.speed = SCROLL_SPEED
        self.engine.obstacles = [wall]
        for _ in range(100):
            self.engine.update()
            if self.engine.game_over:
                break
        self.assertTrue(self.engine.game_over)
        self.assertGreaterEqual(wall.get_top_rect().right, self.engine.helicopter.get_rect().left)
        distance = self.engine.distance
        x = wall.x
        for _ in range(100):
            self.engine.update()
        self.assertEqual(wall.x, x)
        self.assertEqual(self.engine.distance, distance)

    def test_entire_gap_is_safe_and_adjacent_pixels_are_lethal(self):
        # Exhaustively test all 477 legal vertical positions at horizontal contact.
        for y in range(12, HEIGHT - 11):
            with self.subTest(y=y):
                engine = GameEngine()
                engine.frames_until_spawn = 100000
                wall = self.obstacle()
                engine.obstacles = [wall]
                engine.helicopter.y = y
                engine.update()
                body = engine.helicopter.get_rect()
                inside_gap = body.top > wall.get_top_rect().bottom and body.bottom < wall.get_bottom_rect().top
                self.assertEqual(engine.game_over, not inside_gap)

if __name__ == "__main__":
    unittest.main()
