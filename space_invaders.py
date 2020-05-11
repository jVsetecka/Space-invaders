import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox


class Player(object):
    def __init__(self, x, y, image, bullet_img, screen):
        self.player_img = image
        self.x = x
        self.y = y
        self.bullet_x = 0
        self.bullet_y = 0
        self.bullet_speed = 4
        self.pos_change = 0
        self.bullet_img = bullet_img
        self.screen = screen

    def update_player(self):
        global bullet_state
        if self.bullet_y <= 0:
            self.bullet_y = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            self.fire_bullet(self.bullet_x, self.bullet_y)
            self.bullet_y -= self.bullet_speed
        self.screen.blit(self.player_img, (self.x, self.y))

    def move(self):
        global bullet_state
        self.update_player()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.pos_change = -4
                elif event.key == pygame.K_RIGHT:
                    self.pos_change = 4
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        self.fire_bullet(self.x, self.y)
                        self.bullet_x = self.x
            elif event.type == pygame.KEYUP:  # Stop moving on key up
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.pos_change = 0

        self.x += self.pos_change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

    def fire_bullet(self, x, y):
        global bullet_state
        bullet_state = "fire"
        self.screen.blit(self.bullet_img, (x + 16, y + 10))


class Enemy(object):
    def __init__(self, x, y, bullet_speed, image, bullet_img, screen):
        self.x = x
        self.y = y
        self.bullet_speed = bullet_speed
        self.image = image
        self.bullet_img = bullet_img
        self.screen = screen

    def update_enemy(self):
        self.screen.blit(self.image, (self.x, self.y))

    def shoot(self, x, y):
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


def create_enemies(number_of_enemies, layer, enemy_img, enemy_bullet_img, screen):
    enemies = []

    x = ((800 - (number_of_enemies * 64)) / number_of_enemies) / 2
    y = layer * 74
    while len(enemies) < number_of_enemies:
        enemies.append(Enemy(x, y, 3, enemy_img, enemy_bullet_img, screen))
        x += 64 + (800 - (number_of_enemies * 64)) / number_of_enemies  # Evenly spaced enemies

    return enemies


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    pass


def game_over():
    pass


def message_box(subject, content):
    pass


bullet_state = "ready"


def main():
    # Load images
    player_img = pygame.image.load("ship.png")
    bullet_img = pygame.image.load("bullet.png")
    enemy_img = pygame.image.load("enemy.png")
    background_img = pygame.image.load("background.png")
    icon = pygame.image.load("icon.png")

    width = 800
    height = 600
    player_x = 370
    player_y = 480
    number_of_enemies = 15

    screen = create_window(width, height, icon)
    player = Player(player_x, player_y, player_img, bullet_img, screen)
    enemies = create_enemies(number_of_enemies, 0, enemy_img, bullet_img, screen)

    running = True
    while running:
        update_window(screen, background_img)
        player.move()
        for enemy in enemies:
            enemy.update_enemy()
        pygame.display.update()


main()
