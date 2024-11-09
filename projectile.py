import pygame
from settings import PROJECTILE_SPEED, PROJECTILE_SIZE
from pymunk import Vec2d
import os

class Projectile:
    def __init__(self, x, y):
        # Initialize the projectile's position and velocity
        self.position = Vec2d(x, y)
        self.velocity = Vec2d(0, -PROJECTILE_SPEED)  # Moves upward

        # Load the projectile image from the correct path
        projectile_img_path = os.path.join("assets", "projectile.png")
        self.image = pygame.image.load(projectile_img_path).convert_alpha()

        # Scale the projectile image to the desired size
        self.image = pygame.transform.scale(self.image, (PROJECTILE_SIZE, PROJECTILE_SIZE))

        # Get the rect of the image for positioning
        self.rect = self.image.get_rect()

    def update(self, dt):
        # Update the projectile's position based on velocity and delta time
        self.position += self.velocity * dt
        # Update the rect's position to match the projectile's position
        self.rect.topleft = (int(self.position.x), int(self.position.y))

    def draw(self, screen):
        # Draw the projectile image at its updated position
        screen.blit(self.image, self.rect.topleft)
