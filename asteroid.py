# asteroid.py

import pygame
import random
from settings import ASTEROID_SIZE, ASTEROID_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from pymunk import Vec2d

class Asteroid:
    def __init__(self):
        # Initialize the asteroid's position and velocity
        self.position = Vec2d(random.randint(0, SCREEN_WIDTH - ASTEROID_SIZE), 0)
        # Random horizontal velocity and downward speed for movement
        self.velocity = Vec2d(random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED), random.uniform(ASTEROID_SPEED / 2, ASTEROID_SPEED))

    def update(self, dt):
        # Update asteroid position based on its velocity and delta time
        self.position += self.velocity * dt

    def draw(self, screen):
        # Draw the asteroid as a circle
        pygame.draw.circle(screen, WHITE, (int(self.position.x), int(self.position.y)), ASTEROID_SIZE // 2)
