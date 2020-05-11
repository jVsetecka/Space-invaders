import pygame
import math
import random


class Player(object):
    def __init__(self, x, y, image, bullet_speed, bullet_img, screen):
        self.player_img = image
        self.x = x
        self.y = y
        self.bullet_x = 0
        self.bullet_y = 0
        self.bullet_speed = bullet_speed
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
    def __init__(self, x, y, bullet_speed, recharge, image, bullet_img, screen):
        self.x = x
        self.y = y
        self.bullet_speed = bullet_speed
        self.bullet_x = x
        self.bullet_y = y
        self.recharge = recharge
        self.image = image
        self.bullet_img = bullet_img
        self.screen = screen
        self.enemy_bullet_state = "ready"
        self.last_shot = 2000

    def update_enemy(self):
        if pygame.time.get_ticks() >= self.last_shot + self.recharge or self.enemy_bullet_state == "fire":
            self.last_shot = pygame.time.get_ticks()
            self.enemy_bullet_state = "fire"
            if self.bullet_y >= 600:
                self.bullet_x = self.x
                self.bullet_y = self.y
                self.enemy_bullet_state = "ready"
            if self.enemy_bullet_state == "fire":
                self.fire_bullet(self.bullet_x, self.bullet_y)
                self.bullet_y += self.bullet_speed

        self.screen.blit(self.image, (self.x, self.y))

    def fire_bullet(self, x, y):
        self.enemy_bullet_state = "fire"
        self.screen.blit(self.bullet_img, (x, y))


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


def update_ui(font_headline, font, screen):
    global alive, level, lives, score

    score_label = font.render(f"Score: {score}", 1, (255, 255, 255))
    hp_label = font.render(f"Lives: {lives}", 1, (255, 255, 255))
    level_label = font.render(f"Level: {level}", 1, (255, 255, 255))
    screen.blit(score_label, (10, 300))
    screen.blit(hp_label, (10, 320))
    screen.blit(level_label, (10, 340))

    game_over(font_headline, font, screen)


def game_over(font_headline, font_ui, screen):
    global score, lives

    if lives < 1:
        game_over_label = font_headline.render("Game Over", 1, (255, 255, 255))
        score_label = font_ui.render(f"Score: {score}", 1, (255, 255, 255))
        try_again_label = font_ui.render("Press space...", 1, (255, 255, 255))
        screen.blit(game_over_label, (250, 210))
        screen.blit(score_label, (250, 250))
        screen.blit(try_again_label, (250, 270))
        end = True

        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset()
                        end = False
            pygame.display.update()


def level_up(enemy_bullet_speed, enemy_img, enemy_bullet_img, screen):
    global level, enemies
    level += 1

    if level < 3:
        number_of_enemies = random.randint(4, 10)
        recharge = random.randint(1500, 2000)
        create_enemies(number_of_enemies, enemy_bullet_speed, recharge, 0, enemy_img, enemy_bullet_img, screen)
    elif level >= 3:
        pass


def create_enemies(number_of_enemies, bullet_speed, recharge, layer, enemy_img, enemy_bullet_img, screen):
    global level, enemies

    x = ((800 - (number_of_enemies * 64)) / number_of_enemies) / 2
    y = layer * 74
    while len(enemies) < number_of_enemies:
        enemies.append(Enemy(x, y, bullet_speed, recharge, enemy_img, enemy_bullet_img, screen))
        x += 64 + (800 - (number_of_enemies * 64)) / number_of_enemies  # Evenly spaced enemies


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


def reset():
    global alive, score, lives, level, player_x, player_y
    alive = True
    score = 0
    lives = 3
    level = 1
    player_x = 370
    player_y = 480
    enemies.clear()


bullet_state = "ready"
alive = True
score = 0
lives = 1
level = 1
player_x = 370
player_y = 480
enemies = []


def main():
    global bullet_state, alive, score, lives, level, player_x, player_y, enemies
    # Load images
    player_img = pygame.image.load("ship.png")
    bullet_img = pygame.image.load("bullet.png")
    enemy_img = pygame.image.load("enemy.png")
    enemy_bullet = pygame.image.load("enemy_bullet.png")
    background_img = pygame.image.load("background.png")
    icon = pygame.image.load("icon.png")

    width = 800
    height = 600
    bullet_speed = 4
    enemy_bullet_speed = 3
    number_of_enemies = 4
    recharge = 2000

    screen = create_window(width, height, icon)
    player = Player(player_x, player_y, player_img, bullet_speed, bullet_img, screen)
    create_enemies(number_of_enemies, enemy_bullet_speed, recharge, 0, enemy_img, enemy_bullet, screen)
    font_ui = pygame.font.SysFont("monospace", 15)
    font_headline = pygame.font.SysFont("monospace", 35)

    while True:
        update_window(screen, background_img)
        player.move()
        if len(enemies) >= 1:
            for enemy in enemies:
                enemy.update_enemy()

                # Collision with enemy
                if is_collision(enemy.x, enemy.y, player.bullet_x, player.bullet_y):
                    bullet_state = "ready"
                    player.bullet_y = 480
                    score += 1
                    enemies.remove(enemy)

                # Collisions with player
                if is_collision(player.x, player.y, enemy.bullet_x, enemy.bullet_y):
                    enemy.enemy_bullet_state = "ready"
                    enemy.bullet_y = enemy.y
                    lives -= 1
        else:
            level_up(enemy_bullet_speed, enemy_img, enemy_bullet, screen)

        update_ui(font_headline, font_ui, screen)
        pygame.display.update()


main()
