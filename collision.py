# collision.py

import pygame
from settings import PLAYER_SIZE, ASTEROID_SIZE

def detect_collisions(player, asteroids, projectiles, enemies):
    # Convert player position to a rectangle for collision detection
    player_rect = pygame.Rect(player.position.x, player.position.y, PLAYER_SIZE, PLAYER_SIZE)

    # Check for collisions between player and asteroids
    for asteroid in asteroids[:]:  # Using a copy to allow removal
        asteroid_rect = pygame.Rect(asteroid.position.x, asteroid.position.y, ASTEROID_SIZE, ASTEROID_SIZE)

        # Player and asteroid collision
        if player_rect.colliderect(asteroid_rect):
            player.health -= 10  # Decrease player health
            asteroids.remove(asteroid)  # Remove the asteroid upon collision
            print(f"Player hit by asteroid! Health: {player.health}")

    # Check for collisions between player projectiles and asteroids
    for asteroid in asteroids[:]:
        asteroid_rect = pygame.Rect(asteroid.position.x, asteroid.position.y, ASTEROID_SIZE, ASTEROID_SIZE)
        for projectile in projectiles[:]:  # Using a copy to allow removal
            projectile_rect = pygame.Rect(projectile.position.x, projectile.position.y, 5, 5)  # Small size for projectile
            if projectile_rect.colliderect(asteroid_rect):
                projectiles.remove(projectile)  # Remove projectile
                if asteroid in asteroids:
                    asteroids.remove(asteroid)  # Remove asteroid if hit
                print("Asteroid destroyed!")
                break  # Break out to avoid checking removed asteroid

    # Check for collisions between player and enemy projectiles
    for enemy in enemies.enemies:
        for enemy_proj in enemy.projectiles[:]:  # Using a copy to allow removal
            enemy_proj_rect = pygame.Rect(enemy_proj.position.x, enemy_proj.position.y, enemy_proj.size, enemy_proj.size)
            if player_rect.colliderect(enemy_proj_rect):
                player.health -= 5  # Decrease player health if hit by enemy projectile
                enemy.projectiles.remove(enemy_proj)  # Remove the projectile after collision
                print(f"Player hit by enemy projectile! Health: {player.health}")

    # Check for collisions between player projectiles and enemies
    for enemy in enemies.enemies[:]:
        enemy_rect = pygame.Rect(enemy.position.x, enemy.position.y, enemy.size, enemy.size)
        for projectile in projectiles[:]:
            projectile_rect = pygame.Rect(projectile.position.x, projectile.position.y, 5, 5)
            if enemy_rect.colliderect(projectile_rect):
                enemy.health -= 1  # Decrease enemy health
                projectiles.remove(projectile)  # Remove projectile on collision
                print("Enemy hit by projectile!")
                if enemy.health <= 0:
                    enemies.enemies.remove(enemy)  # Remove enemy if health is depleted
                    print("Enemy destroyed!")
                break  # Break to avoid checking removed enemy
