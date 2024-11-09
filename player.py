import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED, PLAYER_HEALTH, PLAYER_AMMO, SCREEN_WIDTH, SCREEN_HEIGHT, PROJECTILE_SIZE
from projectile import Projectile
from pymunk import Vec2d
import os

class Player:
    def __init__(self):
        # Initialize player properties
        self.position = Vec2d(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE - 10)
        self.shape = pygame.Rect(self.position.x, self.position.y, PLAYER_SIZE, PLAYER_SIZE)
        self.ammo = PLAYER_AMMO
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH

        # Load spaceship attack sprites
        self.attack_sprites = []
        self.current_sprite_index = 0
        self.sprite_change_delay = 5  # Adjust this for animation speed
        self.sprite_counter = 0

        # Load all sprites from the spaceship_attack directory
        spaceship_attack_path = "assets/spaceship_attack/"
        for i in range(1, 5):
            sprite = pygame.image.load(os.path.join(spaceship_attack_path, f"Attack1{i}.png")).convert_alpha()
            sprite = pygame.transform.scale(sprite, (PLAYER_SIZE, PLAYER_SIZE))
            self.attack_sprites.append(sprite)

        # Set initial sprite (idle sprite)
        self.default_sprite = self.attack_sprites[0]
        self.current_sprite = self.default_sprite

        # Flag to track if the player is shooting and animating
        self.is_shooting = False

    def move(self, keys, dt):
        # Movement logic
        move_x = 0
        move_y = 0
        if keys[pygame.K_LEFT] and self.position.x > 0:
            move_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.position.x < SCREEN_WIDTH - PLAYER_SIZE:
            move_x = PLAYER_SPEED
        if keys[pygame.K_UP] and self.position.y > 0:
            move_y = -PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.position.y < SCREEN_HEIGHT - PLAYER_SIZE:
            move_y = PLAYER_SPEED

        movement = Vec2d(move_x, move_y) * dt
        self.position += movement
        self.shape.topleft = (self.position.x, self.position.y)

    def draw(self, screen):
        # Draw current sprite
        screen.blit(self.current_sprite, self.shape.topleft)

    def shoot(self, projectiles):
        if self.ammo > 0 and not self.is_shooting:
            # Calculate the spawn position so the projectile appears in front of the player
            projectile_x = self.position.x + (self.shape.width // 2) - (PROJECTILE_SIZE // 2)  # Center of the player
            projectile_y = self.position.y - PROJECTILE_SIZE  # In front of the player (above)

            # Create and add the projectile to the list
            new_projectile = Projectile(projectile_x, projectile_y)
            projectiles.append(new_projectile)
            self.ammo -= 1

            # Start the shooting animation
            self.is_shooting = True
            self.current_sprite_index = 0  # Start animation from the first sprite

    def update_shooting_sprite(self):
        if self.is_shooting:
            self.sprite_counter += 1
            if self.sprite_counter >= self.sprite_change_delay:
                self.sprite_counter = 0
                # Move to the next sprite in the animation
                self.current_sprite_index += 1

                if self.current_sprite_index < len(self.attack_sprites):
                    # Update to the next sprite in the sequence
                    self.current_sprite = self.attack_sprites[self.current_sprite_index]
                else:
                    # Animation is complete, reset to default sprite and stop shooting
                    self.current_sprite = self.default_sprite
                    self.is_shooting = False
                    self.current_sprite_index = 0
