import pygame
import random

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
dice_board = pygame.Rect((width / 2) + 100, 150, (width - 300) / 2, (height - 200) / 2)
dice_board_saved = pygame.Rect(
    (width / 2) + 100, 150 + ((height - 200) / 2), (width - 300) / 2, (height - 200) / 2
)
btn_roll_dice = pygame.Rect((width / 2) + 100, 50, 150, 75)
dice = []


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


def get_random_dice_positions(num_dice=5):
    positions = []

    for _ in range(num_dice):
        to_close = True
        while to_close:
            coords = (
                random.randint(dice_board.left + 50, dice_board.right - 50),
                random.randint(dice_board.top + 50, dice_board.bottom - 50),
            )
            to_close = False
            for item in positions:
                if (item[0] - 45 < coords[0] < item[0] + 45) and (
                    item[1] - 45 < coords[1] < item[1] + 45
                ):
                    to_close = True
        positions.append(coords)

    return positions


def draw_dice():
    for d in dice:
        pygame.draw.rect(screen, "red", d)


# print(get_random_dice_positions(5))
while running:

    x, y = pygame.mouse.get_pos()
    screen.fill("gray25")

    pygame.draw.rect(screen, "skyblue3", table_board)
    pygame.draw.rect(screen, "skyblue3", dice_board)
    pygame.draw.rect(screen, "skyblue2", dice_board_saved)
    draw_dice()

    draw_button(btn_roll_dice, hover=False)
    if btn_roll_dice.collidepoint(x, y):
        draw_button(btn_roll_dice, hover=True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_roll_dice.collidepoint(x, y):
                positions = get_random_dice_positions()
                dice = [pygame.Rect(pos[0], pos[1], 40, 40) for pos in positions]

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
