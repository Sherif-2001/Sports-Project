# Projectile Motion

import math
import random
import pygame

from functions import *

pygame.init()

# intialize the window height and width
SCREEN = WIDTH, HEIGHT = 800, 500

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

# define the font type 
font = pygame.font.SysFont('verdana', 15)

# start fire point
origin = [50, HEIGHT - 70]

ball = pygame.transform.scale(pygame.image.load("assets/football.png"),(25,25))

goal = pygame.transform.scale_by(pygame.image.load("assets/goal.png"),0.25)

football_pitch = pygame.transform.scale(pygame.image.load("assets/pitch.jpg"),(WIDTH,100))
bg = pygame.transform.scale(pygame.image.load("assets/bg.jpg"),(WIDTH,HEIGHT-100))

initial_velocity = 75

gravity = 9.8

 # return sprite (ball)
class Projectile(pygame.sprite.Sprite):

    def __init__(self, velocity, theta):
        super(Projectile, self).__init__()

        # initial given velocity (input)
        self.u = velocity
        
        # intial theta 
        self.theta = toRadian(abs(theta))

        # fire point
        self.x, self.y = origin
 
        self.ch = 0
        self.dx = 2
        
        self.f = self.getTrajectory()

        # horizontal distance range
        self.range = self.x + abs(self.getRange())

        self.path = []
   
    def timeOfFlight(self):
        return round((2 * self.u * math.sin(self.theta)) / gravity, 2)

# The range is a scalar quantity that represents the maximum distance covered by the projectile horizontally,
# whereas the trajectory is a vector quantity that represents the path traced by the projectile in the air, 
# including its direction and magnitude.
    def getRange(self):
        range_ = ((self.u ** 2) * 2 * math.sin(self.theta) * math.cos(self.theta)) / gravity
        return round(range_, 2)


    def getMaxHeight(self):
        h = ((self.u ** 2) * (math.sin(self.theta)) ** 2) / (2 * gravity)
        return round(h, 2)

# On the other hand, the trajectory refers to the path followed by the projectile from the moment of its launch until it hits the ground. 
# It is the curve traced by the projectile in the air, 
# taking into account its initial velocity, angle of projection, and the force of gravity.
    def getTrajectory(self):
        return round(gravity /  (2 * (self.u ** 2) * (math.cos(self.theta) ** 2)), 4)


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
        
        win.blit(ball,(self.path[-1][0] - ball.get_width()/2, self.path[-1][1] - ball.get_height()/2))

        # assign the last five small balls in same fire ball position
        for pos in self.path[:-1:5]:
            pygame.draw.circle(win, WHITE, pos, 1)

projectile_group = pygame.sprite.Group()

clicked = False
currentp = None

# intial draw theta under the line 
theta = -45

# position of the end point for the line 
end = getPosOnCircumeference(theta, origin)

mouse_pos = [origin[0] + 100,origin[1] - 100]

arct = toRadian(theta)

# draw the angle arc
arcrect = pygame.Rect(origin[0]-30, origin[1]-30, 60, 60)

running = True
while running:

    arrow_color = WHITE
    
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
                projectile = Projectile(initial_velocity, theta)
                projectile_group.add(projectile)

                # the last projectile for data 
                currentp = projectile

        if event.type == pygame.MOUSEMOTION:
            if clicked:
                mouse_pos = event.pos

                # Add constraints for the arrow movement around the origin
                if mouse_pos[0] < origin[0]:
                    mouse_pos = (origin[0],mouse_pos[1])
                if mouse_pos[1] > origin[1]:
                    mouse_pos = (mouse_pos[0],origin[1])

                # Distance from origin to the mouse position
                distance = getDistanceFromOrigin(origin,mouse_pos)

                # Max distance for the arrow
                max_arrow_distance = getDistanceFromOrigin(origin,end)

                # Change the initial velocity depending on the arrow length
                initial_velocity = round(75 * distance/ max_arrow_distance)

                # Constraint for the length of the line
                if distance > max_arrow_distance :
                    mouse_pos = end
                    initial_velocity = 75
                
                # Change color of the arrow depending on the power
                if distance < max_arrow_distance/3:
                    arrow_color = GREEN
                elif max_arrow_distance/3 < distance < 2*max_arrow_distance/3:
                    arrow_color = YELLOW
                else:
                    arrow_color = RED

                theta = getAngle(mouse_pos, origin)
                if -90 < theta <= 0:
                    end = getPosOnCircumeference(theta, origin)
                    arct = toRadian(theta)
    
    # Add the pitch and background
    win.blit(football_pitch,(0,HEIGHT-100))
    win.blit(bg,(0,0))
    
    win.blit(goal,(WIDTH - 100, origin[1] - goal.get_height()/1.3))

    win.blit(ball,(origin[0] - ball.get_width()/2, origin[1] - ball.get_height()/2))
    pygame.draw.line(win, arrow_color, origin, mouse_pos, 2)
    pygame.draw.arc(win, WHITE, arcrect, 0, -arct, 2)

    projectile_group.update()

    # Info *******************************************************************
    thetatext = font.render(f"Angle : {int(abs(theta))}", True, WHITE)
    degreetext = font.render(f"{int(abs(theta))}°", True, WHITE)
    veltext = font.render(f"Velocity : {initial_velocity}m/s", True, WHITE)
    distancetext = font.render("Distance : 0", True, WHITE)
    win.blit(thetatext, (20, 20))
    win.blit(degreetext, (origin[0]+38, origin[1]-20))
    win.blit(veltext, (20, 40))
    win.blit(distancetext, (20, 60))

    if currentp:
        timetext = font.render(f"Time : {currentp.timeOfFlight()}s", True, WHITE)
        rangetext = font.render(f"Range : {currentp.getRange()}m", True, WHITE)
        heighttext = font.render(f"Max Height : {currentp.getMaxHeight()}m", True, WHITE)
        win.blit(timetext, (WIDTH-180, 20))
        win.blit(rangetext, (WIDTH-180, 40))
        win.blit(heighttext, (WIDTH-180, 60))

    # Game Window Border    
    pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 5)
    
    clock.tick(FPS)
    pygame.display.update()
            
pygame.quit()