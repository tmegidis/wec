# projectile.py

import pygame
from settings import PROJECTILE_SPEED, PROJECTILE_SIZE, WHITE
from pymunk import Vec2d

class Projectile:
    def __init__(self, x, y):
        # Initialize the projectile's position and velocity
        self.position = Vec2d(x, y)
        self.velocity = Vec2d(0, -PROJECTILE_SPEED)  # Moves upward

    def update(self, dt):
        # Update the projectile's position based on velocity and delta time
        self.position += self.velocity * dt

    def draw(self, screen):
        # Draw the projectile as a small circle on the screen
        pygame.draw.circle(screen, WHITE, (int(self.position.x), int(self.position.y)), PROJECTILE_SIZE)

    def get_position(self):
        return self.position
