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

# Load background image
background_img = pygame.image.load("background.png").convert()
background_y1 = 0  # Position of the first background
background_y2 = -SCREEN_HEIGHT  # Position of the second background

def draw_rolling_background(screen, dt):
    global background_y1, background_y2
    scroll_speed = 100  # Pixels per second

    # Move background positions down
    background_y1 += scroll_speed * dt
    background_y2 += scroll_speed * dt

    # Reset positions when they move off-screen
    if background_y1 >= SCREEN_HEIGHT:
        background_y1 = -SCREEN_HEIGHT
    if background_y2 >= SCREEN_HEIGHT:
        background_y2 = -SCREEN_HEIGHT

    # Draw the two images on screen
    screen.blit(background_img, (0, background_y1))
    screen.blit(background_img, (0, background_y2))

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
        draw_rolling_background(screen, dt)  # Draw rolling background
        player.draw(screen)
        for proj in projectiles:
            proj.draw(screen)
        for ast in asteroids:
            ast.draw(screen)

        # Display ammo count
        ammo_text = pygame.font.Font(None, 36).render(f"Ammo: {player.ammo}", True, (255, 255, 255))
        screen.blit(ammo_text, (10, 40))

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    game_loop()
