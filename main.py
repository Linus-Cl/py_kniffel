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
    "Gesamt Unten",
    "Gesamt Oben",
    "Gesamt",
]
list_background = pygame.Rect(106, 110, 514, 728)

cols = [[] for i in range(5)]
left_values_list = [108, 212, 314, 416, 518]

for i, text in enumerate(list_button_texts):
    for list, left_val in zip(cols, left_values_list):
        list.append(
            Button(
                pygame.Rect(left_val, 110 + i * 40 + (2 if i < 8 else 8), 100, 38),
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


def count_appearances(lst):
    counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for item in lst:
        counts[item] += 1
    return counts


def eval_points():
    used_dice = [d for d in dice_list if d.frozen]
    dice_values = [d.value for d in used_dice]
    value_counts = count_appearances(dice_values)
    possible_values = [0 for _ in range(18)]
    for i in range(6):
        possible_values[i] = value_counts[i + 1] * (i + 1)

    max_count_item = max(value_counts, key=value_counts.get)

    # dreierpasch
    if value_counts[max_count_item] >= 3:
        val = 0
        for item in value_counts.items():
            val += item[0] * item[1]
        possible_values[8] = val

    # viererpasch
    if value_counts[max_count_item] >= 4:
        val = 0
        for item in value_counts.items():
            val += item[0] * item[1]
        possible_values[9] = val

    # full-house
    for item in value_counts.keys():
        if item != max_count_item and value_counts[item] == 2:
            possible_values[10] = 25

    # kleine-strasse
    if (
        (
            value_counts[1] >= 1
            and value_counts[2] >= 1
            and value_counts[3] >= 1
            and value_counts[4] >= 1
        )
        or (
            value_counts[2] >= 1
            and value_counts[3] >= 1
            and value_counts[4] >= 1
            and value_counts[5] >= 1
        )
        or (
            value_counts[3] >= 1
            and value_counts[4] >= 1
            and value_counts[5] >= 1
            and value_counts[6] >= 1
        )
    ):
        possible_values[11] = 30

    # grosse-strasse
    if (
        value_counts[1] == 1
        and value_counts[2] == 1
        and value_counts[3] == 1
        and value_counts[4] == 1
        and value_counts[5] == 1
    ) or (
        value_counts[2] == 1
        and value_counts[3] == 1
        and value_counts[4] == 1
        and value_counts[5] == 1
        and value_counts[6] == 1
    ):
        possible_values[12] = 40

    # kniffel
    if value_counts[max_count_item] == 5:
        possible_values[13] = 50

    print(possible_values)


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

    for col in cols:
        for b in col:
            pygame.draw.rect(screen, "skyblue1", b)

    draw_dice()

    for list_btn in cols[0]:
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
                eval_points()
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
