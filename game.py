import pygame
import random
import math

from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Background
backgroundImage = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImage = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerx_change = 0

# Enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(5, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)  # change in enemy position on y axis by 40pixel

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480           # same as our player position
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # 16 and 10 values are founded so that bullet firs from the center of the spaceship
    screen.blit(bulletImage, (x + 16, y + 10))


def iscollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt(math.pow((bulletX - enemyX), 2) +
                         (math.pow((bulletY-enemyY), 2)))
    if distance < 27:
        return True
    else:
        return False


running = True

# Game Loop
while running:

    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(backgroundImage, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Get the current x coordinate of the player/spaceship
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of box
    playerX += playerx_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        # when enemy is at this location display game over
        if enemyY[i] > 400 and enemyX[i] == 370:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # Moving all the games out of the screen
            game_over_text()
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]

        collision = iscollision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(5, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        # To keep the bullet continously appearing on the screen
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
