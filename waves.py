import random
from asteroid import Asteroid
from enemy import EnemyManager
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Waves:
    def __init__(self, enemy_manager, asteroids):
        self.enemy_manager = enemy_manager
        self.asteroids = asteroids
        self.current_wave = 0
        self.wave_active = False
        self.between_waves = False  # New attribute to track if we are between waves
        self.wave_data = [
            {"enemies": 1, "asteroids": 0, "enemy_type": "basic"},
            {"enemies": 8, "asteroids": 4, "enemy_type": "zigzag"},
            {"enemies": 10, "asteroids": 5, "enemy_type": "spread"},
            # Add more waves with different configurations as needed
        ]

        # Spawning attributes
        self.spawn_timer = 0
        self.spawn_interval = 4  # Time in seconds between enemy spawns

    def start_wave(self, wave_index):
        """Initialize a specific wave."""
        self.current_wave = wave_index
        self.wave_active = True
        self.between_waves = False  # Reset between_waves flag when a wave starts
        self.wave_data[self.current_wave]["enemies_left_to_spawn"] = self.wave_data[self.current_wave]["enemies"]
        self.wave_data[self.current_wave]["asteroids_left_to_spawn"] = self.wave_data[self.current_wave]["asteroids"]
        self.spawn_timer = 0  # Reset spawn timer for the new wave

    def update(self, dt):
        """Update the wave logic, spawning enemies and asteroids."""
        if not self.wave_active or self.current_wave >= len(self.wave_data):
            return

        # Get current wave data
        wave_info = self.wave_data[self.current_wave]

        # Update the spawn timer
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval and wave_info["enemies_left_to_spawn"] > 0:
            # Spawn an enemy if the interval has passed and there are enemies left to spawn
            enemy_x = random.randint(0, SCREEN_WIDTH - 40)
            self.enemy_manager.spawn_enemy(enemy_x, 0, wave_info["enemy_type"])
            wave_info["enemies_left_to_spawn"] -= 1  # Decrease count of remaining spawns
            self.spawn_timer = 0  # Reset the spawn timer

        # Spawn asteroids all at once at the beginning of the wave
        while wave_info["asteroids_left_to_spawn"] > 0:
            self.asteroids.append(Asteroid())
            wave_info["asteroids_left_to_spawn"] -= 1

        # Check if all enemies and asteroids have been spawned and destroyed
        if wave_info["enemies_left_to_spawn"] <= 0 and wave_info["asteroids_left_to_spawn"] <= 0:
            # Check if all spawned enemies and asteroids have been cleared
            if len(self.enemy_manager.enemies) == 0 and len(self.asteroids) == 0:
                self.wave_active = False  # Mark the wave as completed
                self.between_waves = True  # Enter between-waves state
                print(f"Wave {self.current_wave + 1} complete!")

    def is_wave_active(self):
        """Check if the current wave is still active."""
        return self.wave_active

    def is_between_waves(self):
        """Check if the game is between waves."""
        return self.between_waves
