import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox


class Player(object):
    def __init__(self, x, y, image, screen):
        self.player_img = image
        self.x = x
        self.y = y
        self.pos_change = 0
        self.screen = screen

    def update_player(self):
        self.screen.blit(self.player_img, (self.x, self.y))

    def move(self):
        self.update_player()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.pos_change = -4
                elif event.key == pygame.K_RIGHT:
                    self.pos_change = 4
            elif event.type == pygame.KEYUP:  # Stop moving on key up
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.pos_change = 0

        self.x += self.pos_change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

    def shoot(self):
        pass


class Enemy(object):
    def __init__(self, x, y, image, screen):
        self.x = x
        self.y = y


    def move(self):
        pass

    def shoot(self):
        pass


# Prepares window
def create_window(width, height, icon):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Space invaders")
    pygame.display.set_icon(icon)
    screen.blit(pygame.image.load("background.png"), (0, 0))
    return screen


def update_window(screen, background):
    screen.blit(background, (0, 0))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    pass


def game_over():
    pass


def message_box(subject, content):
    pass


def main():
    # Load images
    player_img = pygame.image.load("ship.png")
    background_img = pygame.image.load("background.png")
    icon = pygame.image.load("icon.png")
    width = 800
    height = 600
    player_x = 370
    player_y = 480

    screen = create_window(width, height, icon)
    player = Player(player_x, player_y, player_img, screen)

    running = True
    while running:
        update_window(screen, background_img)
        player.move()
        pygame.display.update()


main()
