import pygame
import sys
import os
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

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
        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game over!")
                sys.exit(1)
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collision(shot):
                    asteroid.split()
                    shot.kill()
        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000








if __name__ == "__main__":
    main()