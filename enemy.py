# enemy.py

import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from pymunk import Vec2d

class Enemy:
    def __init__(self, x, y, speed=100, health=1, shoot_interval=1.5, color=(255, 0, 0), pattern="straight"):
        self.position = Vec2d(x, y)
        self.speed = speed
        self.health = health
        self.size = 40
        self.shape = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        self.projectiles = []
        self.shoot_timer = 0
        self.shoot_interval = shoot_interval
        self.color = color
        self.pattern = pattern

    def update(self, dt):
        self.move(dt)
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot()
            self.shoot_timer = 0

        for proj in self.projectiles[:]:
            proj.update(dt)
            if proj.position.y > SCREEN_HEIGHT:
                self.projectiles.remove(proj)

    def move(self, dt):
        movement = Vec2d(0, self.speed * dt)
        self.position += movement
        self.shape.topleft = (self.position.x, self.position.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)
        for proj in self.projectiles:
            proj.draw(screen)

    def shoot(self):
        self.projectiles.append(EnemyProjectile(self.position.x + self.size // 2, self.position.y + self.size, Vec2d(0, 200)))


class EnemyProjectile:
    def __init__(self, x, y, velocity=Vec2d(0, 200), size=10):
        self.position = Vec2d(x, y)
        self.velocity = velocity
        self.size = size

    def update(self, dt):
        self.position += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.size // 2)


class EnemyManager:
    def __init__(self):
        self.enemies = []

    def spawn_enemy(self, x, y, enemy_type="basic"):
        if enemy_type == "basic":
            enemy = Enemy(x, y, speed=100, health=1, shoot_interval=1.5, color=(255, 0, 0), pattern="straight")
        elif enemy_type == "zigzag":
            enemy = Enemy(x, y, speed=80, health=2, shoot_interval=2, color=(0, 255, 0), pattern="zigzag")
        elif enemy_type == "spread":
            enemy = Enemy(x, y, speed=60, health=3, shoot_interval=1, color=(0, 0, 255), pattern="spread")
        self.enemies.append(enemy)

    def update(self, dt):
        for enemy in self.enemies[:]:
            enemy.update(dt)
            if enemy.position.y > SCREEN_HEIGHT or enemy.health <= 0:
                self.enemies.remove(enemy)

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
