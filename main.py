# main.py

import pygame
import sys
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, clock, SCREEN_MODE
from player import Player
from asteroid import Asteroid
from projectile import Projectile
from collision import detect_collisions
from enemy import EnemyManager


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_MODE)
pygame.display.set_caption("Enhanced Spaceship Game")

# Load and scale background image
background_img = pygame.image.load("assets/background.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_y1 = 0
background_y2 = -SCREEN_HEIGHT

# Font for UI elements
font = pygame.font.Font(None, 36)



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
    enemy_spawn_timer = 0  # Initialize enemy spawn timer
    projectiles = []
    asteroids = []
    enemy_manager = EnemyManager()  # Initialize the EnemyManager
    first_spawn = True

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
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys, dt)

        # Update player shooting animation
        player.update_shooting_sprite()

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

        # Spawn enemies every few seconds
        enemy_spawn_timer += dt


        if first_spawn:
            enemy_type = random.choice(["basic", "zigzag", "spread"])
            enemy_x = random.randint(0, SCREEN_WIDTH - 40)
            enemy_manager.spawn_enemy(enemy_x, 0, enemy_type)
            enemy_spawn_timer = 0
            first_spawn=False

        if enemy_spawn_timer > 5:  # Every 2 seconds, spawn a random type
            enemy_type = random.choice(["basic", "zigzag", "spread"])
            enemy_x = random.randint(0, SCREEN_WIDTH - 40)
            enemy_manager.spawn_enemy(enemy_x, 0, enemy_type)
            enemy_spawn_timer = 0

        # Update and draw enemies
        enemy_manager.update(dt)

        # Collision detection
        detect_collisions(player, asteroids, projectiles, enemy_manager)

        # Draw everything in the correct order
        screen.fill(BLACK)
        draw_rolling_background(screen, dt)  # Draw rolling background
        draw_health_bar(screen, player)  # Draw health bar on top of background
        player.draw(screen)  # Draw player on top
        for proj in projectiles:
            proj.draw(screen)
        for ast in asteroids:
            ast.draw(screen)
        enemy_manager.draw(screen)

        # Display ammo count
        ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
        screen.blit(ammo_text, (10, 40))  # Positioned below the health bar

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    game_loop()
