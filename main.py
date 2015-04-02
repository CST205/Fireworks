__author__ = 'Gautier, Nathaniel :)'
import os
import threading, time
from math import sin, cos, pi, ceil
from random import choice, random, randint
import gc
os.environ['SDL_VIDEODRIVER'] = 'windib'
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, K_q, K_F4
pygame.display.init()
pygame.mixer.init()


class Mode():
    def __init__(self):
        self.x = 0;
savemode = Mode

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

# Load music
song2 = pygame.mixer.Sound('Firework.wav')
song = pygame.mixer.Sound('Kissed.wav')

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

    def __init__(self, x, y, strength, *groups):

        pygame.sprite.Sprite.__init__(self, *groups)

        self.x = x
        self.min_y = y
        self.y = int(490.0 * screen_height / 685.0)
        self.speed = ceil(self.min_y / 1) * -1
        self.strength = strength
        self.image = choice(pix_list)
        self.rect = self.image.get_rect(center=(int(x), int(self.y)))

    def update(self, act_delay):

        if self.y >= self.min_y:
            Trail(self.x,self.y,self.image,Sprites)
            self.y = self.y + self.speed
            self.image = choice(pix_list)
            self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        else:
            range_c = randint(60,100);
            if(savemode.x==1):
                range_c = randint(15,25)
            for i in range(range_c):
                speed = random() * 0.10 + 0.01
                #random() * 2 * pi
                Fire(self.x, self.y, speed, randint(120,360),
                     self.image, self.strength, Sprites)
            self.kill()

# Is created behind a moving pixel. color degrades.
class Trail(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.x = x
        self.y = y
        self.total_time = 0
        self.image = image
        if(savemode==1):
            self.last = 50
        else:
            self.last = 400
        self.rect = self.image.get_rect(center=(int(x), int(y)))
    def update(self, act_delay):
        self.total_time+=act_delay
        pix_surf = pygame.Surface((3, 3))
        map = self.image.get_at((1,1))
        if(map[0]-20>0):
            map[0]-=20
        else:
            map[0]=0
        if(map[1]-20>0):
            map[1]-=20
        else:
            map[1]=0
        if(map[2]-20>0):
            map[2]-=20
        else:
            map[2]=0
        pix_surf.fill((map[0],map[1],map[2]))
        self.image = pix_surf
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        if(map[0]+map[1]+map[2]==0):
            self.kill()
        else:
            if(savemode.x==1 and self.last<self.total_time):
                self.kill()

# contains the firework explosion element
class Fire(pygame.sprite.Sprite):

    def __init__(self, x, y, speed, angle, image, strength, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.x = x
        self.y = y
        self.waitForTrail=4
        self.angle = angle
        self.speed = speed
        self.speed_x = speed * cos(angle)
        self.speed_y = speed * sin(angle)
        self.image = image
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.total_time = 0
        self.gravityEffect = 0
        self.radius = strength

    def update(self, act_delay):
        self.waitForTrail -= 1
        if(self.gravityEffect<12):
            self.gravityEffect += gravity
        if(self.speed>0):
            self.speed -= 0.01;
        if self.total_time < self.radius: # the radius
            if(savemode.x==0 and self.waitForTrail<0):
                Trail(self.x,self.y,self.image,Sprites)
            self.x = self.x + act_delay * self.speed_x
            self.y = self.y + (act_delay * self.speed_y ) + self.gravityEffect
            self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            self.total_time += act_delay
        else:
            self.kill()

gravity = 0.21
Sprites = pygame.sprite.RenderUpdates()

def setSaveMode(mode):
    savemode.x = mode;

def songData(art, ti):
	"""
		This function has a dependency you need to install.
		You'll need to install pyechonest. the easiest way to do this
		is to use setuptools and run the command "easy_install pyechonest"

	"""
	from pyechonest import config, song
	config.ECHO_NEST_API_KEY="J52LGDHNBUF5VOJDA";

	results = song.search(artist = art, title = ti);
	song_result = results[0];
	if song_result is None:
		print "Song not found.";
		return -1;
	return 	song_result.audio_summary['tempo'];

def main():
    Clock = pygame.time.Clock()
    running = True
    act_delay = 0.0
    counter = 0
    #tempo = songData("Katy Perry", "Firework")
    tempo = songData("Katy Perry", "I Kissed A Girl")
    song.play();
    while running:
        start = time.time()
        # Process events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_F4:
                    running = False
            elif event.type == MOUSEBUTTONDOWN:
                Rocket(event.pos[0], event.pos[1], randint(1600,2000), Sprites)

        # Draw
        Sprites.clear(screen, bg)
        Sprites.update(75)
        dirty = Sprites.draw(screen)
        if len(Sprites) > 1000:
            pygame.display.flip()
        else:
            pygame.display.update(dirty)
        if(counter+0.05>1/(tempo/60) and counter!=999999):
            Rocket(randint(100,screen_width), randint(100,screen_height), randint(1600,2000), Sprites)
            counter=999999
        if(counter==999999):
            counter=0
        else:
            counter+=0.05

        # collect garbage
        gc.collect()

        # Set speed
        end = time.time()-start;
        act_delay = Clock.tick(180)
        if(0.05-end<0):
            print "Overrun! too slow!"
            counter+=end-0.05
            setSaveMode(1)
        else:
            time.sleep(0.05-end);
            setSaveMode(0)
main()