import pygame
import time
import random

# Инициализация pygame
pygame.init()

# Определение цветов (RGB)
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

# Размеры окна
window_width = 600
window_height = 400

# Создание окна игры
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Змейка')

# Часы для контроля скорости игры
clock = pygame.time.Clock()

# Размер блока и скорость змейки
block_size = 10
snake_speed = 15

# Шрифт для отображения счета
font_style = pygame.font.SysFont(None, 30)

def show_score(score):
    """Отображение текущего счета"""
    score_text = font_style.render("Счет: " + str(score), True, white)
    game_display.blit(score_text, [10, 10])

def message(msg, color):
    """Отображение сообщения на экране"""
    rendered_message = font_style.render(msg, True, color)
    game_display.blit(rendered_message, [window_width / 6, window_height / 3])

def draw_snake(snake_list, block_size):
    """Отрисовка змейки"""
    for segment in snake_list:
        pygame.draw.rect(game_display, white, [segment[0], segment[1], block_size, block_size])

def game_loop():
    """Основной игровой цикл"""
    game_over = False
    game_close = False

    # Добавляем паузу
    pause_game = False
    
    # Создание препятствий
    obstacles_list = []
    
    # Создание 4-ёх препятствий
    for i in range(4):
        obs_x = round(random.randrange(0, window_width - block_size) / 10.0) * 10.0
        obs_y = round(random.randrange(0, window_height - block_size) / 10.0) * 10.0
        obstacles_list.append([obs_x, obs_y])

    # Начальные координаты змейки
    x1 = window_width / 2
    y1 = window_height / 2

    # Изменение позиции змейки
    x1_change = 0
    y1_change = 0

    # Тело змейки (список координат)
    snake_list = []
    snake_length = 1

    # Координаты еды
    foodx = round(random.randrange(0, window_width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, window_height - block_size) / 10.0) * 10.0

    # Скорость змейки
    current_speed = snake_speed

    while not game_over:

        # Экран окончания игры
        while game_close:
            game_display.fill(black)
            message("Вы проиграли! Нажмите Q для выхода или C для повторной игры", red)
            show_score(snake_length - 1)
            pygame.display.update()

            # Обработка нажатий клавиш на экране окончания игры
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0
                # Пауза при нажатии P
                elif event.key == pygame.K_p:
                    pause_game = not pause_game
        
        if pause_game:
            message("Игра на паузе! Нажми P чтобы продолжить", white)
            pygame.display.update()
            continue

        # Проверка столкновения со стенами
        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_close = True

        # Обновление позиции змейки
        x1 += x1_change
        y1 += y1_change

        # Отрисовка игрового поля
        game_display.fill(black)

        # Отрисовка еды
        pygame.draw.rect(game_display, green, [foodx, foody, block_size, block_size])
        
        # Препятствия
        for obstacle in obstacles_list:
            pygame.draw.rect(game_display, red, [obstacle[0], obstacle[1], block_size, block_size])

        # Добавление текущей позиции змейки в список
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        # Удаление лишних элементов змейки
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка на столкновение с самим собой
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True
        
        # Проверка столкновения с препятствиями
        for obstacle in obstacles_list:
            if x1 == obstacle[0] and y1 == obstacle[1]:
                game_close = True

        # Отрисовка змейки
        draw_snake(snake_list, block_size)

        # Отображение счета
        show_score(snake_length - 1)

        # Обновление экрана
        pygame.display.update()

        # Проверка на поедание еды
        if x1 == foodx and y1 == foody:
            # Создание новой еду
            foodx = round(random.randrange(0, window_width - block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, window_height - block_size) / 10.0) * 10.0
            # Увеличивание длины змейки
            snake_length += 1
            
            # Увеличивание скорости каждые 3 очка
            if snake_length % 3 == 0:
                current_speed += 1
            
            # Новое препятствие каждые 4 очка
            if snake_length % 4 == 0:
                new_obs_x = round(random.randrange(0, window_width - block_size) / 10.0) * 10.0
                new_obs_y = round(random.randrange(0, window_height - block_size) / 10.0) * 10.0
                obstacles_list.append([new_obs_x, new_obs_y])

        # Контроль скорости игры
        clock.tick(current_speed)

    # Завершение pygame
    pygame.quit()
    quit()

game_loop()