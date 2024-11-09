import random
from asteroid import Asteroid
from enemy import EnemyManager
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, clock, SCREEN_MODE


class Waves:
    def __init__(self, enemy_manager, asteroids):
        self.enemy_manager = enemy_manager
        self.asteroids = asteroids
        self.current_wave = 0
        self.wave_active = False
        self.wave_start_time = 0
        self.wave_data = [
            {"enemies": 1, "asteroids": 0, "enemy_type": "basic"},
            {"enemies": 0, "asteroids": 4, "enemy_type": "zigzag"},
            {"enemies": 3, "asteroids": 1, "enemy_type": "spread"},
            # Add more waves with different configurations as needed
        ]

    def start_wave(self, wave_index):
        print("starting wave")
        """Initialize a specific wave."""
        self.current_wave = wave_index
        self.wave_active = True
        self.wave_data[self.current_wave]["enemies_left_to_spawn"] = self.wave_data[self.current_wave]["enemies"]
        self.wave_data[self.current_wave]["asteroids_left_to_spawn"] = self.wave_data[self.current_wave]["asteroids"]

        print(self.wave_data)
    def update(self, dt):
        """Update the wave logic, spawning enemies and asteroids."""
        if not self.wave_active or self.current_wave >= len(self.wave_data):
            return

        # Get current wave data
        wave_info = self.wave_data[self.current_wave]

        # Spawn enemies
        if wave_info["enemies_left_to_spawn"] > 0:
            enemy_x = random.randint(0, SCREEN_WIDTH - 40)
            self.enemy_manager.spawn_enemy(enemy_x, 0, wave_info["enemy_type"])
            wave_info["enemies_left_to_spawn"] -= 1  # Decrease count of remaining spawns

        # Spawn asteroids
        if wave_info["asteroids_left_to_spawn"] > 0:
            self.asteroids.append(Asteroid())
            wave_info["asteroids_left_to_spawn"] -= 1

        # Check if all enemies and asteroids have been spawned and destroyed
        if wave_info["enemies_left_to_spawn"] <= 0 and wave_info["asteroids_left_to_spawn"] <= 0:
            # Check if all spawned enemies and asteroids have been cleared
            if len(self.enemy_manager.enemies) == 0 and len(self.asteroids) == 0:
                self.wave_active = False  # Mark the wave as completed
                print(f"Wave {self.current_wave + 1} complete!")

    def is_wave_active(self):
        """Check if the current wave is still active."""
        return self.wave_active