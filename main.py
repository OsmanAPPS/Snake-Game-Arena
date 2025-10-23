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
        self.fps_controller = pygame.time.Clock()
        self.game_state = 'PLAYING'
        self.reset()

    def reset(self):
        """Resets the game to its initial state."""
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.base_snake_speed = 15
        self.snake_speed = self.base_snake_speed
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.food_pos = [random.randrange(1, (self.screen_width//10)) * 10, random.randrange(1, (self.screen_height//10)) * 10]
        self.food_spawn = True
        self.score = 0
        self.game_state = 'PLAYING'

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.game_state == 'PLAYING':
                        self.game_state = 'PAUSED'
                    elif self.game_state == 'PAUSED':
                        self.game_state = 'PLAYING'
                if self.game_state == 'PLAYING':
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'
                elif self.game_state == 'GAME_OVER':
                    if event.key == pygame.K_r:
                        self.reset()
                    if event.key == pygame.K_q:
                        self.quit_game()

    def update(self):
        if self.game_state != 'PLAYING':
            return
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
            self.snake_speed = self.base_snake_speed + (self.score // 5)
            self.food_spawn = False
        else:
            self.snake_body.pop()
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.screen_width//10)) * 10, random.randrange(1, (self.screen_height//10)) * 10]
        self.food_spawn = True
        if self.check_game_over():
            self.game_state = 'GAME_OVER'

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
        if self.game_state == 'GAME_OVER':
            self.draw_game_over()
        elif self.game_state == 'PAUSED':
            self.draw_pause_screen()
        pygame.display.update()

    def draw_game_over(self):
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Oyun Bitti!', True, self.red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.screen_width/2, self.screen_height/4)
        self.screen.blit(game_over_surface, game_over_rect)
        score_font = pygame.font.SysFont('times new roman', 30)
        score_surface = score_font.render('Skor: ' + str(self.score), True, self.white)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.screen_width/2, self.screen_height/2)
        self.screen.blit(score_surface, score_rect)
        instr_font = pygame.font.SysFont('times new roman', 20)
        instr_surface = instr_font.render('Tekrar Oyna (R) / Çık (Q)', True, self.white)
        instr_rect = instr_surface.get_rect()
        instr_rect.midtop = (self.screen_width/2, self.screen_height/1.5)
        self.screen.blit(instr_surface, instr_rect)

    def draw_pause_screen(self):
        my_font = pygame.font.SysFont('times new roman', 50)
        pause_surface = my_font.render('Paused', True, self.white)
        pause_rect = pause_surface.get_rect()
        pause_rect.midtop = (self.screen_width/2, self.screen_height/4)
        self.screen.blit(pause_surface, pause_rect)

    def check_game_over(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.screen_width-10:
            return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.screen_height-10:
            return True
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return True
        return False

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.fps_controller.tick(self.snake_speed)

if __name__ == '__main__':
    game = Game()
    game.run()
