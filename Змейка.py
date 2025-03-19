import pygame  
import random 

pygame.init() 

#Экран:
WIDTH, HEIGHT = 300, 300 
CELL_SIZE = 30 
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE 

#Цвет:
BACKGROUND_COLOR = (240, 248, 255)   
GRID_COLOR = (220, 220, 220)   
SNAKE_COLOR = (144, 238, 144)   
FOOD_COLOR = (255, 182, 193)   

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Snake Game") 


#Создаем змейку (в центре), начальное направление (вверх) и еду:

snake = [(5, 5)]  # List of (x, y) positions 
direction = (0, -1)  # Initial direction: up 
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) 

clock = pygame.time.Clock() 
speed = 5  # скорость змейки 

#Отрисовка поля:

def draw_grid(): 
    for x in range(0, WIDTH, CELL_SIZE): 
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT)) 
    for y in range(0, HEIGHT, CELL_SIZE): 
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y)) 

#Логика движения змейки:

def move_snake(): 
    global food 
    head = snake[0] 
    new_head = ((head[0] + direction[0]) % GRID_WIDTH, (head[1] + direction[1]) % GRID_HEIGHT) 
     
    # Проверяем столкновение головы змейки с хвостом 
    if new_head in snake: 
        return False 

    snake.insert(0, new_head) 

    # Проверяем, съела ли она еду 
    if new_head == food: 
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) 
    else: 
        snake.pop() 

    return True 

#Основной цикл:

running = True 
while running: 
    screen.fill(BACKGROUND_COLOR) 
    draw_grid() 

    # Проверяем нажатия кнопок 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_UP and direction != (0, 1): 
                direction = (0, -1) 
            elif event.key == pygame.K_DOWN and direction != (0, -1): 
                direction = (0, 1) 
            elif event.key == pygame.K_LEFT and direction != (1, 0): 
                direction = (-1, 0) 
            elif event.key == pygame.K_RIGHT and direction != (-1, 0): 
                direction = (1, 0) 

    # Двигаем змейку и если move_snake вернул false, то выводим Game Over 
    if not move_snake(): 
        print("Game Over!") 
        running = False 

    # Отрисовка змейки 
    for segment in snake: 
        x, y = segment 
        pygame.draw.rect(screen, SNAKE_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) 

    # Отрисовка еды 
    fx, fy = food 
    pygame.draw.rect(screen, FOOD_COLOR, (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)) 

    # Обновляем экран 
    pygame.display.flip() 
    clock.tick(speed) 

pygame.quit()