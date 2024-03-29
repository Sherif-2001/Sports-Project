import math
from time import sleep
import pygame
import numpy as np
from functions import *

pygame.font.init()
pygame.mixer.init()

# ------------------------------- Constants ---------------------------------- #

# intialize the window with height and width
SCREEN = WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

# Assign the real clock for the game with frames per second
CLOCK = pygame.time.Clock()
FPS = 60

GRAVITY = 9.8

# Define used colors
BLACK = (18, 18, 18)
WHITE = (217, 217, 217)
RED = (252, 91, 122)
GREEN = (29, 161, 16)
BLUE = (78, 193, 246)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)

# Define the font type 
FONT = pygame.font.SysFont('verdana', 15)
Goal_font = pygame.font.SysFont('verdana', 70)

ball_image = pygame.transform.scale(pygame.image.load("assets/images/football.png"),(25,25))
goal_image = pygame.transform.scale_by(pygame.image.load("assets/images/goal2.png"),0.25)
pitch_image = pygame.transform.scale(pygame.image.load("assets/images/pitch.jpg"),(WIDTH-10,100))
bg = pygame.transform.scale(pygame.image.load("assets/images/bg.jpg"),(WIDTH,HEIGHT-100))

whistle_sfx = pygame.mixer.Sound("assets/audio/whistle.mp3")
ball_kick_sfx = pygame.mixer.Sound("assets/audio/ball_kick.mp3")
goal_sfx = pygame.mixer.Sound("assets/audio/goal.mp3")
bg_music = pygame.mixer.Sound("assets/audio/bg_music.mp3")
bg_music.play(-1)
# ------------------------------- Variables ---------------------------------- #

# Starting fire point
origin = [50, HEIGHT - 70]

# the total width is 800 pixel which corresponds to 100 meter from start to end
# so each pixel corresponds to 1/8 meter

initial_velocity = 75

ball_rect = ball_image.get_rect()

goal_rect = goal_image.get_rect()
goal_rect.bottomleft = (WIDTH-100,origin[1] + ball_rect.centery)

border_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

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
 
        self.height_at_position = 0
        self.flying_velocity_x = 2
        
        # horizontal distance range
        self.range = self.pos_x + abs(self.getRange())

        # Height at goal
        self.height_at_goal = 0

        self.path = []
   
    def getTimeOfFlight(self):
        return round((2 * self.initial_velocity * math.sin(self.firing_angle)) / GRAVITY, 2)

    def getRange(self):
        """
        The maximum distance covered by the projectile horizontally
        """
        range_ = ((self.initial_velocity ** 2) * 2 * math.sin(self.firing_angle) * math.cos(self.firing_angle)) / GRAVITY
        return round(range_, 2)

    def getMaxHeight(self):
        h = ((self.initial_velocity ** 2) * (math.sin(self.firing_angle)) ** 2) / (2 * GRAVITY)
        return round(h, 2)

    def getTrajectory(self):
        """
        The path followed by the projectile from the moment of its launch until it hits the ground.
        It is the curve traced by the projectile in the air, taking into account its 
        initial velocity, angle of projection, and the force of gravity.
        """
        return round(GRAVITY /  (2 * (self.initial_velocity ** 2) * (math.cos(self.firing_angle) ** 2)), 4)


    def getProjectilePos(self, x):
        return x * math.tan(self.firing_angle) - self.getTrajectory() * x ** 2

    def entered_goal(self):
            # Sound effects
            whistle_sfx.play()
            goal_sfx.play()

            self.flying_velocity_x = 0
            self.height_at_goal = self.getProjectilePos(self.pos_x - origin[0])

            # Add the goal text
            win_text = Goal_font.render("GOAL", True, WHITE)
            time_of_flight_text = FONT.render(f"Time : {current_projectile.getTimeOfFlight()} s", True, WHITE)
            range_text = FONT.render(f"Range : {round(current_projectile.getRange() *(1/8), 2)} m", True, WHITE)
            max_height_text = FONT.render(f"Max Height : {round(current_projectile.getMaxHeight()/46.4,2)} m", True, WHITE)
            height_at_goal_text = FONT.render(f"Height : {round(current_projectile.height_at_goal/46.4,2)} m", True, WHITE)

            WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2,HEIGHT/2 - win_text.get_height()/2))
            WIN.blit(time_of_flight_text, (WIDTH/2 - time_of_flight_text.get_width()/2, 20))
            WIN.blit(range_text, (WIDTH/2 - range_text.get_width()/2, 40))
            WIN.blit(max_height_text, (WIDTH/2 - max_height_text.get_width()/2, 60))
            WIN.blit(height_at_goal_text, (WIDTH/2 - height_at_goal_text.get_width()/2, 80))
             
            pygame.display.update()
            pygame.time.delay(3000)
            projectiles_group.empty()

    def update(self):
        
        # stop ball
        if self.pos_x >= self.range:
            self.flying_velocity_x = 0

        self.pos_x += self.flying_velocity_x

        # vertical according to horizontal position
        self.height_at_position = self.getProjectilePos(self.pos_x - origin[0])

        # add a position of the ball to the path
        self.path.append((self.pos_x, self.pos_y-abs(self.height_at_position)))

        # take the last 50 elements of self.path.
        self.path = self.path[-50:]
        
        # Draw moving ball
        moving_ball_rect = ball_image.get_rect()
        moving_ball_rect.center = self.path[-1]
        WIN.blit(ball_image, moving_ball_rect)

        if moving_ball_rect.colliderect(goal_rect):
            if moving_ball_rect.y >= goal_rect.y:
                self.entered_goal()
            else:
                self.flying_velocity_x = 0

        # assign the last five small balls in same fire ball position
        for pos in self.path[:-1:5]:
            pygame.draw.circle(WIN, WHITE, pos, 2)

# ------------------------------- Initial Values ---------------------------------- #
current_projectile = None

projectiles_group = pygame.sprite.Group()

# initial theta under the line 
theta = 45

arrow_color = WHITE

# line end point position
line_end_pos = getLineEndPos(theta, origin)

arc_angle = toRadian(theta)

mouse_pos = np.add(origin,[100,-100])

mouse_clicked = False

move_ball_left, move_ball_right = False,False

distance_from_goal = getDistanceFromOrigin(origin, (WIDTH - 100,origin[1]))

# ------------------------------- Input Functions ---------------------------------- #

def kick_ball():
    global current_projectile
    if not current_projectile or current_projectile.flying_velocity_x == 0:
        if 0 < theta < 90:
            ball_kick_sfx.play()
            projectiles_group.empty()
            new_projectile = Projectile(initial_velocity, theta)
            projectiles_group.add(new_projectile)
            current_projectile = new_projectile

def change_arrow_parameters():
        global mouse_pos
        global initial_velocity
        global arrow_color
        global line_end_pos
        global arc_angle
        global theta

        mouse_pos = [event.pos[0],event.pos[1]]

        # Add constraints for the arrow movement around the origin
        if mouse_pos[0] < origin[0]:
            mouse_pos[0] = origin[0]
        if mouse_pos[1] > origin[1]:
            mouse_pos[1] = origin[1]

        # Distance from origin to the mouse position
        # * 0.0002645833
        distance = getDistanceFromOrigin(origin, mouse_pos) 

        # Max distance for the arrow
        max_arrow_distance = getDistanceFromOrigin(origin, line_end_pos)

        # Change the initial velocity depending on the arrow length
        initial_velocity = round(75 * distance / max_arrow_distance)

        # Constraint for the length of the line
        if distance > max_arrow_distance :
            mouse_pos = line_end_pos
            initial_velocity = 75
            
        # Change color of the arrow depending on the power
        if distance < max_arrow_distance / 3:
            arrow_color = GREEN
        elif max_arrow_distance / 3 < distance < 2 * max_arrow_distance / 3:
            arrow_color = YELLOW
        else:
            arrow_color = RED
        
        theta = getAngle(mouse_pos, origin)
        if 0 < theta < 90:
            line_end_pos = getLineEndPos(theta, origin)
            arc_angle = toRadian(theta)

def change_distance_from_goal():
    global distance_from_goal

    if not current_projectile or current_projectile.flying_velocity_x == 0:
        if move_ball_right and origin[0] < WIDTH - 300:
            projectiles_group.empty()
            origin[0] += 3
            mouse_pos[0] += 3
            distance_from_goal = getDistanceFromOrigin((origin[0],0), (goal_rect.left,0))

        if move_ball_left and origin[0] >= 50:
            projectiles_group.empty()
            origin[0] -= 3
            mouse_pos[0] -= 3
            distance_from_goal = getDistanceFromOrigin((origin[0],0), (goal_rect.left,0))

def draw_objects():
    # Pitch and background
    WIN.blit(pitch_image,(0,HEIGHT-100))
    WIN.blit(bg,(0,0))
    
    # Goal
    WIN.blit(goal_image, goal_rect)

    # Football at origin
    ball_rect.center = origin
    if not current_projectile or current_projectile.flying_velocity_x == 0:
        WIN.blit(ball_image, ball_rect)
    
    # Firing Arrow
    pygame.draw.line(WIN, arrow_color, origin, mouse_pos, 3)

    # Draw the angle arc
    arc_rect = pygame.Rect(origin[0]-30, origin[1]-30, 60, 60)
    pygame.draw.arc(WIN, arrow_color, arc_rect, 0, arc_angle, 3)

    # Game Window Border    
    pygame.draw.rect(WIN, WHITE, border_rect, 3)

    projectiles_group.update()

# ------------------------------- Game Loop ---------------------------------- #
game_running = True
while game_running:
    
    for event in pygame.event.get():

        # close game / stop running 
        if event.type == pygame.QUIT:
            game_running = False
            
         # close game with escape or q (key)   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                game_running = False

            # remove the drawn balls 
            if event.key == pygame.K_r:
                projectiles_group.empty()
                current_projectile = None

            # Move the ball to the right
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_ball_left, move_ball_right = False, True

            # Move the ball to the left
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_ball_left, move_ball_right = True, False
            
        if event.type == pygame.KEYUP:
            move_ball_left, move_ball_right = False, False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_clicked = False
            kick_ball()
            
        if event.type == pygame.MOUSEMOTION and mouse_clicked:
            change_arrow_parameters()

    change_distance_from_goal()
    draw_objects()
    # *0.0002645833
    # pitch length is 110 meter
    
# ------------------------------- Parameters Text ---------------------------------- #
    angle_text = FONT.render(f"Angle : {int(abs(theta))}", True, WHITE)
    velocity_text = FONT.render(f"Velocity : {round(initial_velocity * (0.4),2) } m/sec", True, WHITE)
    distance_text = FONT.render(f"Distance : {round(distance_from_goal *(1/8),2)} m", True, WHITE)
    WIN.blit(angle_text, (20, 20))
    WIN.blit(velocity_text, (20, 40))
    WIN.blit(distance_text, (20, 60))

    # Angle text at the line
    arrow_angle_text = FONT.render(f"{int(abs(theta))}°", True, WHITE)
    WIN.blit(arrow_angle_text, (origin[0]+38, origin[1]-20))

    # * 0.0002645833
    if current_projectile:
        time_of_flight_text = FONT.render(f"Time : {current_projectile.getTimeOfFlight()} s", True, WHITE)
        range_text = FONT.render(f"Range : {round(current_projectile.getRange() *(1/8),2) } m", True, WHITE)
        max_height_text = FONT.render(f"Max Height : {round(current_projectile.getMaxHeight() / 46.4,2)} m", True, WHITE)
        # height_at_goal_text = FONT.render(f"Height : {round(current_projectile.height_at_goal,2)} m", True, WHITE)
        WIN.blit(time_of_flight_text, (WIDTH-180, 20))
        WIN.blit(range_text, (WIDTH-180, 40))
        WIN.blit(max_height_text, (WIDTH-180, 60))
        # WIN.blit(height_at_goal_text, (WIDTH-180, 80))
    
    CLOCK.tick(FPS)
    pygame.display.update()
            
pygame.quit()