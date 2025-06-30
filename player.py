import pygame
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLODOWN
import random

class Player(CircleShape):
    def __init__(self, x, y, laser_sounds):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.laser_sounds = laser_sounds

        # Acceleration and movement
        self.acceleration_forward = 0.0
        self.acceleration_strafe = 0.0
        self.max_speed = PLAYER_SPEED
        self.acceleration_time = 0.8

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def get_speed_progression(self, t, max_speed, accel_time):
        progress = min(t / accel_time, 1)
        return max_speed * (1 - (1 - progress) ** 2)  # Ease-out quadratic

    def move(self, direction, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        speed = self.get_speed_progression(self.acceleration_forward, self.max_speed, self.acceleration_time)
        self.velocity += forward * speed * direction * dt

    def strafe(self, direction, dt):
        strafe = pygame.Vector2(0, 1).rotate(self.rotation + 90)
        speed = self.get_speed_progression(self.acceleration_strafe, self.max_speed / 1.2, self.acceleration_time)
        self.velocity += strafe * speed * direction * dt

    def update(self, dt):
        self.cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(0 - dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        moving_forward = keys[pygame.K_w] - keys[pygame.K_s]
        moving_strafe = keys[pygame.K_e] - keys[pygame.K_q]

        # Update acceleration timers
        if moving_forward != 0:
            self.acceleration_forward += dt
            self.acceleration_forward = min(self.acceleration_forward, self.acceleration_time)
        else:
            self.acceleration_forward -= dt
            self.acceleration_forward = max(self.acceleration_forward, 0)

        if moving_strafe != 0:
            self.acceleration_strafe += dt
            self.acceleration_strafe = min(self.acceleration_strafe, self.acceleration_time)
        else:
            self.acceleration_strafe -= dt
            self.acceleration_strafe = max(self.acceleration_strafe, 0)

        # Apply movement using helpers
        if self.acceleration_forward > 0:
            self.move(moving_forward, dt)

        if self.acceleration_strafe > 0:
            self.strafe(moving_strafe, dt)

        # Apply velocity and decay
        self.position += self.velocity * dt
        self.velocity *= 0.995  # friction-like decay

        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.cooldown > 0:
            return
        self.cooldown = PLAYER_SHOOT_COOLODOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        random.choice(self.laser_sounds).play()

    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)
