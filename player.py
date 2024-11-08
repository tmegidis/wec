# player.py

import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED, PLAYER_HEALTH, PLAYER_AMMO, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from projectile import Projectile
from pymunk import Vec2d

class Player:
    def __init__(self):
        # Initialize player properties
        self.position = Vec2d(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE - 10)
        self.shape = pygame.Rect(self.position.x, self.position.y, PLAYER_SIZE, PLAYER_SIZE)
        self.ammo = PLAYER_AMMO  # Set initial ammo from settings
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH  # Track maximum health for scaling the health bar

    def move(self, keys, dt):
        # Movement logic as before
        move_x = 0
        move_y = 0
        if keys[pygame.K_LEFT] and self.position.x > 0:
            move_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.position.x < SCREEN_WIDTH - PLAYER_SIZE:
            move_x = PLAYER_SPEED
        if keys[pygame.K_UP] and self.position.y > 0:
            move_y = -PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.position.y < SCREEN_HEIGHT - PLAYER_SIZE:
            move_y = PLAYER_SPEED

        movement = Vec2d(move_x, move_y) * dt
        self.position += movement
        self.shape.topleft = (self.position.x, self.position.y)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.shape)

    def shoot(self, projectiles):
        if self.ammo > 0:
            new_projectile = Projectile(self.position.x + PLAYER_SIZE // 2, self.position.y)
            projectiles.append(new_projectile)
            self.ammo -= 1
