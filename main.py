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

game_over_img = pygame.image.load("assets/slides/lose.png").convert()
game_over_img = pygame.transform.scale(game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

win_img = pygame.image.load("assets/slides/win.png").convert()
win_img = pygame.transform.scale(win_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

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


def show_game_over():
    # Display the Game Over screen
    screen.blit(game_over_img, (0, 0))
    pygame.display.flip()

    # Wait for player to press a key to exit or restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()  # Exit the game (or add a restart option if desired)
        clock.tick(500)

def show_game_win():
    # Display the win Over screen
    screen.blit(win_img, (0, 0))
    pygame.display.flip()

    # Wait for player to press a key to exit or restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()  # Exit the game (or add a restart option if desired)
        clock.tick(500)


def game_loop():
    player = Player()
    asteroid_spawn_timer = 0
    enemy_spawn_timer = 0
    projectiles = []
    asteroids = []
    enemy_manager = EnemyManager()
    waves = Waves(enemy_manager, asteroids)
    ammo_manager = AmmoManager()
    explosions = []
    score = 0

    # Start the first wave
    current_wave_index = 0
    waves.start_wave(current_wave_index)

    while True:
        dt = clock.tick(60) / 1000  # Delta time calculation

        # Handle player death
        if player.health <= 0:
            show_game_over()
            break  # Exit the game loop to end the game after showing Game Over

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.ammo > 0:
                    player.shoot(projectiles)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    player.shooting_speed_factor = 0.5  # Temporarily double the shooting speed
                    player.no_ammo_reduction_time = player.no_ammo_reduction_duration
                    print('Shooting Speed Boost Activated')
                elif event.key == pygame.K_g:
                    if not player.double_gun_mode:
                        player.double_gun_mode = True
                        player.double_gun_timer = 3  # Set timer for 3 seconds
                        print('Double Gun Mode Activated')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If between waves, start the next wave on click
                if waves.is_between_waves():
                    current_wave_index += 1
                    if current_wave_index < len(waves.wave_data):
                        waves.start_wave(current_wave_index)
                        waves.between_waves = False  # Clear between waves flag
                    else:
                        print("All waves complete!")
                        show_game_win()
                        return  # Exit game loop to end the game

        # Only update entities if a wave is active
        if waves.is_wave_active():
            keys = pygame.key.get_pressed()
            player.move(keys, dt)
            player.update_shooting_sprite()

            # Update projectiles
            for proj in projectiles[:]:
                proj.update(dt)
                if proj.position.y < 0:
                    projectiles.remove(proj)

            # Update current wave
            waves.update(dt)

            # Update enemies and check for collisions
            enemy_manager.update(dt)
            destroyed_asteroids, destroyed_enemies = detect_collisions(
                player, asteroids, projectiles, enemy_manager, explosions, []
            )
            score += len(destroyed_asteroids) * 1 + len(destroyed_enemies) * 3

            # Update ammo pickups and explosions
            if random.random() < 0.01:
                ammo_manager.spawn_ammo()
            if ammo_manager.update(dt, player.shape):
                player.ammo += 1  # Increase ammo on pickup

            for explosion in explosions[:]:
                explosion.update(dt)
                if explosion.done:
                    explosions.remove(explosion)

        # If the wave is complete, set the between-waves state
        if not waves.is_wave_active() and not waves.is_between_waves():
            waves.between_waves = True

        # Draw everything in the correct order
        screen.fill(BLACK)
        draw_rolling_background(screen, dt)
        draw_health_bar(screen, player)
        player.draw(screen)

        for proj in projectiles:
            proj.draw(screen)
        for ast in asteroids:
            ast.draw(screen)

            # Update asteroids
        for ast in asteroids[:]:
            ast.update(dt)
            if ast.position.y > SCREEN_HEIGHT:
                asteroids.remove(ast)
        enemy_manager.draw(screen)
        ammo_manager.draw(screen)  # Draw ammo drops
        for explosion in explosions:
            explosion.draw(screen)

        # Display score and ammo count
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 70))
        ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
        screen.blit(ammo_text, (10, 40))

        # If between waves, display a message to prompt the player to click
        if waves.is_between_waves():
            font_large = pygame.font.Font(None, 60)

            if waves.current_wave == 0:
                line1 = "Wave Complete! Click to Start Next Wave!"
                line2 = "Asteroids approaching."
            elif waves.current_wave == 1:
                line1 = "Wave Complete! Our engineers installed a double gun."
                line2 = "Press 'G' to equip."
            elif waves.current_wave == 2:
                line1 = "Wave Complete! Final round"
                line2 = "Toughest enemies approach"
            elif waves.current_wave > 2:
                line1="VICTORY!!!"
                line2=""

            # Render the first line
            text1 = font_large.render(line1, True, (255, 215, 0))
            text_rect1 = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(text1, text_rect1)

            # Render the second line slightly below the first
            text2 = font_large.render(line2, True, (255, 215, 0))
            text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            screen.blit(text2, text_rect2)

        # Update the display
        pygame.display.flip()





if __name__ == "__main__":
    show_intro()  # Show intro cutscene first
    game_loop()
