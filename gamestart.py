# Underwater World

import pygame
import random
class Enemy():
    def __init__(self, x, y, speed, size):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.pic = pygame.image.load ("81XoKEm9G-L._AC_SX355_.png")
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)

        #shrink enemy pic
        self.pic = pygame.transform.scale(self.pic, (self.size, self.size))

        if self.speed < 0:
            self.pic = pygame.transform.flip (self.pic, True, False)

    def update (self, screen):
        self.x+=self.speed
        self.hitbox.x += self.speed
        #pygame.draw.rect (screen, (0, 255, 255), self.hitbox)
        screen.blit(self.pic, (self.x, self.y))

# Start the game
pygame.init()
game_width = 1000
game_height = 580
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

# Load all the pictures
background_pic = pygame.image.load("Sea.jpg")
player_pic = pygame.image.load("fish01A.png")

# Player's Variables
player_starting_x=480
player_starting_y = 310
player_starting_size = 50
player_x = player_starting_x
player_y = player_starting_y
player_speed = 3
player_size= player_starting_size
player_facing_left = False
player_hitbox = pygame.Rect(player_x, player_y, player_size, player_size)
player_alive = True

enemy_timer_max = 60
enemy_timer = enemy_timer_max
enemies = []


score = 0
score_font = pygame.font.SysFont("default", 30)
score_text = score_font.render("Score: "+str(score), 1, (0, 0, 0))
play_button_pic = pygame.image.load ("download.png")
play_button_x = game_width/2 - play_button_pic.get_width()/2
play_button_y = game_height/2 - play_button_pic.get_height()/2
#enemy object

# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False


    # Check Key Pressed and Player's Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_facing_left = False
        player_x += 5
    if keys[pygame.K_LEFT]:
        player_x -= 5
        player_facing_left = True
    if keys[pygame.K_UP]:
        player_y -= 5
    if keys[pygame.K_DOWN]:
        player_y += 5
    if keys[pygame.K_SPACE]:
        player_size +=2
    screen.blit(background_pic, (0, 0))

    enemy_timer -= 1
    if enemy_timer <= 0:
        new_enemy_y = random.randint(0, game_height)
        new_enemy_speed = random.randint(2, 5)
        new_enemy_size = random.randint(player_size / 2, player_size * 2)
        if random.randint(0, 1) == 0:
            enemies.append(Enemy(-new_enemy_size * 2, new_enemy_y, new_enemy_speed, new_enemy_size))
        else:
            enemies.append(Enemy(game_width, new_enemy_y, -new_enemy_speed, new_enemy_size))
        enemy_timer = enemy_timer_max

    for enemy in enemies:
        enemy.update(screen)
        

    if player_alive:

        for enemy in enemies:
            if player_hitbox.colliderect(enemy.hitbox):
                if player_size >= enemy.size:
                    score += enemy.size
                    player_size += 2
                    enemies.remove(enemy)
                else:
                    player_alive = False

        player_hitbox.x = player_x
        player_hitbox.y = player_y
        player_hitbox.width = player_size
        player_hitbox.height = player_size
        # pygame.draw.rect(screen, (255, 0, 255), player_hitbox)

        player_pic_small = pygame.transform.scale(player_pic, (player_size, player_size))
        if player_facing_left:
            player_pic_small = pygame.transform.flip(player_pic_small, True, False)
        screen.blit(player_pic_small, (player_x, player_y))
    if player_alive:
        score_text= score_font.render ("Score: "+str(score), 1, (0, 0, 0))
    else:
        score_text = score_font.render("Final Score: " + str(score), 1, (0, 0, 0))
    screen.blit(score_text, (30, 30))
    if not player_alive:
        screen.blit(play_button_pic, (play_button_x, play_button_y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() [0]:
            if mouse_x > play_button_x and mouse_x < play_button_x + play_button_pic.get_width():
                if mouse_y > play_button_y and mouse_y < play_button_y + play_button_pic.get_height():
                    player_alive= True
                    score = 0
                    player_x = player_starting_x
                    player_y = player_starting_y
                    player_size = player_starting_size
                    enemies = []
                    enemies_to_remove = []

    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))





