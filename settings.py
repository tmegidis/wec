# settings.py

import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
PLAYER_SIZE = 50
PLAYER_SPEED = 50
PLAYER_HEALTH = 100
PLAYER_AMMO = 100

# Projectile settings
PROJECTILE_SPEED = 400
PROJECTILE_SIZE = 5

# Asteroid settings
ASTEROID_SIZE = 30
ASTEROID_SPEED = 200

# Physics settings
GRAVITY = (0, 0)  # No gravity in this space game

# Clock (for frame rate control)
clock = pygame.time.Clock()
