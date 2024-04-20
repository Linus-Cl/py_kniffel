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

dice_img_one = pygame.image.load("images/dice_one.png")
dice_img_two = pygame.image.load("images/dice_two.png")
dice_img_three = pygame.image.load("images/dice_three.png")
dice_img_four = pygame.image.load("images/dice_four.png")
dice_img_five = pygame.image.load("images/dice_five.png")
dice_img_six = pygame.image.load("images/dice_six.png")

dice_images = [
    (dice_img_one, 1),
    (dice_img_two, 2),
    (dice_img_three, 3),
    (dice_img_four, 4),
    (dice_img_five, 5),
    (dice_img_six, 6),
]

table_board = pygame.Rect(50, 50, (width / 2) + 50 / 2, height - 100)
dice_board = pygame.Rect((width / 2) + 100, 150, (width - 300) / 2, (height - 200) / 2)
dice_board_saved = pygame.Rect(
    (width / 2) + 100, 150 + ((height - 200) / 2), (width - 300) / 2, (height - 200) / 2
)
btn_roll_dice = pygame.Rect((width / 2) + 100, 50, 150, 75)
dice = []
dice_states = []


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


def roll_dice():
    states = []
    for _ in dice:
        num = random.randint(1, 6)
        img = dice_img_one
        for pair in dice_images:
            if pair[1] == num:
                img = pair[0]

        states.append(img)

    return states


def draw_dice():
    for d, img in zip(dice, dice_states):
        pygame.draw.rect(screen, "red", d)
        screen.blit(img, d)


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
                dice_states = roll_dice()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
