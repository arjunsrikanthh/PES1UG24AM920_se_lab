"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
HUD_HEIGHT = 100
WINDOW_SIZE = (WIDTH, HEIGHT + HUD_HEIGHT)

COLOR_BG = (140, 200, 230)
COLOR_HELI = (60, 60, 70)
COLOR_OBSTACLE = (70, 150, 80)
COLOR_TEXT = (20, 20, 20)


def draw_scene(surface, helicopter, obstacles):
    surface.fill(COLOR_BG)
    for obstacle in obstacles:
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_top_rect())
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_bottom_rect())
    pygame.draw.rect(surface, COLOR_HELI, helicopter.get_rect(), border_radius=4)
    if helicopter.shield_active:
        shield_rect = helicopter.get_rect().inflate(14, 14)
        pygame.draw.ellipse(surface, (20, 90, 220), shield_rect, 3)


def draw_hud(surface, font, distance, shield_active, shield_hit):
    # Status belongs outside the collision arena so boundary checks stay visible.
    pygame.draw.rect(surface, (245, 248, 250), (0, HEIGHT, WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, (60, 80, 90), (0, HEIGHT), (WIDTH, HEIGHT), 2)
    draw_text(surface, font, f'Distance: {int(distance)} px', (14, HEIGHT + 9))
    status = 'ON (1 hit)' if shield_active else 'OFF'
    draw_text(surface, font, f'Shield: {status}', (400, HEIGHT + 9))
    if shield_hit:
        draw_text(surface, font, 'SHIELD HIT - wall cleared; shield used',
                  (14, HEIGHT + 37), (150, 55, 0))
    else:
        draw_text(surface, font, 'Avoid green walls. Fly through the gaps.',
                  (14, HEIGHT + 37))
    draw_text(surface, font, 'Up / Down: move   Space: shield   R: restart',
              (14, HEIGHT + 68))


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (180, 40, 40))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)


def draw_game_over(surface, font, distance):
    veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    veil.fill((10, 20, 30, 165))
    surface.blit(veil, (0, 0))
    for offset, text in ((-45, 'GAME OVER'),
                         (0, f'Final distance: {int(distance)} px'),
                         (45, 'Press R to restart')):
        label = font.render(text, True, (255, 255, 255))
        surface.blit(label, label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + offset)))
