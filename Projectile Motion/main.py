# Projectile Motion

import math
import random
import pygame

from functions import *

pygame.init()

# intialize the window height and width
SCREEN = WIDTH, HEIGHT = 288, 512

# class is used to retrieve information about the user's display.
info = pygame.display.Info()

width = info.current_w
height = info.current_h

# screen mode 
if width >= height:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)


# Assign the real clock for the game 
clock = pygame.time.Clock()

# frame per second
FPS = 60

# define used colors
BLACK = (18, 18, 18)
WHITE = (217, 217, 217)
RED = (252, 91, 122)
GREEN = (29, 161, 16)
BLUE = (78, 193, 246)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)
AQUA = (0,249,182)


COLORS = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]

# define the font type 
font = pygame.font.SysFont('verdana', 12)


# start fire point
origin = (20, 340)


# radius = 250


# intial velocity (input)
u = 50

# gravity
g = 9.8


 # return sprite (ball)
class Projectile(pygame.sprite.Sprite):

    def __init__(self, u, theta):
        super(Projectile, self).__init__()

        # initial given velocity (input)
        self.u = u
        
        # intial theta 
        self.theta = toRadian(abs(theta))

        # fire point
        self.x, self.y = origin

        # ball color set
        self.color = random.choice(COLORS)
 
        self.ch = 0
        self.dx = 2
        
        self.f = self.getTrajectory()

        # horizontal distance range
        self.range = self.x + abs(self.getRange())

        
        self.path = []

   
    def timeOfFlight(self):
        return round((2 * self.u * math.sin(self.theta)) / g, 2)

# The range is a scalar quantity that represents the maximum distance covered by the projectile horizontally,
# whereas the trajectory is a vector quantity that represents the path traced by the projectile in the air, 
# including its direction and magnitude.
    def getRange(self):
        range_ = ((self.u ** 2) * 2 * math.sin(self.theta) * math.cos(self.theta)) / g
        return round(range_, 2)


    def getMaxHeight(self):
        h = ((self.u ** 2) * (math.sin(self.theta)) ** 2) / (2 * g)
        return round(h, 2)

# On the other hand, the trajectory refers to the path followed by the projectile from the moment of its launch until it hits the ground. 
# It is the curve traced by the projectile in the air, 
# taking into account its initial velocity, angle of projection, and the force of gravity.
    def getTrajectory(self):
        return round(g /  (2 * (self.u ** 2) * (math.cos(self.theta) ** 2)), 4)


    def getProjectilePos(self, x):
        return x * math.tan(self.theta) - self.f * x ** 2

    def update(self):
        if self.x >= self.range:
            # stop ball
            self.dx = 0

        self.x += self.dx

        # vertical according to horizontal position
        self.ch = self.getProjectilePos(self.x - origin[0])

        # the height of the ball from bottom
        self.path.append((self.x, self.y-abs(self.ch)))

        #it takes the last 50 elements of self.path and assigns them.
        self.path = self.path[-50:]

        # draw the ball to the screen with 5 radius 
        pygame.draw.circle(win, self.color, self.path[-1], 5)
        ball = pygame.transform.scale_by(pygame.image.load("assets/football.png"),0.05)
     
        # the trail of the fire ball
        pygame.draw.circle(win, WHITE, self.path[-1], 5, 1)

        # assign the last five small balls in same fire ball position
        for pos in self.path[:-1:5]:
            pygame.draw.circle(win, WHITE, pos, 1)

projectile_group = pygame.sprite.Group()

clicked = False
currentp = None


# intial drawe theta under the line 
theta = -30

# position of the end point for the line 
end = getPosOnCircumeference(theta, origin)

arct = toRadian(theta)


# draw the angle arc
arcrect = pygame.Rect(origin[0]-30, origin[1]-30, 60, 60)


running = True
while running:
    win.fill(BLACK)
    

    for event in pygame.event.get():

        # close game / stop running 
        if event.type == pygame.QUIT:
            running = False
            
         # close game with escape or q (key)   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False

            # remove the drawn balls 
            if event.key == pygame.K_r:
                projectile_group.empty()
                currentp = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

           # clicked position
            pos = event.pos

            theta = getAngle(pos, origin)
            if -90 < theta <= 0:
                projectile = Projectile(u, theta)
                projectile_group.add(projectile)

                # the last projectile for data 
                currentp = projectile

        if event.type == pygame.MOUSEMOTION:
            if clicked:
                pos = event.pos
                theta = getAngle(pos, origin)
                if -90 < theta <= 0:
                    end = getPosOnCircumeference(theta, origin)
                    arct = toRadian(theta)
    
    pygame.draw.line(win, WHITE, origin, (origin[0] + 250, origin[1]), 2)
    pygame.draw.line(win, WHITE, origin, (origin[0], origin[1] - 250), 2)
    pygame.draw.line(win, AQUA, origin, end, 2)
    pygame.draw.circle(win, WHITE, origin, 3)
    pygame.draw.arc(win, AQUA, arcrect, 0, -arct, 2)

    projectile_group.update()

    # Info *******************************************************************
    title = font.render("Projectile Motion", True, WHITE)
    fpstext = font.render(f"FPS : {int(clock.get_fps())}", True, WHITE)
    thetatext = font.render(f"Angle : {int(abs(theta))}", True, WHITE)
    degreetext = font.render(f"{int(abs(theta))}°", True, YELLOW)
    win.blit(title, (80, 30))
    win.blit(fpstext, (20, 400))
    win.blit(thetatext, (20, 420))
    win.blit(degreetext, (origin[0]+38, origin[1]-20))

    if currentp:
        veltext = font.render(f"Velocity : {currentp.u}m/s", True, WHITE)
        timetext = font.render(f"Time : {currentp.timeOfFlight()}s", True, WHITE)
        rangetext = font.render(f"Range : {currentp.getRange()}m", True, WHITE)
        heighttext = font.render(f"Max Height : {currentp.getMaxHeight()}m", True, WHITE)
        win.blit(veltext, (WIDTH-150, 400))
        win.blit(timetext, (WIDTH-150, 420))
        win.blit(rangetext, (WIDTH-150, 440))
        win.blit(heighttext, (WIDTH-150, 460))

    pygame.draw.rect(win, (0,0,0), (0, 0, WIDTH, HEIGHT), 5)
    clock.tick(FPS)
    pygame.display.update()
            
pygame.quit()