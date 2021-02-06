import pygame
import sys
import random
import time

RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
BROWN = pygame.Color(165, 42, 42)

FPS_CONTROL = pygame.time.Clock()


class Game():
    def __init__(self):

        self.width = 800
        self.height = 600

        self.score = 0

    def init(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Змейка")

    def event_loop(self, change):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord("d"):
                    change = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord("a"):
                    change = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord("w"):
                    change = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord("s"):
                    change = "DOWN"

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change

    # переделать
    def refresh(self):
        pygame.display.flip()
        FPS_CONTROL.tick(20)

    def show_score(self, choice=1):
        s_font = pygame.font.SysFont('comicsansms', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, BLACK)
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (80, 10)
        else:
            s_rect.midtop = (360, 120)
        self.surface.blit(s_surf, s_rect)

    def game_over(self):
        go_font = pygame.font.SysFont('comicsansms', 72)
        go_surf = go_font.render('Game over', True, RED)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()


class Snake():
    def __init__(self, snake_color):
        self.head = [100, 100]
        self.body = [[100, 100], [90, 100], [80, 100]]
        self.snake_color = snake_color

        self.direction = "RIGHT"

        self.change = self.direction

    def validate_change(self):
        if any((self.change == "RIGHT" and not self.direction == "LEFT",
                self.change == "LEFT" and not self.direction == "RIGHT",
                self.change == "UP" and not self.direction == "DOWN",
                self.change == "DOWN" and not self.direction == "UP")):
            self.direction = self.change

    def change_head(self):
        if self.direction == "RIGHT":
            self.head[0] += 10
        elif self.direction == "LEFT":
            self.head[0] -= 10
        elif self.direction == "UP":
            self.head[1] -= 10
        elif self.direction == "DOWN":
            self.head[1] += 10

    def snake_body(self, score, food_pos, width, height):
        self.body.insert(0, list(self.head))

        if self.head[0] == food_pos[0] and self.head[1] == food_pos[1]:
            food_pos = [random.randrange(1, width / 10) * 10,
                        random.randrange(1, height / 10) * 10]
            score += 1
        else:
            self.body.pop()
        return score, food_pos

    def draw(self, surface, color):
        surface.fill(color)
        for pos in self.body:
            pygame.draw.rect(surface, self.snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

    def check_collisions(self, game_over, width, height):
        if any((
                self.head[0] > width - 10
                or self.head[0] < 0,
                self.head[1] > height - 10
                or self.head[1] < 0
        )):
            game_over()
        for block in self.body[1:]:
            if block[0] == self.head[0] and block[1] == self.head[1]:
                game_over()


class Food():
    def __init__(self, food_color, width, height):
        """Инит еды"""
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, width/10)*10,
                         random.randrange(1, height/10)*10]

    def draw_food(self, surface):
        """Отображение еды"""
        pygame.draw.rect(
            surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


game = Game()
snake = Snake(GREEN)
food = Food(BROWN, game.width, game.height)

game.init()

while True:
    snake.change = game.event_loop(snake.change)

    snake.validate_change()
    snake.change_head()
    game.score, food.food_pos = snake.snake_body(
        game.score, food.food_pos, game.width, game.height)
    snake.draw(game.surface, WHITE)

    food.draw_food(game.surface)

    snake.check_collisions(
        game.game_over, game.width, game.height)

    game.show_score()
    game.refresh()
