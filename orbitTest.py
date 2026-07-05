import pygame as pg
from pygame.locals import *
from sys import exit

import math

import random

pg.init()

FPS = 240

timeFactor = 240

objects = []
particles = []

screenWidth = 800
screenHeight = 800
centreX = screenWidth/2
centreY = screenHeight/2
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Orbit Test")
screen.fill((0,0,0))

zoomFactor = 1

clock = pg.time.Clock()

class ball():
    def __init__(self, canvas, colour, position, radius, xVel, yVel, mass):
        self.canvas = canvas
        self.colour = colour
        self.position = [position[0] + centreX, position[1] + centreY]
        self.radius = radius
        self.xVel = xVel
        self.yVel = yVel
        self.mass = mass
        self.lastTrail = 0
    def goto(self,x,y):
        self.position = [x,y]
    def move(self,x,y):
        self.position = [self.position[0]+x,self.position[1]+y]
    def setVelocity(self,x,y):
        self.xVel = x
        self.yVel = y
    def updatePos(self):
        self.position = [(self.position[0]+(self.xVel*(timeFactor/FPS))),(self.position[1]+(self.yVel*(timeFactor/FPS)))]
    def calcGravity(self, objects):
        for object in objects:
            if object != self:
                distance = math.sqrt((object.position[0]-self.position[0])**2 + (object.position[1]-self.position[1])**2)
                if distance > self.radius + object.radius:
                    direction = [(object.position[0]-self.position[0])/distance, (object.position[1]-self.position[1])/distance]
                    force = object.mass / (distance**2)
                    self.xVel += (force * direction[0]) * (timeFactor/FPS)
                    self.yVel += (force * direction[1]) * (timeFactor/FPS)
                else:
                    if False:
                        print('Collision.')
                        if object.mass > self.mass:
                            objects.remove(self)
                            del self
                        else:
                            objects.remove(object)
                            del object
    def newTrail(self):
        particles.append(ball(self.canvas, self.colour, [self.position[0]-centreX, self.position[1]-centreY], 2, 0, 0, 0))
    def shrink(self):
        self.radius -= (0.0005 * timeFactor / FPS)
        if self.radius <= 1:
            particles.remove(self)
            del self
    def getShape(self):
        return ('Circle')

def zoom(position):
    #return [int(position[0]/zoomFactor), int(position[1]/zoomFactor)]
    return [int((position[0]-centreX)/zoomFactor)+400, int((position[1]-centreY)/zoomFactor)+400]

def unzoom(position):
    return [int((position[0]-centreX)*zoomFactor)+centreX, int((position[1]-centreY)*zoomFactor)+centreY]

def renderScreen(objects):
    screen.fill((0,0,0))
    for object in objects:
        if object.getShape() == 'Circle':
            pg.draw.circle(object.canvas, object.colour, zoom(object.position), math.ceil(object.radius/zoomFactor))
    for particle in particles:
        if particle.getShape() == 'Circle':
            pg.draw.circle(particle.canvas, particle.colour, zoom(particle.position), math.ceil(particle.radius/zoomFactor))
    pg.display.update()

if False:
    doga = ball(screen, (0,255,255), [0,0], 10, 0, -.1, 1000)
    ian = ball(screen, (255,0,0), [500,500], 10, -.1, .1 , 10)
    objects.append(doga)
    objects.append(ian)

    sustingus = ball(screen, (255,255,0), [-200,-200], 2, 0, 0 , 1)
    objects.append(sustingus)

    superStresseman = ball(screen, (255,0,255), [800,800], 1, 0.001, 0 , 1)
    objects.append(superStresseman)

if True:
    sun = ball(screen, (255,255,0), [0,0], 20, 0, -0.05 , 100)
    objects.append(sun)

    earth = ball(screen, (0,0,255), [400, 0], 0, 0, 0.5 , 10)
    objects.append(earth)

    moon = ball(screen, (200,200,200), [450,0], 0, 0, 0.7 , 0.1)
    objects.append(moon)

print(zoom([400,400]))

while True:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEWHEEL:
            if event.y == 1:
                zoomFactor *= 1.1
            if event.y == -1:
                zoomFactor /= 1.1
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                for object in objects:
                    if math.sqrt((zoom(object.position)[0]-zoom(pg.mouse.get_pos())[0])**2 + (zoom(object.position)[1]-zoom(pg.mouse.get_pos())[1])**2) < math.ceil(object.radius/zoomFactor):
                        objects.remove(object)
                        print('Killed')
                        del object
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_0:
                print('jarona...')
                FPS = 30
            if event.key == pg.K_1:
                print('sus')
                FPS = 60
            elif event.key == pg.K_2:
                print('stingus')
                FPS = 120
            elif event.key == pg.K_3:
                print('im falling!')
                FPS = 240
            elif event.key == pg.K_SPACE:
                bodyName = str(zoomFactor)
                print(pg.mouse.get_pos())
                print(centreX, centreY)
                print(((pg.mouse.get_pos()[0])-400)*zoomFactor+centreX, ((pg.mouse.get_pos()[1])-400)*zoomFactor+centreY)
                bodyName = ball(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [(pg.mouse.get_pos()[0]-400)*zoomFactor, (pg.mouse.get_pos()[1]-400)*zoomFactor], 5, 0, 0 , 1)
                objects.append(bodyName)
                print(objects[-1])
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            print('Y key pressed')
            centreX = ((pg.mouse.get_pos()[0])-400)*zoomFactor+centreX
            print(centreX)
            centreY = ((pg.mouse.get_pos()[1])-400)*zoomFactor+centreY
            print(centreY)
    for object in objects:
        object.calcGravity(objects)
    for object in objects:
        object.updatePos()
        if len(particles) < 10000:
            if object.lastTrail >= math.ceil(FPS/60):
                object.lastTrail = 0
                object.newTrail()
            else:
                object.lastTrail += 1
    for particle in particles:
        particle.shrink()
    renderScreen(objects)