import math
import pygame
from functions import *

pygame.init()

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

ball_image = pygame.transform.scale(pygame.image.load("assets/football.png"),(25,25))
goal_image = pygame.transform.scale_by(pygame.image.load("assets/goal.png"),0.25)
pitch_image = pygame.transform.scale(pygame.image.load("assets/pitch.jpg"),(WIDTH,100))
bg = pygame.transform.scale(pygame.image.load("assets/bg.jpg"),(WIDTH,HEIGHT-100))

# ------------------------------- Variables ---------------------------------- #

# Starting fire point
origin = [50, HEIGHT - 70]

initial_velocity = 75


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
        
        # Add a ball at the origin
        WIN.blit(ball_image,(self.path[-1][0] - ball_image.get_width()/2, self.path[-1][1] - ball_image.get_height()/2))

        # assign the last five small balls in same fire ball position
        for pos in self.path[:-1:5]:
            pygame.draw.circle(WIN, WHITE, pos, 2)

current_projectile = None

projectiles_group = pygame.sprite.Group()

# initial theta under the line 
theta = 45

arrow_color = WHITE

# position of the end point for the line 
line_end_pos = getPosOnCircumeference(theta, origin)

arc_angle = toRadian(theta)

mouse_pos = [origin[0] + 100,origin[1] - 100]

mouse_clicked = False

move_ball_right = False

move_ball_left = False

distance_from_goal = getDistanceFromOrigin(origin, (WIDTH - 100,origin[1]))

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
                move_ball_right = True
                move_ball_left = False

            # Move the ball to the left
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_ball_right = False
                move_ball_left = True
            
        if event.type == pygame.KEYUP:
                move_ball_right = False
                move_ball_left = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_clicked = False

           # mouse up position
            mouse_up_pos = event.pos

            # theta = getAngle(mouse_up_pos, origin)
            if 0 <= theta < 90:
                new_projectile = Projectile(initial_velocity, theta)
                projectiles_group.add(new_projectile)
                current_projectile = new_projectile

        if event.type == pygame.MOUSEMOTION:
            if mouse_clicked:
                mouse_pos = event.pos

                # Add constraints for the arrow movement around the origin
                if mouse_pos[0] < origin[0]:
                    mouse_pos = (origin[0], mouse_pos[1])
                if mouse_pos[1] > origin[1]:
                    mouse_pos = (mouse_pos[0], origin[1])

                # Distance from origin to the mouse position
                distance = getDistanceFromOrigin(origin, mouse_pos)

                # Max distance for the arrow
                max_arrow_distance = getDistanceFromOrigin(origin, line_end_pos)

                # Change the initial velocity depending on the arrow length
                initial_velocity = round(75 * distance / max_arrow_distance)

                # Constraint for the length of the line
                if distance > max_arrow_distance :
                    mouse_pos = line_end_pos
                    initial_velocity = 75
                    
                # Change color of the arrow depending on the power (NEVEEN TOUCH)
                if distance < max_arrow_distance / 3:
                    arrow_color = GREEN
                elif max_arrow_distance / 3 < distance < 2 * max_arrow_distance / 3:
                    arrow_color = YELLOW
                else:
                    arrow_color = RED
                
                theta = getAngle(mouse_pos, origin)
                if 0 <= theta < 90:
                    line_end_pos = getPosOnCircumeference(theta, origin)
                    arc_angle = toRadian(theta)

    # Move ball (origin) left and right
    if move_ball_right and origin[0] < WIDTH - 300:
        origin[0] += 5
        distance_from_goal = getDistanceFromOrigin(origin, (WIDTH - 100,origin[1]))

    if move_ball_left and origin[0] >= 50 :
        origin[0] -= 5
        distance_from_goal = getDistanceFromOrigin(origin, (WIDTH - 100,origin[1]))

    # Pitch and background
    WIN.blit(pitch_image,(0,HEIGHT-100))
    WIN.blit(bg,(0,0))
    
    # Goal
    WIN.blit(goal_image,(WIDTH - 100, origin[1] - goal_image.get_height()/1.3))

    # Football
    WIN.blit(ball_image,(origin[0] - ball_image.get_width()/2, origin[1] - ball_image.get_height()/2))
    
    # Firing Arrow
    pygame.draw.line(WIN, arrow_color, origin, mouse_pos, 3)

    # Draw the angle arc
    arc_rect = pygame.Rect(origin[0]-30, origin[1]-30, 60, 60)
    pygame.draw.arc(WIN, arrow_color, arc_rect, 0, arc_angle, 3)

    # Game Window Border    
    pygame.draw.rect(WIN, WHITE, (0, 0, WIDTH, HEIGHT), 5)

    projectiles_group.update()

# ------------------------------- Parameters Text ---------------------------------- #
    angle_text = FONT.render(f"Angle : {int(abs(theta))}", True, WHITE)
    velocity_text = FONT.render(f"Velocity : {initial_velocity} m/sec", True, WHITE)
    distance_text = FONT.render(f"Distance : {distance_from_goal} m", True, WHITE)
    WIN.blit(angle_text, (20, 20))
    WIN.blit(velocity_text, (20, 40))
    WIN.blit(distance_text, (20, 60))

    # Angle text at the line
    arrow_angle_text = FONT.render(f"{int(abs(theta))}°", True, WHITE)
    WIN.blit(arrow_angle_text, (origin[0]+38, origin[1]-20))

    if current_projectile:
        time_of_flight_text = FONT.render(f"Time : {current_projectile.getTimeOfFlight()} s", True, WHITE)
        range_text = FONT.render(f"Range : {current_projectile.getRange()} m", True, WHITE)
        max_height_text = FONT.render(f"Max Height : {current_projectile.getMaxHeight()} m", True, WHITE)
        WIN.blit(time_of_flight_text, (WIDTH-180, 20))
        WIN.blit(range_text, (WIDTH-180, 40))
        WIN.blit(max_height_text, (WIDTH-180, 60))
    
    CLOCK.tick(FPS)
    pygame.display.update()
            
pygame.quit()