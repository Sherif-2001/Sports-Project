import pygame


pygame.font.init()


# Constants
FPS = 60
WIDTH,HEIGHT = 800,400
FONT = pygame.font.SysFont("comicsans",30)

# Game Window
WIN = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Projectiles Test")

# Backgrounds
BG2 = pygame.transform.scale(pygame.image.load("assets/pitch.jpg"),(WIDTH,80))
BG = pygame.transform.scale(pygame.image.load("assets/bg.jpg"),(WIDTH,HEIGHT-BG2.get_height()))


def draw(ball,goal):
    """
    Draw objects to the game window
    """
    # Draw the backgrounds to the window
    WIN.blit(BG,(0,0))
    WIN.blit(BG2,(0,HEIGHT-BG2.get_height()))

    # Draw the goal to the window
    WIN.blit(goal,(WIDTH - goal.get_width(), HEIGHT - goal.get_height() - 40))
    WIN.blit(ball,(WIDTH/2, HEIGHT - ball.get_height() - 40))

    # Update the Screen
    pygame.display.update()

def main():
    """
    Main function to start the game
    """
    run = True
    
    # Game parameters
    clock = pygame.time.Clock()
    goal = pygame.transform.scale_by(pygame.image.load("assets/goal.png"),0.25)
    ball = pygame.transform.scale_by(pygame.image.load("assets/football.png"),0.05)
    
    while run:
        # Check events of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        draw(ball,goal)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()