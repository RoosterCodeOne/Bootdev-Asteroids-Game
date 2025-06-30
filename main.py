import pygame
import sys
import os
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def resolve_asteroid_collision(a1, a2):
    # Vector between centers
    delta = a1.position - a2.position
    distance = delta.length()

    if distance == 0:
        return  # avoid division by zero

    # Normal vector
    normal = delta.normalize()

    # Relative velocity
    relative_velocity = a1.velocity - a2.velocity
    speed = relative_velocity.dot(normal)

    if speed > 0:
        return  # they're moving apart

    # Simple elastic collision (equal mass)
    impulse = normal * speed
    a1.velocity -= impulse
    a2.velocity += impulse

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    laser_sounds = [
        pygame.mixer.Sound(os.path.join("assets", "shotsounds", f"Lsr{i}.wav"))
        for i in range(1, 6)
    ]
    for sound in laser_sounds:
        sound.set_volume(0.3)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Shot.containers = (shots, updatable, drawable)

    Player.containers = (updatable, drawable)
    player = Player((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2), laser_sounds)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)
        # Asteroid-to-player collisions
        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game over!")
                sys.exit(1)
        # Asteroid-to-shot collisions
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collision(shot):
                    asteroid.split()
                    shot.kill()
        # Asteroid-to-asteroid collisions
        for i, asteroid1 in enumerate(asteroids):
            for asteroid2 in list(asteroids)[i+1:]:
                if asteroid1.collision(asteroid2):
                    resolve_asteroid_collision(asteroid1, asteroid2)

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000





if __name__ == "__main__":
    main()