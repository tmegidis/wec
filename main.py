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
from waves import Waves
from ammo import AmmoManager
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

slide1 = pygame.image.load("assets/intro_slides/intro1.png").convert()
slide1 = pygame.transform.scale(slide1, (SCREEN_WIDTH, SCREEN_HEIGHT))
slide2 = pygame.image.load("assets/intro_slides/intro2.png").convert()
slide2 = pygame.transform.scale(slide2, (SCREEN_WIDTH, SCREEN_HEIGHT))
slide3 = pygame.image.load("assets/intro_slides/intro3.png").convert()
slide3 = pygame.transform.scale(slide3, (SCREEN_WIDTH, SCREEN_HEIGHT))
slide4 = pygame.image.load("assets/intro_slides/intro4.png").convert()
slide4 = pygame.transform.scale(slide4, (SCREEN_WIDTH, SCREEN_HEIGHT))

intro_slides = [
    slide1,
    slide2,
    slide3,
    slide4
]


def show_intro():
    slide_index = 0
    slide_duration = 30000  # 30 seconds per slide
    start_time = pygame.time.get_ticks()
    begin_button_text = "Begin"

    while slide_index < len(intro_slides):
        current_time = pygame.time.get_ticks()
        screen.fill(BLACK)
        screen.blit(intro_slides[slide_index], (0, 0))

        if slide_index == len(intro_slides) - 1:
            # Check if the mouse is hovering over the button
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = False

            # Render "Begin" button with hover effect
            begin_button = pygame.font.Font(None, 100).render(begin_button_text, True, (255, 215, 0))  # White color
            button_rect = begin_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            if button_rect.collidepoint(mouse_pos):
                begin_button = pygame.font.Font(None, 100).render(begin_button_text, True,
                                                                  (255, 215, 255))  # "Gold" color
                begin_button = pygame.transform.scale(begin_button, (
                    int(button_rect.width * 1.1), int(button_rect.height * 1.1)))  # Slightly larger
                is_hovered = True
            else:
                # Normal state
                begin_button = pygame.font.Font(None, 100).render(begin_button_text, True, (255, 215, 0))  # White color

            # Recalculate button rect to center it after scaling
            button_rect = begin_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(begin_button, button_rect.topleft)

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If on the last slide, only start the game if the button is clicked
                if slide_index == len(intro_slides) - 1 and button_rect.collidepoint(event.pos):
                    return  # Start game
                    # Advance to the next slide if it's not the last slide
                slide_index += 1
                start_time = current_time  # Reset timer for next slide

        # Automatically proceed to the next slide after the duration
        if current_time - start_time > slide_duration and slide_index < len(intro_slides) - 1:
            slide_index += 1
            start_time = current_time

        pygame.display.flip()
        clock.tick(60)


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
    enemy_spawn_timer = 0
    projectiles = []
    asteroids = []
    enemy_manager = EnemyManager()
    waves = Waves(enemy_manager, asteroids)
    ammo_manager = AmmoManager()  # Initialize the AmmoManager
    first_spawn = True
    explosions = []
    enemy_hitbox = []

    # Start the first wave
    current_wave_index = 0
    waves.start_wave(current_wave_index)

    while True:
        dt = clock.tick(60) / 1000  # Delta time calculation

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.ammo > 0:
                    player.shoot(projectiles)
                    player.ammo -= 1  # Decrease ammo count when shooting
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:  # Activate shooting speed boost (R key functionality)
                    player.shooting_speed_factor = 0.5  # Temporarily double the shooting speed
                    player.no_ammo_reduction_time = player.no_ammo_reduction_duration  # Disable ammo reduction for 3 seconds
                    print('Shooting Speed Boost Activated')
                elif event.key == pygame.K_g:  # Activate double gun mode (G key functionality)
                    if not player.double_gun_mode:  # Activate double gun mode only if it's not already active
                        player.double_gun_mode = True
                        player.double_gun_timer = 3  # Set timer for 3 seconds
                        print('Double Gun Mode Activated')

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

        # Update current wave
        waves.update(dt)

        # Check if the wave is complete and start the next wave if necessary
        if not waves.is_wave_active():
            current_wave_index += 1
            if current_wave_index < len(waves.wave_data):
                waves.start_wave(current_wave_index)
            else:
                print("All waves complete!")
                break

        # Update asteroids
        for ast in asteroids[:]:
            ast.update(dt)
            if ast.position.y > SCREEN_HEIGHT:
                asteroids.remove(ast)

        # Update enemies
        # Spawn enemies every few seconds
        enemy_spawn_timer += dt

        if first_spawn:
            enemy_type = random.choice(["basic", "zigzag", "spread"])
            enemy_x = random.randint(0, SCREEN_WIDTH - 40)
            enemy_manager.spawn_enemy(enemy_x, 0, enemy_type)
            enemy_spawn_timer = 0
            first_spawn = False

        if enemy_spawn_timer > 5:  # Every 5 seconds, spawn a random type of enemy
            enemy_type = random.choice(["basic", "zigzag", "spread"])
            enemy_x = random.randint(0, SCREEN_WIDTH - 40)
            enemy_manager.spawn_enemy(enemy_x, 0, enemy_type)
            enemy_spawn_timer = 0

        # Update and draw enemies
        enemy_manager.update(dt)

        # Update and draw ammo, checking for player collisions
        if random.random() < 0.01:  # Adjust probability for ammo spawn rate
            ammo_manager.spawn_ammo()

        if ammo_manager.update(dt, player.shape):  # Check for collision with player
            player.ammo += 1  # Increase player ammo count on pickup (adjust amount as needed)

        # Collision detection
        detect_collisions(player, asteroids, projectiles, enemy_manager, explosions, enemy_hitbox)

        for explosion in explosions[:]:
            explosion.update(dt)
            if explosion.done:
                explosions.remove(explosion)

        # Update pulse power-up state
        player.update_power_up(dt)

        # Handle the countdown for double gun mode
        if player.double_gun_mode:
            player.double_gun_timer -= dt
            if player.double_gun_timer <= 0:
                player.double_gun_mode = False  # Deactivate double gun mode after 3 seconds
                print('Double Gun Mode Deactivated')

        # Draw everything in the correct order
        screen.fill(BLACK)
        draw_rolling_background(screen, dt)
        draw_health_bar(screen, player)
        player.draw(screen)
        for proj in projectiles:
            proj.draw(screen)
        for ast in asteroids:
            ast.draw(screen)
        enemy_manager.draw(screen)
        ammo_manager.draw(screen)  # Draw ammo drops
        for explosion in explosions:
            explosion.draw(screen)

        # Display ammo count
        ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
        screen.blit(ammo_text, (10, 40))

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    show_intro()  # Show intro cutscene first
    game_loop()
