import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
FPS = 10

BACKGROUND_COLOR = (254, 115, 119)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MENU = 0
GAME = 1
INSTRUCTIONS = 2
OPTIONS = 3

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.directions = [(0, 0)]
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.directions[0] if self.directions else (0, 0)
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def set_direction(self, direction):
        if direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            self.directions.insert(0, direction)

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.directions = [(0, 0)]

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = BLUE
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

class MainMenu:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.title = self.font_large.render("Snake Game", True, WHITE)
        self.play_text = self.font_medium.render("Play", True, WHITE)
        self.instructions_text = self.font_medium.render("Use arrow keys to control the snake", True, WHITE)
        self.options_text = self.font_medium.render("Avoid collisions with the snake's body", True, WHITE)

        self.play_rect = self.play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.instructions_rect = self.instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.options_rect = self.options_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    def render(self, surface):
        surface.fill(BACKGROUND_COLOR)
        surface.blit(self.title, (WIDTH // 2 - self.title.get_width() // 2, HEIGHT // 4))
        pygame.draw.rect(surface, WHITE, self.play_rect, 2)
        surface.blit(self.play_text, self.play_rect.topleft)
        surface.blit(self.instructions_text, self.instructions_rect.topleft)
        surface.blit(self.options_text, self.options_rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.play_rect.collidepoint(mouse_pos):
                return "Play"
        return None

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
snake = Snake()
food = Food()
menu = MainMenu()

game_state = MENU

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_RETURN:
                    game_state = GAME
            elif game_state == GAME:
                if event.key == pygame.K_UP:
                    snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction((1, 0))
                elif event.key == pygame.K_ESCAPE:
                    game_state = MENU
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == MENU:
                button_clicked = menu.handle_event(event)
                if button_clicked == "Play":
                    game_state = GAME

    if game_state == MENU:
        menu.render(screen)
    elif game_state == GAME:
        snake.update()

        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()

        screen.fill(WHITE)
        snake.render(screen)
        food.render(screen)

    pygame.display.update()
    clock.tick(FPS)
