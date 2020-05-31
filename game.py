# Import files and Libs
import math
import random

import pygame
from playsound import playsound

bgm = "bgm.mp3"
fire = "laser.wav"
explosion = "explosion.wav"
gameover = "end.wav"

# Initializing
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(bgm)
pygame.mixer.music.play(-1)

# Screen Creation
screen = pygame.display.set_mode((1000, 600))
bg = pygame.image.load("background.png")

# Title and Icon of Game
pygame.display.set_caption("Space War")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player define
playerImg = pygame.image.load("spaceship.png")
playerX = 450
playerY = 480
playerX_change = 0

# Enemy define
enemyImg = pygame.image.load("ufo.png")
enemyX = random.randint(0, 936)
enemyY = 30
enemyX_change = 5
enemyY_change = 0
# Bullet define
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

life_value = 5
life_font = pygame.font.Font("Iceberg.ttf", 24)
lifeX = 920
lifeY = 10
score_value = 0
score_font = pygame.font.Font("Iceberg.ttf", 24)
scoreX = 10
scoreY = 10
over_font = pygame.font.Font("Iceberg.ttf", 64)


def live_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def live_life(x, y):
    life = life_font.render("Life: " + str(life_value), True, (255, 255, 255))
    screen.blit(life, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (350, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 50:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Keypressing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = +4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = pygame.mixer.Sound(fire)
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    life_value -= 1
            if event.key == pygame.K_q:
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    if life_value < 1:
        enemyY = 5000
        enemyY_change += 5
        enemyY += enemyY_change
        scoreX = 5000
        lifeX = 5000
        game_over_text()

    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 5
    elif enemyX >= 936:
        enemyX_change = -5

    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        boomSound = pygame.mixer.Sound(explosion)
        boomSound.play()
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        life_value += 1
        enemyX = random.randint(0, 936)

    enemy(enemyX, enemyY)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if enemyY == 5200:
        playsound(gameover)
        break

    player(playerX, playerY)
    live_score(scoreX, scoreY)
    live_life(lifeX, lifeY)
    pygame.display.update()
