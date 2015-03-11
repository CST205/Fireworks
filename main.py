__author__ = 'Gautier'
import os
from math import sin, cos, pi
from random import choice, random
import gc
os.environ['SDL_VIDEODRIVER'] = 'windib'
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, K_q, K_F4
pygame.display.init()
pygame.mixer.init()

# Start screen
info = pygame.display.Info()
screen_width = float(info.current_w)
screen_height = float(info.current_h)
bg_ratio = 1000.0 / 685.0
if screen_width / screen_height > bg_ratio:
    screen_width = screen_width * 0.8
    screen_height = screen_width / bg_ratio
else:
    screen_height = screen_height * 0.8
    screen_width = screen_height * bg_ratio
del info

screen_width = int(screen_width)
screen_height = int(screen_height)
screen_size = screen_width, screen_height
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Firework')

# Load background image
bg = pygame.image.load('pix.jpg')
bg = pygame.transform.smoothscale(bg, screen_size).convert()
screen.blit(bg, (0, 0))
pygame.display.flip()

# Load sounds effects
launch = pygame.mixer.Sound('fireworks_launch_denoised.wav')
explosion = pygame.mixer.Sound('blow.aif')

# Make overgrown pixel map
pix_list = []
for rgb_tuple in pygame.color.THECOLORS.values():
    if sum(rgb_tuple) > 509:
        pix_surf = pygame.Surface((3, 3))
        pix_surf.fill(rgb_tuple)
        pix_list.append(pix_surf.convert())
del rgb_tuple, pix_surf

# Define sprite classes
class Rocket(pygame.sprite.Sprite):

    def __init__(self, x, y, *groups):

        pygame.sprite.Sprite.__init__(self, *groups)

        self.x = x
        self.min_y = y
        self.y = int(490.0 * screen_height / 685.0)
        self.speed = -0.400
        self.image = choice(pix_list)
        self.rect = self.image.get_rect(center=(int(x), int(self.y)))

        launch.play()

    def update(self, act_delay):

        if self.y >= self.min_y:

            self.y = self.y + act_delay * self.speed
            self.image = choice(pix_list)
            self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        else:

            for i in range(300):
                speed = random() * 0.15 + 0.01
                Fire(self.x, self.y, speed, random() * 2 * pi,
                     self.image, 1,1,0,1, Sprites)
            for i in range(60):
                Fire(self.x, self.y, 0.16, random() * 2 * pi,
                     self.image, 1, 1,0, 1, Sprites)

            self.kill()

            explosion.play()

class Fire(pygame.sprite.Sprite):

    def __init__(self, x, y, speed, angle, image, gen, grav, stop, sub, *groups):

        pygame.sprite.Sprite.__init__(self, *groups)
        self.stop=stop
        self.sub=sub
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.speed_x = speed * cos(angle)
        self.speed_y = speed * sin(angle)
        self.image = image
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.total_time = 0
        self.gravityEffect = grav
        self.gen = gen
        self.radius = 1200 - gen

    def update(self, act_delay):
            if(self.stop<=5):
                self.stop+=1
                Fire(self.x, self.y, self.angle, self.speed, self.image, self.gen*1.2,self.gravityEffect, self.stop, 0, Sprites)
            if(self.total_time>self.radius/2):
                self.gravityEffect -= gravity
            if self.total_time < self.radius: # the radius
                self.x = self.x + act_delay * self.speed_x
                self.y = self.y + (act_delay * self.speed_y )- self.gravityEffect
                self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
                self.total_time += act_delay
            else:
                self.kill()
gravity = 0.03

Sprites = pygame.sprite.RenderUpdates()

def main():

    Clock = pygame.time.Clock()
    running = True
    act_delay = 0.0

    while running:

        # Process events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_F4:
                    running = False
            elif event.type == MOUSEBUTTONDOWN:
                Rocket(event.pos[0], event.pos[1], Sprites)

        # Draw
        Sprites.clear(screen, bg)
        Sprites.update(act_delay)
        dirty = Sprites.draw(screen)
        if len(Sprites) > 1000:
            pygame.display.flip()
        else:
            pygame.display.update(dirty)

        # collect garbage
        gc.collect()

        # Set speed
        act_delay = Clock.tick(80)
main()