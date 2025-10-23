import pygame
import sys
import random

# Pygame'i başlatma
pygame.init()

# Ekran boyutları
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Yılan Oyunu')

# Renkler
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Yılan
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_speed = 15
direction = 'RIGHT'
change_to = direction

# Yem
food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
food_spawn = True

# Puan
score = 0

# FPS (Frame Per Second) denetleyicisi
fps_controller = pygame.time.Clock()

# Oyun Bitti fonksiyonu
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Oyun Bitti!', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width/2, screen_height/4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Ana oyun döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Yön kontrolü
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Yılanın hareket etmesi
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Yılanın vücudunu büyütme mekanizması
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Yeni yem oluşturma
    if not food_spawn:
        food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
    food_spawn = True

    # Arka planı çizme
    screen.fill(black)

    # Yılanı ve yemi çizme
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Oyun bitti koşulları
    if snake_pos[0] < 0 or snake_pos[0] > screen_width-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > screen_height-10:
        game_over()
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # Puanı gösterme
    my_font = pygame.font.SysFont('times new roman', 20)
    score_surface = my_font.render('Puan : ' + str(score), True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (screen_width/10, 15)
    screen.blit(score_surface, score_rect)

    # Ekranı güncelleme
    pygame.display.update()

    # Frame rate'i ayarlama
    fps_controller.tick(snake_speed)
