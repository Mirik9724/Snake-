import os
import pygame
import time
import random

from dotenv import load_dotenv

env_file = '.env'
load_dotenv()

# Настройки
BGCOLOR_START = tuple(map(int, os.getenv('background-min').split(', ')))
BGCOLOR_END = tuple(map(int, os.getenv('background-max').split(', ')))
SNAKE_HEAD_COLOR = (13, 66, 13)  # Зелёный цвет для головы
SNAKE_BODY_COLOR = (204, 204, 0)  # Темно-желтый цвет для тела змеи (меняем оттенок)
FOOD_COLOR = (255, 255, 255)  # Белый цвет для еды
DELAY = float(os.getenv('speed'))
SCREEN_WIDTH = int(os.getenv('screen-w'))
SCREEN_HEIGHT = int(os.getenv('screen-h'))
SNAKE_SIZE = 20
score = 0
sft = os.getenv('sft')
is_welcome_screen_shown = True  # Флаг для экрана приветствия

# Инициализация Pygame
pygame.init()

# Создание окна
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake++")
clock = pygame.time.Clock()

icon = pygame.image.load('img/logo-np.png')
pygame.display.set_icon(icon)

# Змея (начальное положение)
snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
         (SCREEN_WIDTH // 2 - SNAKE_SIZE, SCREEN_HEIGHT // 2),
         (SCREEN_WIDTH // 2 - 2 * SNAKE_SIZE, SCREEN_HEIGHT // 2)]  # Центр экрана
snake_direction = "RIGHT"
is_moving = False  # Змейка не двигается, пока не нажмут клавишу

# Список съеденных яблок
eaten_foods = []

# Функция для генерации еды (с проверкой, что еда не появляется на теле змеи)
def spawn_food():
    while True:
        food_pos = (random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE,
                    random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)
        # Проверка, что еда не находит на теле змеи
        if food_pos not in snake:
            return food_pos

food = spawn_food()  # Инициализируем еду в начале игры


# Функция для обработки съеденной еды
def handle_eaten_food(food):
    global score
    head_x, head_y = snake[0]

    # Проверка на "задевание" еды: если голова змеи находится в пределах одной клетки от еды
    if (head_x <= food[0] + SNAKE_SIZE and head_x + SNAKE_SIZE >= food[0] and
        head_y <= food[1] + SNAKE_SIZE and head_y + SNAKE_SIZE >= food[1]):
        score += 1  # Увеличиваем очки на 1
        food = spawn_food()  # Генерируем новую еду
        snake.append(snake[-1])  # Добавляем новый сегмент змеи
    return food

# Обрабатываем съеденную еду
food = handle_eaten_food(food)

# Функции управления
def change_direction(new_direction):
    global snake_direction
    if new_direction == "UP" and snake_direction != "DOWN":
        snake_direction = "UP"
    elif new_direction == "DOWN" and snake_direction != "UP":
        snake_direction = "DOWN"
    elif new_direction == "LEFT" and snake_direction != "RIGHT":
        snake_direction = "LEFT"
    elif new_direction == "RIGHT" and snake_direction != "LEFT":
        snake_direction = "RIGHT"

def move_snake():
    head_x, head_y = snake[0]
    new_head = None  # Инициализация переменной new_head

    if snake_direction == "UP":
        new_head = (head_x, head_y - SNAKE_SIZE)
    elif snake_direction == "DOWN":
        new_head = (head_x, head_y + SNAKE_SIZE)
    elif snake_direction == "LEFT":
        new_head = (head_x - SNAKE_SIZE, head_y)
    elif snake_direction == "RIGHT":
        new_head = (head_x + SNAKE_SIZE, head_y)

    if new_head:  # Проверка, что new_head был присвоен
        return [new_head] + snake[:-1]
    return snake  # Если направление не установлено, возвращаем старое положение змеи

def draw_snake():
    for i, segment in enumerate(snake):
        if i == 0:  # Голова змеи
            pygame.draw.rect(window, SNAKE_HEAD_COLOR, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        else:  # Тело змеи
            pygame.draw.rect(window, SNAKE_BODY_COLOR, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

def draw_food():
    apple_texture = pygame.image.load('img/apple.png')  # Путь к текстуре яблока
    food_pos = food  # Это координаты еды (x, y)

    # Отрисовка текстуры яблока
    window.blit(pygame.transform.scale(apple_texture, (SNAKE_SIZE, SNAKE_SIZE)), (food_pos[0], food_pos[1]))



def check_collision_with_boundaries():
    head_x, head_y = snake[0]
    if head_x >= SCREEN_WIDTH or head_x < 0 or head_y >= SCREEN_HEIGHT or head_y < 0:
        return True
    return False

def check_collision_with_self():
    head_x, head_y = snake[0]
    for segment in snake[1:]:
        if segment[0] == head_x and segment[1] == head_y:
            return True
    return False

# Функция для отрисовки градиентного фона
def draw_gradient_background():
    for y in range(SCREEN_HEIGHT):
        color = (
            int(BGCOLOR_START[0] + (BGCOLOR_END[0] - BGCOLOR_START[0]) * y / SCREEN_HEIGHT),
            int(BGCOLOR_START[1] + (BGCOLOR_END[1] - BGCOLOR_START[1]) * y / SCREEN_HEIGHT),
            int(BGCOLOR_START[2] + (BGCOLOR_END[2] - BGCOLOR_START[2]) * y / SCREEN_HEIGHT)
        )
        pygame.draw.line(window, color, (0, y), (SCREEN_WIDTH, y))

# Функция для отображения счета
def draw_score():
    font = pygame.font.Font(sft, 30)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))  # Отображаем счет в верхнем левом углу

# Функция для отображения экрана приветствия
def show_welcome_screen():
    font = pygame.font.Font(sft, 50)
    title_text = font.render("Welcome to Snake++", True, (255, 255, 255))
    start_text = font.render("Press any key to start", True, (255, 255, 255))

    # Получение размеров текста для центровки
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    window.fill((0, 0, 0))  # Очистить экран
    window.blit(title_text, title_rect)  # Отображение заголовка по центру
    window.blit(start_text, start_rect)  # Отображение подсказки по центру


    pygame.display.update()  # Обновление экрана

# Основной игровой цикл
running = True
while running:
    window.fill((0, 0, 0))  # Очистка экрана перед отрисовкой

    if is_welcome_screen_shown is True:
        show_welcome_screen()  # Показываем экран приветствия
    else:
        draw_gradient_background()
        draw_food()
        draw_snake()
        draw_score()

    # draw_snake()  # Рисуем змею
    # draw_food()  # Рисуем еду
    # draw_score()  # Рисуем счет
    # draw_gradient_background()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if is_welcome_screen_shown:  # Если экран приветствия показан, скрываем его
                is_welcome_screen_shown = False  # Начинаем игру
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                change_direction("UP")
                is_moving = True  # Змейка начинает двигаться после первого ввода
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                change_direction("DOWN")
                is_moving = True
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                change_direction("LEFT")
                is_moving = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                change_direction("RIGHT")
                is_moving = True

    # Двигаем змею только если она начала движение
    if is_moving:
        snake = move_snake()

        # Проверка на столкновение с границами
        if check_collision_with_boundaries() or check_collision_with_self():
            snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                     (SCREEN_WIDTH // 2 - SNAKE_SIZE, SCREEN_HEIGHT // 2),
                     (SCREEN_WIDTH // 2 - 2 * SNAKE_SIZE, SCREEN_HEIGHT // 2)]  # Сбрасываем змею в исходное положение
            snake_direction = "RIGHT"
            is_moving = False  # Змейка не двигается после сброса

        # Проверка на поедание еды
        head_x, head_y = snake[0]
        if (head_x, head_y) == food:
            eaten_foods.append(food)  # Добавляем съеденную еду в список
            food = spawn_food()  # Генерируем новую еду
            snake.append(snake[-1])  # Добавляем новый сегмент змеи
            score += 1 # Увеличиваем очки

        # Отображение еды и змеи
        draw_gradient_background()
        draw_food()
        draw_snake()
        draw_score()








    # Обновление экрана
    pygame.display.update()

    # Задержка и управление FPS
    time.sleep(DELAY)
    clock.tick(10)

pygame.quit()
