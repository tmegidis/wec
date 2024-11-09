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

        # Load the thruster sprite (for movement)
        self.thruster_sprite = pygame.image.load("assets/spaceship_boost.png").convert_alpha()
        self.thruster_sprite = pygame.transform.scale(self.thruster_sprite, (PLAYER_SIZE, PLAYER_SIZE))

        # Load the pulse sprite for the power-up effect
        self.pulse_sprite = pygame.image.load("assets/pulse.png").convert_alpha()
        self.pulse_sprite = pygame.transform.scale(self.pulse_sprite, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))  # Larger area for pulse

        # Load damage sprites for health flashing, resizing them to PLAYER_SIZE
        self.damage_sprites = [
            pygame.transform.scale(
                pygame.image.load(f"assets/spaceship_damage/damage{i}.png").convert_alpha(),
                (PLAYER_SIZE, PLAYER_SIZE)
            ) for i in range(1, 5)
        ]

        # Flag to track if the player is shooting and animating
        self.is_shooting = False

        # Flag to track if the player is moving
        self.is_moving = False

        # Flash-related properties
        self.flashing = False
        self.flash_count = 0
        self.flash_timer = 0
        self.flash_interval = 0.25  # Flash every 0.25 seconds
        self.last_health_threshold = self.max_health
        self.damage_stage = 0  # Track which damage sprite to show next

        # Power-up related properties
        self.is_using_power_up = False
        self.power_up_cooldown = 0
        self.power_up_duration = 2  # Power-up lasts 2 seconds

        # New properties for shooting speed and no ammo reduction
        self.shooting_speed_factor = 1  # Normal shooting speed
        self.no_ammo_reduction_time = 0  # Time when ammo reduction is disabled
        self.no_ammo_reduction_duration = 3  # Duration in seconds for no ammo reduction

        # New properties for double gun mode
        self.double_gun_mode = False  # Flag to check if double guns are active
        self.double_gun_timer = 0  # Timer for double gun mode
        self.double_gun_duration = 5  # Duration for double guns in seconds

    def move(self, keys, dt):
        # Movement logic
        move_x = 0
        move_y = 0
        self.is_moving = False  # Reset the movement flag

        if keys[pygame.K_LEFT] and self.position.x > 0:
            move_x = -PLAYER_SPEED
            self.is_moving = True
        if keys[pygame.K_RIGHT] and self.position.x < SCREEN_WIDTH - PLAYER_SIZE:
            move_x = PLAYER_SPEED
            self.is_moving = True
        if keys[pygame.K_UP] and self.position.y > 0:
            move_y = -PLAYER_SPEED
            self.is_moving = True
        if keys[pygame.K_DOWN] and self.position.y < SCREEN_HEIGHT - PLAYER_SIZE:
            move_y = PLAYER_SPEED
            self.is_moving = True

        movement = Vec2d(move_x, move_y) * dt
        self.position += movement
        self.shape.topleft = (self.position.x, self.position.y)

        # Change to thruster sprite if moving
        if self.is_moving and not self.is_shooting:
            self.current_sprite = self.thruster_sprite
        elif not self.is_moving and not self.is_shooting and not self.flashing:
            self.current_sprite = self.default_sprite

    def draw(self, screen):
        # Draw current sprite
        screen.blit(self.current_sprite, self.shape.topleft)

    def update(self, dt, keys):
        """Update the player's state."""
        # Handle the 'R' key press for temporary shooting speed boost and no ammo reduction
        if keys[pygame.K_r]:
            if self.no_ammo_reduction_time <= 0:
                self.shooting_speed_factor = 0.5  # Double the shooting speed (half the delay)
                self.no_ammo_reduction_time = self.no_ammo_reduction_duration  # Activate no ammo reduction for 3 seconds

        if self.no_ammo_reduction_time > 0:
            self.no_ammo_reduction_time -= dt  # Countdown timer for no ammo reduction
        else:
            self.shooting_speed_factor = 1  # Reset to normal shooting speed after 3 seconds

        # Handle the 'G' key press for double gun mode
        if keys[pygame.K_g] and not self.double_gun_mode:
            self.double_gun_mode = True  # Activate double gun mode
            self.double_gun_timer = 3  # Set the timer for 3 seconds

        # Update the double gun mode timer
        if self.double_gun_mode:
            self.double_gun_timer -= dt
            if self.double_gun_timer <= 0:
                self.double_gun_mode = False  # Deactivate double gun mode after 3 seconds

    def shoot(self, projectiles):
        if self.ammo > 0 and not self.is_shooting:
            # Check if double gun mode is active and adjust projectile firing
            projectile_y = self.position.y - PROJECTILE_SIZE  # In front of the player (above)

            # If double gun mode is active, shoot two projectiles
            if self.double_gun_mode:
                # Left projectile (slightly to the left of the player's center)
                left_projectile_x = self.position.x + (self.shape.width // 2) - PROJECTILE_SIZE - 5
                left_projectile = Projectile(left_projectile_x, projectile_y)
                projectiles.append(left_projectile)

                # Right projectile (slightly to the right of the player's center)
                right_projectile_x = self.position.x + (self.shape.width // 2) + 5
                right_projectile = Projectile(right_projectile_x, projectile_y)
                projectiles.append(right_projectile)

                self.ammo -= 1  # Decrease ammo by 2 since two projectiles are fired
            else:
                # Default behavior: fire a single projectile
                center_projectile_x = self.position.x + (self.shape.width // 2) - PROJECTILE_SIZE // 2
                center_projectile = Projectile(center_projectile_x, projectile_y)
                projectiles.append(center_projectile)

                self.ammo -= 1  # Decrease ammo by 1 since one projectile is fired

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

    def update_damage_sprite(self, dt):
        """Check if health has dropped by 20 points and flash damage sprites."""
        current_health = self.health

        # Trigger flashing if health is at the next damage stage
        if self.health <= 80 - 20 * self.damage_stage:
            self.flashing = True
            self.flash_count = 0
            self.damage_stage += 1  # Move to the next damage stage

        # Handle flashing logic
        if self.flashing:
            self.flash_timer += dt

            # Flash every 0.25 second
            if self.flash_timer > self.flash_interval:
                if self.flash_count < 6:  # Flash 3 times, so 6 updates (on/off cycles)
                    if self.flash_count % 2 == 0:
                        # Show the current damage sprite
                        self.current_sprite = self.damage_sprites[self.damage_stage - 1]
                    else:
                        # Hide the sprite (show default)
                        self.current_sprite = self.default_sprite

                    self.flash_count += 1
                else:
                    # Reset sprite after flashing
                    self.current_sprite = self.default_sprite
                    self.flashing = False  # Stop flashing after 3 flashes

                self.flash_timer = 0  # Reset timer


    def update_power_up(self, dt):
        """Update the power-up state (cooldown and duration)."""
        if self.is_using_power_up:
            self.power_up_cooldown -= dt
            if self.power_up_cooldown <= 0:
                self.is_using_power_up = False
                self.current_sprite = self.default_sprite  # Revert back to normal sprite

    def update(self, dt, keys):
        """Update the player's state."""
        # Handle the 'R' key press for temporary shooting speed boost and no ammo reduction
        if keys[pygame.K_r]:
            if self.no_ammo_reduction_time <= 0:
                self.shooting_speed_factor = 0.5  # Double the shooting speed (half the delay)
                self.no_ammo_reduction_time = self.no_ammo_reduction_duration  # Activate no ammo reduction for 3 seconds

        if self.no_ammo_reduction_time > 0:
            self.no_ammo_reduction_time -= dt  # Countdown timer for no ammo reduction
        else:
            self.shooting_speed_factor = 1  # Reset to normal shooting speed after 3 seconds

        # Handle the 'G' key press for double gun mode
        if keys[pygame.K_g] and not self.double_gun_mode:
            self.double_gun_mode = True  # Activate double gun mode
            self.double_gun_timer = self.double_gun_duration  # Set the timer for 5 seconds

        # Update the double gun mode timer
        if self.double_gun_mode:
            self.double_gun_timer -= dt
            if self.double_gun_timer <= 0:
                self.double_gun_mode = False  # Deactivate double gun mode after 5 seconds
