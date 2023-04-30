import math
import pygame
from functions import *

pygame.init()

# intialize the window with height and width
SCREEN = WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

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

# ------------------------------- Projectile Class ---------------------------------- #
class Projectile(pygame.sprite.Sprite):

    def __init__(self, velocity, theta):
        super(Projectile, self).__init__()

        # initial given velocity (input)
        self.initial_velocity = velocity
        
        # intial theta 
        self.firing_angle = toRadian(abs(theta))

        # fire point
        self.pos_x, self.pos_y = origin
 
        self.ch = 0
        self.dx = 2
        
        self.f = self.getTrajectory()

        # horizontal distance range
        self.range = self.pos_x + abs(self.getRange())

        self.path = []
   
    def timeOfFlight(self):
        return round((2 * self.initial_velocity * math.sin(self.firing_angle)) / gravity, 2)


    def getRange(self):
        """
        The maximum distance covered by the projectile horizontally
        """
        range_ = ((self.initial_velocity ** 2) * 2 * math.sin(self.firing_angle) * math.cos(self.firing_angle)) / gravity
        return round(range_, 2)


    def getMaxHeight(self):
        h = ((self.initial_velocity ** 2) * (math.sin(self.firing_angle)) ** 2) / (2 * gravity)
        return round(h, 2)

    def getTrajectory(self):
        """
        The path followed by the projectile from the moment of its launch until it hits the ground.
        It is the curve traced by the projectile in the air, taking into account its 
        initial velocity, angle of projection, and the force of gravity.
        """
        return round(gravity /  (2 * (self.initial_velocity ** 2) * (math.cos(self.firing_angle) ** 2)), 4)


    def getProjectilePos(self, x):
        return x * math.tan(self.firing_angle) - self.f * x ** 2

    def update(self):
        if self.pos_x >= self.range:
            # stop ball
            self.dx = 0

        self.pos_x += self.dx

        # vertical according to horizontal position
        self.ch = self.getProjectilePos(self.pos_x - origin[0])

        # the height of the ball from bottom
        self.path.append((self.pos_x, self.pos_y-abs(self.ch)))

        #it takes the last 50 elements of self.path and assigns them.
        self.path = self.path[-50:]
        
        window.blit(ball,(self.path[-1][0] - ball.get_width()/2, self.path[-1][1] - ball.get_height()/2))

        # assign the last five small balls in same fire ball position
        for pos in self.path[:-1:5]:
            pygame.draw.circle(window, WHITE, pos, 1)

projectile_group = pygame.sprite.Group()

clicked = False
current_projectile = None

# initial theta under the line 
theta = -45

arrow_color = WHITE

# position of the end point for the line 
end = getPosOnCircumeference(theta, origin)

mouse_pos = [origin[0] + 100,origin[1] - 100]

arct = toRadian(theta)

# draw the angle arc
arcrect = pygame.Rect(origin[0]-30, origin[1]-30, 60, 60)

running = True

# ------------------------------- Game Loop ---------------------------------- #
while running:
    
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
                current_projectile = None

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
                current_projectile = projectile

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
    
    # Pitch and background
    window.blit(football_pitch,(0,HEIGHT-100))
    window.blit(bg,(0,0))
    
    # Goal
    window.blit(goal,(WIDTH - 100, origin[1] - goal.get_height()/1.3))

    # Football
    window.blit(ball,(origin[0] - ball.get_width()/2, origin[1] - ball.get_height()/2))
    
    # Firing Arrow
    pygame.draw.line(window, arrow_color, origin, mouse_pos, 2)

    # Firing Angle
    pygame.draw.arc(window, WHITE, arcrect, 0, -arct, 2)

    # Game Window Border    
    pygame.draw.rect(window, BLACK, (0, 0, WIDTH, HEIGHT), 5)

    projectile_group.update()

# ------------------------------- Parameters Text ---------------------------------- #
    angle_text = font.render(f"Angle : {int(abs(theta))}", True, WHITE)
    velocity_text = font.render(f"Velocity : {initial_velocity}m/s", True, WHITE)
    distance_text = font.render("Distance : 0", True, WHITE)
    window.blit(angle_text, (20, 20))
    window.blit(velocity_text, (20, 40))
    window.blit(distance_text, (20, 60))

    # Angle text at the line
    angle_line_text = font.render(f"{int(abs(theta))}°", True, WHITE)
    window.blit(angle_line_text, (origin[0]+38, origin[1]-20))

    if current_projectile:
        time_of_flight_text = font.render(f"Time : {current_projectile.timeOfFlight()} s", True, WHITE)
        range_text = font.render(f"Range : {current_projectile.getRange()} m", True, WHITE)
        max_height_text = font.render(f"Max Height : {current_projectile.getMaxHeight()} m", True, WHITE)
        window.blit(time_of_flight_text, (WIDTH-180, 20))
        window.blit(range_text, (WIDTH-180, 40))
        window.blit(max_height_text, (WIDTH-180, 60))
    
    clock.tick(FPS)
    pygame.display.update()
            
pygame.quit()