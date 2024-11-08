# main.py

import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, clock
from player import Player
from asteroid import Asteroid
from projectile import Projectile
from collision import detect_collisions

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced Spaceship Game")


def game_loop():
    player = Player()
    asteroid_spawn_timer = 0
    projectiles = []
    asteroids = []

    while True:
        dt = clock.tick(60) / 1000  # Delta time calculation

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(projectiles)

        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys, dt)  # Pass keys and dt for movement

        # Update projectiles
        for proj in projectiles[:]:
            proj.update(dt)
            if proj.position.y < 0:  # Remove if out of screen
                projectiles.remove(proj)

        # Spawn and update asteroids
        asteroid_spawn_timer += dt
        if asteroid_spawn_timer > 1:  # Spawn asteroid every second
            asteroids.append(Asteroid())
            asteroid_spawn_timer = 0
        for ast in asteroids[:]:
            ast.update(dt)
            if ast.position.y > SCREEN_HEIGHT:  # Remove if out of screen
                asteroids.remove(ast)

        # Collision detection
        detect_collisions(player, asteroids, projectiles)

        # Draw everything
        screen.fill(BLACK)
        player.draw(screen)
        for proj in projectiles:
            proj.draw(screen)
        for ast in asteroids:
            ast.draw(screen)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    game_loop()
