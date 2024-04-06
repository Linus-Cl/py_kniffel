import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
running = True
dt = 0

table_board = pygame.Rect(
    50, 50, (screen.get_width() / 2) + 50 / 2, screen.get_height() - 100
)
dice_board = pygame.Rect(
    (screen.get_width() / 2) + 100,
    150,
    (screen.get_width() - 300) / 2,
    screen.get_height() - 200,
)
btn_roll_dice = pygame.Rect((screen.get_width() / 2) + 100, 50, 150, 75)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray25")

    pygame.draw.rect(screen, "skyblue3", table_board)
    pygame.draw.rect(screen, "skyblue3", dice_board)
    pygame.draw.rect(screen, "skyblue3", btn_roll_dice)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
