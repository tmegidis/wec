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
        self.ammo = PLAYER_AMMO
        self.health = PLAYER_HEALTH

    def move(self, keys, dt):
        # Calculate horizontal movement
        move_x = 0
        if keys[pygame.K_LEFT] and self.position.x > 0:
            move_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.position.x < SCREEN_WIDTH - PLAYER_SIZE:
            move_x = PLAYER_SPEED

        # Create a new movement vector and update the position
        movement = Vec2d(move_x, 0) * dt
        self.position += movement

        # Update the player's shape position for collision detection
        self.shape.topleft = (self.position.x, self.position.y)

    def draw(self, screen):
        # Draw the player on the screen
        pygame.draw.rect(screen, WHITE, self.shape)

    def shoot(self, projectiles):
        # Shooting logic
        if self.ammo > 0:
            # Create a new projectile centered on the player and add it to the projectiles list
            new_projectile = Projectile(self.position.x + PLAYER_SIZE // 2, self.position.y)
            projectiles.append(new_projectile)
            self.ammo -= 1  # Decrease ammo
