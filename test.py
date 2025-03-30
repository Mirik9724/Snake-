import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Размеры блоков
SNAKE_SIZE = 20
FOOD_SIZE = 20

# Игровая переменная
snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
snake_direction = "RIGHT"
food = (random.randrange(0, SCREEN_WIDTH - FOOD_SIZE, FOOD_SIZE), random.randrange(0, SCREEN_HEIGHT - FOOD_SIZE, FOOD_SIZE))
score = 0

# Основной игровой цикл
running = True
is_welcome_screen_shown = True  # Флаг для экрана приветствия
clock = pygame.time.Clock()

# Функция для отрисовки змеи
def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

# Функция для отрисовки еды
def draw_food():
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], FOOD_SIZE, FOOD_SIZE))

# Функция для отрисовки счета
def draw_score():
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])

# Функция для отображения экрана приветствия
def show_welcome_screen():
    font = pygame.font.SysFont(None, 55)
    welcome_text = font.render("Welcome to Snake Game! Press any key to start.", True, WHITE)
    screen.blit(welcome_text, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2])

# Основной игровой цикл
while running:
    screen.fill(BLACK)  # Очистка экрана

    if is_welcome_screen_shown:
        show_welcome_screen()  # Показываем экран приветствия
    else:
        draw_snake()  # Рисуем змею
        draw_food()  # Рисуем еду
        draw_score()  # Рисуем счет

    pygame.display.update()  # Обновляем экран

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if is_welcome_screen_shown:  # Если экран приветствия показан, скрываем его
                is_welcome_screen_shown = False  # Начинаем игру
            else:
                # Обработка движения змеи
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    snake_direction = "UP"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    snake_direction = "DOWN"
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    snake_direction = "LEFT"
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    snake_direction = "RIGHT"

    # Логика движения змеи
    if not is_welcome_screen_shown:
        head_x, head_y = snake[0]
        if snake_direction == "UP":
            head_y -= SNAKE_SIZE
        elif snake_direction == "DOWN":
            head_y += SNAKE_SIZE
        elif snake_direction == "LEFT":
            head_x -= SNAKE_SIZE
        elif snake_direction == "RIGHT":
            head_x += SNAKE_SIZE

        snake = [(head_x, head_y)] + snake[:-1]  # Обновляем положение змеи

        # Проверка на столкновение с границами экрана
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            running = False  # Если столкновение с границей — конец игры

        # Проверка на поедание еды
        if (head_x, head_y) == food:
            food = (random.randrange(0, SCREEN_WIDTH - FOOD_SIZE, FOOD_SIZE), random.randrange(0, SCREEN_HEIGHT - FOOD_SIZE, FOOD_SIZE))
            snake.append(snake[-1])  # Добавляем сегмент к змее
            score += 1  # Увеличиваем счет

    # Задержка и управление FPS
    clock.tick(10)

pygame.quit()
