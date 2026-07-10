import pygame as pg # type: ignore
from pygame.locals import * # type: ignore
from sys import exit

import math

import random

pg.init()

FPS = 240

timeFactor = 240

inAddingMenu = False

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

text = pg.font.SysFont('Comic Sans MS', 30)

paused = False

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
        self.arrowLine = arrow(canvas, colour, position, position, 1)
        self.moving = True
    def goto(self,x,y):
        self.position = [x,y]
    def move(self,x,y):
        self.position = [self.position[0]+x,self.position[1]+y]
    def setVelocity(self,x,y):
        self.xVel = x
        self.yVel = y
    def updatePos(self):
        if self.moving and not paused:
            self.position = [(self.position[0]+(self.xVel*(timeFactor/FPS))),(self.position[1]+(self.yVel*(timeFactor/FPS)))]
        self.arrowLine.updatePos(self.position[0], self.position[1], self.xVel, self.yVel)
    def calcGravity(self, objects):
        if self.moving:
            for object in objects:
                if object != self and object.moving:
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
                                break
    def newTrail(self):
        particles.append(ball(self.canvas, self.colour, [self.position[0]-centreX, self.position[1]-centreY], 2, 0, 0, 0))
    def shrink(self):
        self.radius -= ((0.003 * timeFactor / FPS))
        if self.radius <= 0.1:
            particles.remove(self)
            del self
    def getShape(self):
        return ('Circle')

class arrow():
    def __init__(self, canvas, colour, startPos, endPos, width):
        self.canvas = canvas
        self.colour = colour
        self.startPos = startPos
        self.endPos = endPos
        self.width = width
        self.DAMPER = 0.01
    def updatePos(self, planetX, planetY, planetXVel, planetYVel):
        self.startPos = [planetX, planetY]
        self.endPos = [planetX + planetXVel/self.DAMPER, planetY + planetYVel/self.DAMPER]
        #self.width = math.sqrt(planetXVel ** 2 + planetYVel **2) / self.DAMPER
        self.width = math.ceil(2/zoomFactor)
    def render(self):
        pg.draw.line(self.canvas, self.colour, realToAbs(self.startPos), realToAbs(self.endPos), self.width)
        #pg.draw.polygon(self.canvas, self.colour, getArrowHead(self.startPos, self.endPos))

def getArrowHead(startPos, endPos): #Returns the points of an arrowhead given which way the line is supposed to be facing.
    if startPos[0] != endPos[0] and startPos[1] != endPos[1]:
        angleToUp = math.atan((startPos[0]-endPos[0])/(startPos[1]-endPos[1]))  * 180/3.14159
    else:
        if startPos[0] == endPos[0]:
            if endPos[1] > startPos[1]:
                return 180
            else:
                return 0
        elif startPos[1] == endPos[1]:
            if endPos[0] > startPos[0]:
                return 90
            else:
                return 270

    return angleToUp

print(getArrowHead([0,0],[-1,-1]))

def realToAbs(position):
    #return [int(position[0]/zoomFactor), int(position[1]/zoomFactor)]
    return [int((position[0]-centreX)/zoomFactor)+400, int((position[1]-centreY)/zoomFactor)+400]

def unzoom(position):
    return [int((position[0]-centreX)*zoomFactor)+centreX, int((position[1]-centreY)*zoomFactor)+centreY]

def renderScreen(objects):
    screen.fill((0,0,0))
    for object in objects:
        if object.getShape() == 'Circle':
            try:
                pg.draw.circle(object.canvas, object.colour, realToAbs(object.position), math.ceil(object.radius/zoomFactor))
                object.arrowLine.render()
            except:
                pass
    for particle in particles:
        if particle.getShape() == 'Circle':
            try:
                pg.draw.circle(particle.canvas, particle.colour, realToAbs(particle.position), math.ceil(particle.radius/zoomFactor))
            except:
                pass
    if inAddingMenu:
        screen.blit(text.render('Adding Planet...', False, (255,0,0)), (0,0))
    
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

    earth = ball(screen, (0,0,255), [400, 0], 0.5, 0, 0.5 , 10)
    objects.append(earth)

    moon = ball(screen, (200,200,200), [450,0], 0.2, 0, 0.7 , 1)
    objects.append(moon)


while True:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEWHEEL:
            if event.y == 1:
                if zoomFactor > 0.001:
                    zoomFactor /= 1.1
                else:
                    print('Zoom limit reached.')
            if event.y == -1:
                if zoomFactor < 100000:
                    zoomFactor *= 1.1
                else:
                    print('Zoom limit reached.')
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                for object in objects:
                    if math.sqrt((realToAbs(object.position)[0]-pg.mouse.get_pos()[0])**2 + (realToAbs(object.position)[1]-pg.mouse.get_pos()[1])**2) < math.ceil(object.radius/zoomFactor):
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
                if inAddingMenu:
                    bodyName.moving = True
                    inAddingMenu = False
                else:
                    inAddingMenu = True
                    bodyName = str(zoomFactor)
                    print(pg.mouse.get_pos())
                    print(centreX, centreY)
                    print(((pg.mouse.get_pos()[0])-400)*zoomFactor+centreX, ((pg.mouse.get_pos()[1])-400)*zoomFactor+centreY)
                    bodyName = ball(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [(pg.mouse.get_pos()[0]-400)*zoomFactor, (pg.mouse.get_pos()[1]-400)*zoomFactor], 5, 0, 0 , 1)
                    objects.append(bodyName)
                    bodyName.moving = False
            if inAddingMenu:
                if event.key == pg.K_m:
                    objects[-1].mass *= 8
                    objects[-1].radius *= 2
                elif event.key == pg.K_n:
                    if objects[-1].mass > 8 and objects[-1].radius >2:
                        objects[-1].mass /= 8
                        objects[-1].radius /= 2
                    else:
                        objects[-1].mass = 0
                        objects[-1].radius = 1
            if event.key == pg.K_p:
                paused = not paused
            if event.key == pg.K_r:
                centreX = screenWidth/2
                centreY = screenHeight/2
                zoomFactor = 1
                timeFactor = 240
                FPS = 240
            if event.key == pg.K_UP:
                timeFactor *= 2
                if FPS < 2400:
                    FPS *= 2
                else:
                    print('FPS Cap reached. Simulation quality may vary.')
            if event.key == pg.K_DOWN:
                timeFactor /= 2
                if FPS > 48:
                    FPS /= 2
                else:
                    print('FPS Lower bound reached.')
            if event.key == pg.K_q:
                for object in objects:
                    del object
                objects = []
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not inAddingMenu:
                print('Y key pressed')
                centreX = ((pg.mouse.get_pos()[0])-400)*zoomFactor+centreX
                print(centreX)
                centreY = ((pg.mouse.get_pos()[1])-400)*zoomFactor+centreY
                print(centreY)
            else:
                objects[-1].xVel = (pg.mouse.get_pos()[0] - realToAbs(objects[-1].position)[0]) * 0.01 * zoomFactor
                objects[-1].yVel = (pg.mouse.get_pos()[1] - realToAbs(objects[-1].position)[1]) * 0.01 * zoomFactor
    if not paused:        
        for object in objects:
            object.calcGravity(objects)
            if len(particles) < 10000:
                if object.lastTrail >= math.ceil(FPS/60):
                    object.lastTrail = 0
                    object.newTrail()
                else:
                    object.lastTrail += 1
        for particle in particles:
            particle.shrink()
    for object in objects:
            object.updatePos()
    renderScreen(objects)