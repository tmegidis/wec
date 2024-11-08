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
font = pygame.font.Font(None, 36)  # Font for ammo display

def draw_health_bar(screen, player):
    # Health bar dimensions
    bar_width = 200  # Max width of the health bar
    bar_height = 20
    bar_x = 10
    bar_y = 10

    # Calculate health ratio
    health_ratio = player.health / player.max_health
    current_bar_width = bar_width * health_ratio

    # Draw background bar (grey)
    pygame.draw.rect(screen, (169, 169, 169), (bar_x, bar_y, bar_width, bar_height))

    # Draw current health (red)
    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, current_bar_width, bar_height))

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
        player.move(keys, dt)

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

        # Draw health bar
        draw_health_bar(screen, player)

        # Display ammo count
        ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
        screen.blit(ammo_text, (10, 40))  # Positioned below the health bar

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    game_loop()
