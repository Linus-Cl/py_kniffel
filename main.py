import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 900))
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont("Sans", 20)

table_board = pygame.Rect(50, 50, (width / 2) + 50 / 2, height - 100)
dice_board = pygame.Rect(
    (width / 2) + 100,
    150,
    (width - 300) / 2,
    height - 200,
)
btn_roll_dice = pygame.Rect((width / 2) + 100, 50, 150, 75)


def draw_button(format, hover):
    if hover:
        pygame.draw.rect(screen, "skyblue2", format)
        text = font.render("Roll Dice", True, "white")
        text_rec = text.get_rect(center=(format.center))
        screen.blit(text, text_rec)
    else:
        pygame.draw.rect(screen, "skyblue3", format)
        text = font.render("Roll Dice", True, "white")
        text_rec = text.get_rect(center=(format.center))
        screen.blit(text, text_rec)


while running:

    x, y = pygame.mouse.get_pos()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray25")

    pygame.draw.rect(screen, "skyblue3", table_board)
    pygame.draw.rect(screen, "skyblue3", dice_board)

    draw_button(btn_roll_dice, hover=False)
    if btn_roll_dice.collidepoint(x, y):
        draw_button(btn_roll_dice, hover=True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_roll_dice.collidepoint(x, y):
                print("button pressed!")

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
