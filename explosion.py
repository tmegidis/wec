import pygame

class Explosion:
    def __init__(self, x, y):
        # Load explosion frames
        self.frames = []
        for i in range(1, 6):  # Assuming explosion1.png to explosion5.png
            filename = f"assets/explosion/explosion{i}.png"
            image = pygame.image.load(filename).convert_alpha()
            self.frames.append(image)

        self.current_frame = 0
        self.animation_speed = 0.1  # Adjust for desired animation speed
        self.frame_timer = 0
        self.position = (x, y)
        self.done = False  # Tracks if the animation is finished

    def update(self, dt):
        # Update the explosion animation
        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.done = True  # Mark as finished when all frames are shown

    def draw(self, screen):
        if not self.done:
            screen.blit(self.frames[self.current_frame], (int(self.position[0]), int(self.position[1])))
