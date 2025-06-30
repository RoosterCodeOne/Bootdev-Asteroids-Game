from circleshape import *
from constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)

        new_traj1 = self.velocity.rotate(random_angle)
        new_traj2 = self.velocity.rotate(0 - random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid = Asteroid((self.position.x - new_radius), self.position.y, new_radius)
        asteroid.velocity = new_traj1 * 1.2
        asteroid = Asteroid((self.position.x + new_radius), self.position.y, new_radius)
        asteroid.velocity = new_traj2 * 1.2




