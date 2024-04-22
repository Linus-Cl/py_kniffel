import pygame
import random

dice_img_one = pygame.image.load("images/dice_one.png")
dice_img_two = pygame.image.load("images/dice_two.png")
dice_img_three = pygame.image.load("images/dice_three.png")
dice_img_four = pygame.image.load("images/dice_four.png")
dice_img_five = pygame.image.load("images/dice_five.png")
dice_img_six = pygame.image.load("images/dice_six.png")
dice_empty = pygame.image.load("images/empty.png")

dice_images = [
    (dice_img_one, 1),
    (dice_img_two, 2),
    (dice_img_three, 3),
    (dice_img_four, 4),
    (dice_img_five, 5),
    (dice_img_six, 6),
]


class Dice:
    def __init__(self, id, x, y) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.image = dice_empty
        self.value = 0
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.frozen = False

    def change_position(self, x, y):
        if not self.frozen:
            self.x = x
            self.y = y
            self.rect.x = self.x
            self.rect.y = self.y

    def roll(self):
        if not self.frozen:
            self.value = random.randint(1, 6)
            self.image = dice_img_one
            for pair in dice_images:
                if pair[1] == self.value:
                    self.image = pair[0]

    def freeze(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.frozen = True

    def reset(self):
        self.x = 0
        self.y = 0
        self.rect.x = 0
        self.rect.y = 0
        self.image = dice_empty
        self.value = 0
        self.frozen = False
