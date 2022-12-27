import pygame

# Initialize pygame
pygame.init()

# Set screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set title
pygame.display.set_caption('Locomotive Game')

# Load locomotive image
locomotive_img = pygame.image.load('/Users/potosacho/Desktop/Polytechnique/3A/INF573/Projet/biscuit/assets/biscuit1.png')
locomotive_x = 0
locomotive_y = 0

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Move locomotive
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        locomotive_y -= 5
    if keys[pygame.K_DOWN]:
        locomotive_y += 5
    if keys[pygame.K_LEFT]:
        locomotive_x -= 5
    if keys[pygame.K_RIGHT]:
        locomotive_x += 5

    # Draw locomotive
    screen.blit(locomotive_img, (locomotive_x, locomotive_y))

    # Update display
    pygame.display.update()
