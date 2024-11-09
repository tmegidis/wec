import pygame
import random
from settings import ASTEROID_SIZE, ASTEROID_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from pymunk import Vec2d

class Asteroid:
    def __init__(self, scale_factor=3):
        # Initialize the asteroid's position and velocity
        self.position = Vec2d(random.randint(0, SCREEN_WIDTH - ASTEROID_SIZE), 0)
        self.velocity = Vec2d(random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED), random.uniform(ASTEROID_SPEED / 2, ASTEROID_SPEED))

        # Load and scale the asteroid frames
        self.frames = []
        for i in range(1, 15):  # Assuming you have asteroid1.png to asteroid10.png
            filename = f"assets/asteroids/asteroid{i}.png"
            image = pygame.image.load(filename)
            new_width = int(ASTEROID_SIZE * scale_factor)
            new_height = int(ASTEROID_SIZE * scale_factor)
            scaled_image = pygame.transform.scale(image, (new_width, new_height))
            self.frames.append(scaled_image)

        # Animation parameters
        self.current_frame = 0
        self.animation_speed = 0.2  # Adjust for faster or slower animation
        self.frame_timer = 0

    def update(self, dt):
        # Update asteroid position based on its velocity and delta time
        self.position += self.velocity * dt

        # Update frame for animation
        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        # Draw the current frame of the asteroid
        screen.blit(self.frames[self.current_frame], (int(self.position.x), int(self.position.y)))
