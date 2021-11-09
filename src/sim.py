import pygame
import random
import sys
import math
import numpy as np
import numba as nb
import os

CORES = os.cpu_count()

class Simulation:
    def __init__(self, width = 800, height = 800, fps = 60,):
        self.fps = fps
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.background_color = (0, 0, 0)
        self.metaballs = []
        self.screen_arr = np.zeros((self.width, self.height, 3), dtype=np.int32)

    def setup(self):
        pygame.display.set_caption('Metaballs Simulation')
          
    def render(self):
        #for mb in self.metaballs:
        #    mb.render()

        # each pixel in grid
        for start in nb.prange(CORES):
            for x in range(start, self.width, CORES):
                for y in range(self.height):
                    _color = 0
                    for mb in self.metaballs:
                        dx, dy = mb.x - x,  mb.y - y                    
                        _color += 2500 * mb.r / (dx * dx + dy * dy + 1)

                    nc = _color;
                    if(nc > 255):
                        nc = 255
                    for c in range(3):
                        self.screen_arr[x, y, c] = nc

                

    def update(self):
        dt = self.clock.tick() / 1000.0 # get elapsed seconds

        for event in pygame.event.get():
           if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #self.screen.fill(self.background_color)

        for mb in self.metaballs:
            mb.update(dt)
        self.render()
        pygame.surfarray.blit_array(self.screen, self.screen_arr)
        pygame.display.flip()
        #self.clock.tick(self.fps)       

    def addMetaball(self):
        rx = random.randint(1, self.width)
        ry = random.randint(1, self.height)
        m = Metaball(sim=self, x=rx, y=ry)
        self.metaballs.append(m)

class Metaball(Simulation):
    def __init__(self, sim, x = 200, y = 200):
        self.x = x
        self.y = y
        self.r = 20
        self.vx, self.vy = (random.randint(-5,5), random.randint(-5, 5))
        self.color = (0, 255, 0)
        self.sim = sim
        print('created metaball at ', x, ' ', y)

    def render(self):
        pass
        #pygame.draw.circle(self.sim.screen, self.color, (self.x, self.y), self.r, width = 1)

    def update(self, dt):
        self.x += self.vx * dt * 5.0
        self.y += self.vy * dt * 5.0

        # check bounds
        if self.x > self.sim.width or self.x < 0:
            self.vx *= -1
        if self.y > self.sim.height or self.y < 0:
            self.vy *= -1