import pygame
import random
import dice
import Player
from Button import Button

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 900))
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
running = True
dt = 0
main_font = pygame.font.SysFont("Sans", 20)
list_font = pygame.font.SysFont("Sans", 16)

dice_list = [dice.Dice(i, 0, 0) for i in range(5)]
table_board = pygame.Rect(50, 50, (width / 2) + 50 / 2, height - 100)
dice_board = pygame.Rect((width / 2) + 100, 150, (width - 300) / 2, (height - 200) / 2)
dice_board_saved = pygame.Rect(
    (width / 2) + 100, 150 + ((height - 200) / 2), (width - 300) / 2, (height - 200) / 2
)
saved_dice_positions = [
    [dice_board_saved.left + 155, dice_board_saved.top + 105, False],
    [dice_board_saved.left + 225, dice_board_saved.top + 105, False],
    [dice_board_saved.left + 295, dice_board_saved.top + 105, False],
    [dice_board_saved.left + 190, dice_board_saved.top + 245, False],
    [dice_board_saved.left + 270, dice_board_saved.top + 245, False],
]
btn_roll_dice = Button(
    pygame.Rect((width / 2) + 100, 50, 150, 75),
    "Roll Dice",
    "skyblue3",
    "skyblue2",
    main_font,
)
btn_finish_turn = Button(
    pygame.Rect((width / 2) + 275, 50, 150, 75),
    "Finish Turn",
    "skyblue3",
    "skyblue2",
    main_font,
)

list_button_texts = [
    "1er",
    "2er",
    "3er",
    "4er",
    "5er",
    "6er",
    "Gesamt",
    "Bonus?",
    "Dreierpasch",
    "Viererpasch",
    "Full House",
    "Kleine Straße",
    "Große Straße",
    "Kniffel",
    "Chance",
    "gesamt unten",
    "gesamt oben",
    "gesamt",
]
list_background = pygame.Rect(106, 110, 514, 728)
list_buttons2 = [
    Button(
        pygame.Rect(108, 110 + i * 40 + 2, 100, 38),
        text,
        "skyblue1",
        "skyblue3",
        list_font,
    )
    for i, text in zip(range(18), list_button_texts)
]

list_buttons = []
list_col_1 = []
list_col_2 = []
list_col_3 = []
list_col_4 = []
cols = [list_buttons, list_col_1, list_col_2, list_col_3, list_col_4]
left_values_list = [108, 212, 314, 416, 518]

for i, text in zip(range(18), list_button_texts):
    for list, left_val in zip(cols, left_values_list):
        if i < 8:
            list.append(
                Button(
                    pygame.Rect(left_val, 110 + i * 40 + 2, 100, 38),
                    text,
                    "skyblue1",
                    "skyblue3",
                    list_font,
                )
            )
        else:
            list.append(
                Button(
                    pygame.Rect(left_val, 110 + i * 40 + 8, 100, 38),
                    text,
                    "skyblue1",
                    "skyblue3",
                    list_font,
                )
            )


def draw_button(button: Button):
    color = button.color
    if button.hover:
        color = button.hover_color
    if button.disabled:
        color = button.disabled_color

    pygame.draw.rect(screen, color, button.rect)
    text = button.font.render(button.text, True, "white")
    text_rec = text.get_rect(center=(button.rect.center))
    screen.blit(text, text_rec)


# returns 5 positions that do not interfere
def get_random_dice_positions(num_dice=5):
    frozen_positions = [(d.x, d.y) for d in dice_list if d.frozen]
    positions = []

    for _ in range(num_dice):
        to_close = True
        while to_close:
            coords = (
                random.randint(dice_board.left + 50, dice_board.right - 50),
                random.randint(dice_board.top + 50, dice_board.bottom - 50),
            )
            to_close = False
            for item in frozen_positions:
                if (item[0] - 45 < coords[0] < item[0] + 45) and (
                    item[1] - 45 < coords[1] < item[1] + 45
                ):
                    to_close = True
        frozen_positions.append(coords)
        positions.append(coords)

    return positions


def get_free_freeze_position():
    for pos in saved_dice_positions:
        if not pos[2]:
            pos[2] = True
            return (pos[0], pos[1])


def roll_dice():
    for d in dice_list:
        d.roll()


def draw_dice():
    for d in dice_list:
        pygame.draw.rect(screen, "gray25", d.rect)
        screen.blit(d.image, d.rect)


def start_screen(screen):
    text = main_font.render("Select number of players: 1, 2, or 3", True, "white")
    text_rect = text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2)
    )
    screen.blit(text, text_rect)
    pygame.display.flip()

    num_players = None
    while num_players is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    num_players = 1
                elif event.key == pygame.K_2:
                    num_players = 2
                elif event.key == pygame.K_3:
                    num_players = 3
    return num_players


num_players = start_screen(screen)
players = [Player.Player(i) for i in range(num_players)]
current_player = players[0]
switch_player_flag = False
attempt_counter = 3


# game loop
while running:

    if switch_player_flag:
        current_player = players[(current_player.id + 1) % len(players)]
        switch_player_flag = False
        attempt_counter = 3
        print(current_player.id)
        btn_roll_dice.disabled = False

    btn_roll_dice.hover = False
    btn_finish_turn.hover = False
    x, y = pygame.mouse.get_pos()
    screen.fill("gray25")

    pygame.draw.rect(screen, "skyblue3", table_board)
    pygame.draw.rect(screen, "skyblue3", dice_board)
    pygame.draw.rect(screen, "skyblue2", dice_board_saved)
    pygame.draw.rect(screen, "white", list_background)

    for col1, col2, col3, col4 in zip(list_col_1, list_col_2, list_col_3, list_col_4):
        # draw_button(list_btn)
        pygame.draw.rect(screen, "skyblue1", col1)
        pygame.draw.rect(screen, "skyblue1", col2)
        pygame.draw.rect(screen, "skyblue1", col3)
        pygame.draw.rect(screen, "skyblue1", col4)

    draw_dice()

    for list_btn in list_buttons:
        list_btn.hover = False
        if list_btn.rect.collidepoint(x, y):
            list_btn.hover = True
        draw_button(list_btn)

    if btn_roll_dice.rect.collidepoint(x, y):
        btn_roll_dice.hover = True
    draw_button(btn_roll_dice)

    if btn_finish_turn.rect.collidepoint(x, y):
        btn_finish_turn.hover = True
    draw_button(btn_finish_turn)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_roll_dice.rect.collidepoint(x, y):
                if attempt_counter > 1:
                    roll_dice()
                    attempt_counter -= 1
                    positions = get_random_dice_positions()
                    for d, coords in zip(dice_list, positions):
                        d.change_position(coords[0], coords[1])
                elif attempt_counter == 1:
                    roll_dice()
                    attempt_counter -= 1
                    positions = get_random_dice_positions()
                    for d, coords in zip(dice_list, positions):
                        d.change_position(coords[0], coords[1])
                    btn_roll_dice.disabled = True

            if btn_finish_turn.rect.collidepoint(x, y):
                switch_player_flag = True
                for d in dice_list:
                    d.reset()

            for d in dice_list:
                if d.rect.collidepoint(x, y):
                    if not d.frozen:
                        freeze_pos = get_free_freeze_position()
                        d.freeze(*freeze_pos)
                    elif d.frozen:
                        d.frozen = False
                        for pos in saved_dice_positions:
                            if pos[0] == d.rect.x and pos[1] == d.rect.y:
                                pos[2] = False
                        d.change_position(d.x, d.y)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
