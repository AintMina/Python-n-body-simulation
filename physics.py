'''
Author: AintMina
Date: 27.10.2021

This is a gravitational simulation with particles.

Controls:
Left click = adds particle on mouse
Right click = deletes all particles
ESC = pause/play

TODO:
better collisions

'''

import pygame as pg
from random import randint, random, choice
import sys, math
from pygame.constants import VIDEORESIZE


''' Window prefs '''
width = 900                 # Window width
height = 900                # Window height
pg.init()
surf = pg.display.set_mode((width, height), pg.RESIZABLE)
pg.display.set_caption("N-Body Simulation V2")
clock = pg.time.Clock()
font = pg.font.SysFont('Liberation Serif', 18)


''' Colours '''
BLACK = (0, 0, 0)
WHITE = (225, 225, 225)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (150, 90, 62)
BLUE = (0, 0, 255)
COLORS = [WHITE, GREEN, RED, YELLOW, BLUE]


''' Settings '''
particlesAtStart = True    # True will spawn particles at random
numberOfParticles = 50      # Number of particles if above is True
listOfParticles = []        # A list that stores the particles
listOfCoordinates = []      # A list that stores the coordinates
G = 6.67408 * 10**-11                       # Gravitational constant use (6.67408 * 10**-11) for real life sim
mass = 3**2                 # Particle starting mass
vel = 0.0000001                   # Particle starting velocity
timeUnit = 40000                # Time step
wrapAround = True           # Universe wraps around itself(torus)
particleColour = YELLOW     # Colour of the particles
boundaries = False
softness = 5


gifMode = False             # Saves frames as png if True
limitFPS = False            # Limits FPS
limit = 30                  # FPS limit


def update_fps():
    fps = clock.get_fps()
    print("       " + str(int(fps)) + "       ", end='\r')

class Particle():
    def __init__(self, v, theta, m, x, y, col):
        self.x = float(x)
        self.y = float(y)
        self.mass = m
        self.v_x = v * math.cos(theta)
        self.v_y = v * math.sin(theta)
        self.forceX = 0.0
        self.forceY = 0.0
        self.numberInCoordinates = 0
        self.size = math.sqrt(m)
        self.colour = col

    def move(self):
        self.applyForce()
        self.v_x += (timeUnit / 2) * (self.forceX / self.mass)
        self.v_y += (timeUnit / 2) * (self.forceY / self.mass)

        for k, i in enumerate(listOfParticles):
            if i.x == self.x and i.y == self.y:
                self.numberInCoordinates = k
                listOfCoordinates[k] = [self.y + (self.v_y * timeUnit), self.x + (self.v_x * timeUnit)]

        ''' Universe wraps around itself(torus) '''
        if wrapAround:
            if self.x + (self.v_x * timeUnit) < 0:
                listOfCoordinates[self.numberInCoordinates][1] = width
            elif self.x + (self.v_x * timeUnit) > width:
                listOfCoordinates[self.numberInCoordinates][1] = 0
            elif self.y + (self.v_y * timeUnit) < 0:
                listOfCoordinates[self.numberInCoordinates][0] = height
            elif self.y + (self.v_y * timeUnit) > height:
                listOfCoordinates[self.numberInCoordinates][0] = 0
        elif boundaries:
            ''' Bounces particles back when going out of bounds '''
            if self.x + (self.v_x * timeUnit) < 0:
                self.v_x *= -1 / softness
            elif self.x + (self.v_x * timeUnit) > width:
                self.v_x *= -1 / softness
            elif self.y + (self.v_y * timeUnit) < 0:
                self.v_y *= -1 / softness
            elif self.y + (self.v_y * timeUnit) > height:
                self.v_y *= -1 / softness
        else:
            ''' Removes particles when going out of bounds '''
            if self.x + (self.v_x * timeUnit) < 0:
                listOfCoordinates.pop(self.numberInCoordinates)
                listOfParticles.pop(self.numberInCoordinates)
            elif self.x + (self.v_x * timeUnit) > width:
                listOfCoordinates.pop(self.numberInCoordinates)
                listOfParticles.pop(self.numberInCoordinates)
            elif self.y + (self.v_y * timeUnit) < 0:
                listOfCoordinates.pop(self.numberInCoordinates)
                listOfParticles.pop(self.numberInCoordinates)
            elif self.y + (self.v_y * timeUnit) > height:
                listOfCoordinates.pop(self.numberInCoordinates)
                listOfParticles.pop(self.numberInCoordinates)

    def applyForce(self):
        self.forceX = 0
        self.forceY = 0

        for i in listOfParticles:
            deltaX = i.x - self.x
            deltaY = i.y - self.y

            if not deltaX and not deltaY:
                continue

            if not deltaX:
                deltaX = 0.0000001

            deltaRsq = deltaY**2 + deltaX**2
            theta = math.atan2(deltaY, deltaX)
            deltaF = G * ((i.mass * self.mass) / deltaRsq)

            ''' Temporary collision '''
            if math.sqrt(deltaRsq) < (self.size + i.size):
                if deltaF > 10:
                    deltaF /= 10000
                deltaF = -deltaF / 8

            self.forceX += deltaF * math.cos(theta)
            self.forceY += deltaF * math.sin(theta)

            ''' Universe wraps around itself(torus) '''
            if wrapAround:
                deltaX2 = width - abs(deltaX)
                deltaY2 = height - abs(deltaY)

                if deltaX > 0:
                    deltaX2 *= -1
                if deltaY > 0:
                    deltaY2 *= -1
                if not deltaX2:
                    deltaX2 = 0.0000001

                deltaR2sq = deltaY2**2 + deltaX2**2
                theta2 = math.atan2(deltaY2, deltaX2)
                deltaF2 = G * ((i.mass * self.mass) / deltaR2sq)

                ''' Temporary collision '''
                if math.sqrt(deltaR2sq) < (self.size + i.size):
                    if deltaF2 > 2:
                        deltaF2 /= 10
                    deltaF2 = -deltaF2 / 8

                self.forceX += deltaF2 * math.cos(theta2)
                self.forceY += deltaF2 * math.sin(theta2)


                deltaX3 = width - abs(deltaX)
                deltaY3 = deltaY

                if deltaX > 0:
                    deltaX3 *= -1
                if not deltaX3:
                    deltaX3 = 0.0000001

                deltaR3sq = deltaY3**2 + deltaX3**2
                theta3 = math.atan2(deltaY3, deltaX3)
                deltaF3 = G * ((i.mass * self.mass) / deltaR3sq)

                ''' Temporary collision '''
                if math.sqrt(deltaR3sq) < (self.size + i.size):
                    if deltaF3 > 2:
                        deltaF3 /= 10
                    deltaF3 = -deltaF3 / 8

                self.forceX += deltaF3 * math.cos(theta3)
                self.forceY += deltaF3 * math.sin(theta3)


                deltaX4 = deltaX
                deltaY4 = height - abs(deltaY)

                if deltaY > 0:
                    deltaY4 *= -1
                if not deltaX4:
                    deltaX4 = 0.0000001

                deltaR4sq = deltaY4**2 + deltaX4**2
                theta4 = math.atan2(deltaY4, deltaX4)
                deltaF4 = G * ((i.mass * self.mass) / deltaR4sq)

                ''' Temporary collision '''
                if math.sqrt(deltaR4sq) < (self.size + i.size):
                    if deltaF4 > 2:
                        deltaF4 /= 10
                    deltaF4 = -deltaF4 / 8

                self.forceX += deltaF4 * math.cos(theta4)
                self.forceY += deltaF4 * math.sin(theta4)




if particlesAtStart:
    ''' Creates particles at random '''
    for i in range(0, numberOfParticles):
        X = randint(0, width)
        Y = randint(0, height)
        listOfParticles.append(Particle(vel, (random() * 2 * math.pi), mass, X, Y, choice(COLORS)))
        listOfCoordinates.append([Y, X])

counter = 0
while True:
    if limitFPS:
        ''' Limit FPS '''
        clock.tick(limit)
    else:
        clock.tick()
    
    update_fps()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            ''' Left click to add a particle with random speed and direction '''
            if event.button == 1:
                pos = pg.mouse.get_pos()
                listOfParticles.append(Particle(vel, random() * 2 * math.pi, mass, pos[0], pos[1], choice(COLORS)))
                listOfCoordinates.append([pos[1], pos[0]])
            ''' Right click to clear all particles '''
            if event.button == 3:
                listOfParticles = []
                listOfCoordinates = []

        ''' Pause Game'''
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                go = True
                while go:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                go = False
                                break
                        if event.type == pg.MOUSEBUTTONDOWN:
                            ''' Left click to add a particle with random speed and direction '''
                            if event.button == 1:
                                pos = pg.mouse.get_pos()
                                listOfParticles.append(Particle(vel, random() * 2 * math.pi, mass, pos[0], pos[1], choice(COLORS)))
                                listOfCoordinates.append([pos[1], pos[0]])
                                pg.draw.rect(surf, particleColour, [round(listOfCoordinates[-1][1]), round(listOfCoordinates[-1][0]), round(listOfParticles[-1].size), round(listOfParticles[-1].size)])
                                pg.display.flip()
                            ''' Right click to clear all particles '''
                            if event.button == 3:
                                listOfParticles = []
                                listOfCoordinates = []
                                surf.fill(BLACK)
                                pg.display.flip()
        if event.type == VIDEORESIZE:
            width, height = surf.get_size()

    surf.fill(BLACK)

    ''' Draws the particles '''
    for k, i in enumerate(listOfParticles):
        pg.draw.rect(surf, i.colour, [round(listOfCoordinates[k][1] - i.size/2), round(listOfCoordinates[k][0]) - i.size/2, round(i.size), round(i.size)])
        i.move()

    # for i in listOfParticles:
    #     checkCollision(i)

    ''' Updates the coordinates '''
    for k, i in enumerate(listOfParticles):
        i.y, i.x = listOfCoordinates[k]

    ''' Updates the window '''
    pg.display.flip()

    ''' Saves frames as png if enabled '''
    if gifMode:
        pg.image.save(surf, "./shots/" + str(counter) + ".png")
        print("         ", counter, "        ", end='\r')
        counter += 1