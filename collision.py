# collision.py

import pygame
from settings import PLAYER_SIZE, ASTEROID_SIZE


def detect_collisions(player, asteroids, projectiles):
    # Convert player position to a rectangle for collision detection
    player_rect = pygame.Rect(player.position.x, player.position.y, PLAYER_SIZE, PLAYER_SIZE)

    # Check for collisions between player and asteroids
    for asteroid in asteroids[:]:  # Using a copy to allow removal
        asteroid_rect = pygame.Rect(asteroid.position.x, asteroid.position.y, ASTEROID_SIZE, ASTEROID_SIZE)

        # Player and asteroid collision
        if player_rect.colliderect(asteroid_rect):
            player.health -= 10  # Decrease player health
            asteroids.remove(asteroid)  # Remove the asteroid upon collision
            print(f"Player hit! Health: {player.health}")

        # Check for collisions between projectiles and asteroids
        for projectile in projectiles[:]:  # Using a copy to allow removal
            projectile_rect = pygame.Rect(projectile.position.x, projectile.position.y, 5,
                                          5)  # Small size for projectile
            if projectile_rect.colliderect(asteroid_rect):
                projectiles.remove(projectile)  # Remove projectile
                if asteroid in asteroids:
                    asteroids.remove(asteroid)  # Remove asteroid if hit
                print("Asteroid destroyed!")
                break  # Break out to avoid checking removed asteroid
