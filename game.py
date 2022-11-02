import pygame
import random
import math
from pygame import mixer

# To initialize pygame
pygame.init()

# To set the pygame window frame
screen = pygame.display.set_mode((800, 600))

# To set the game background
background = pygame.image.load("images\skyground.jpg")

# Adding background music
mixer.music.load('sounds\spacewar.mp3')
mixer.music.play(-1)

# To set the game icon and name
pygame.display.set_caption("Space Raiders 9999")
game_icon = pygame.image.load("images\gali.png")
pygame.display.set_icon(game_icon)

# To add player/character
player_img = pygame.image.load("images\player.png")
player_x = 370
player_y = 530
player_x_change = 0

# To add enemy character
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("images\enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(7, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(30)

# Adding bullets
bullet_img = pygame.image.load("images\sbullet.png")
bullet_x = 0
bullet_y = 530
bullet_x_change = 0
bullet_y_change = 12
bullet_state = "ready"

# Scoring System
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
text_x = 675
text_y = 10

# Game Over Text
end_game = pygame.font.Font('freesansbold.ttf', 100)

def score_text(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))


def end_text():
    game_over_text = end_game.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (100, 240))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


# Implementing quit control
running = True
while running:
    screen.fill((48, 25, 52))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # To gain control of player/character
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -13
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_x_change = 13
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound('sounds\shots.wav')
                bullet_sound.play()
                bullet_x = player_x
            fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0


    # Player Movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Ending the Game
        if enemy_y[i] > 487:
            for j in range(num_of_enemies):
                enemy_y[j] = 1100
                player_x = 2090
                player_y = 2090
                mixer.music.load('sounds\spacewar.mp3')
                mixer.music.stop()
                bullet_sound = mixer.pause()
            end_text()
            font = pygame.font.Font('freesansbold.ttf', 40)
            text_x = 290
            text_y = 200
            break


        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 2.5
            enemy_y[i] += enemy_y_change[i]
            if score_value >= 100:
                enemy_x_change[i] = 3
                enemy_y[i] += enemy_y_change[i]
                if score_value >= 300:
                    enemy_x_change[i] = 4
                    enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -2.5
            enemy_y[i] += enemy_y_change[i]
            if score_value >= 100:
                enemy_x_change[i] = -3
                enemy_y[i] += enemy_y_change[i]
                if score_value >= 300:
                    enemy_x_change[i] = -4
                    enemy_y[i] += enemy_y_change[i]

        # Checking collision to kill enemy
        collide = collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collide:
            contact_sound = mixer.Sound('sounds\kills.wav')
            contact_sound.play()
            bullet_y = 530
            bullet_state = "ready"
            score_value += 5
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(7, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = 530
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    score_text(text_x, text_y)
    pygame.display.update()