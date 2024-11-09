# collision.py

import pygame
from settings import PLAYER_SIZE, ASTEROID_SIZE, PROJECTILE_SIZE

def detect_collisions(player, asteroids, projectiles, enemies):
    # Convert player position to a rectangle for collision detection
    player_rect = pygame.Rect(player.position.x, player.position.y, PLAYER_SIZE, PLAYER_SIZE)

    # Check for collisions between player and asteroids
    for asteroid in asteroids[:]:  # Using a copy to allow removal
        # Player and asteroid collision (rectangle check)
        asteroid_rect = pygame.Rect(asteroid.position.x, asteroid.position.y, ASTEROID_SIZE, ASTEROID_SIZE)
        if player_rect.colliderect(asteroid_rect):
            player.health -= 10  # Decrease player health
            asteroids.remove(asteroid)  # Remove the asteroid upon collision
            print(f"Player hit by asteroid! Health: {player.health}")

    # Check for collisions between player projectiles and asteroids (using circular hitbox)
    for asteroid in asteroids[:]:
        for projectile in projectiles[:]:  # Using a copy to allow removal
            # Calculate the distance between the asteroid center and the projectile
            distance = asteroid.position.get_distance(projectile.position)
            if distance <= asteroid.hitbox_radius + (PROJECTILE_SIZE / 2):  # Adjust for projectile radius if needed
                projectiles.remove(projectile)  # Remove projectile on collision
                if asteroid in asteroids:
                    asteroids.remove(asteroid)  # Remove asteroid if hit
                print("Asteroid destroyed!")
                break  # Exit inner loop to avoid checking removed asteroid

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
