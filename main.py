import pygame
import sys
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Yılan Oyunu')
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_speed = 15
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.food_pos = [random.randrange(1, (self.screen_width//10)) * 10, random.randrange(1, (self.screen_height//10)) * 10]
        self.food_spawn = True
        self.score = 0
        self.fps_controller = pygame.time.Clock()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    self.change_to = 'RIGHT'

    def update(self):
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.screen_width//10)) * 10, random.randrange(1, (self.screen_height//10)) * 10]
        self.food_spawn = True

    def draw(self):
        self.screen.fill(self.black)
        for pos in self.snake_body:
            pygame.draw.rect(self.screen, self.green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(self.screen, self.red, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
        my_font = pygame.font.SysFont('times new roman', 20)
        score_surface = my_font.render('Puan : ' + str(self.score), True, self.white)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.screen_width/10, 15)
        self.screen.blit(score_surface, score_rect)
        pygame.display.update()

    def check_game_over(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.screen_width-10:
            self.game_over()
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.screen_height-10:
            self.game_over()
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_over()

    def game_over(self):
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Oyun Bitti!', True, self.red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.screen_width/2, self.screen_height/4)
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.check_game_over()
            self.fps_controller.tick(self.snake_speed)

if __name__ == '__main__':
    game = Game()
    game.run()
