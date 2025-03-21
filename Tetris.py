import pygame
import random

# Инициализация pygame
pygame.init()

# Настройки игры
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GAME_OVER_FONT = pygame.font.SysFont("arial", 48)

# Цвета
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
PASTEL_GREEN = (119, 221, 119)
PASTEL_RED = (255, 179, 186)
PASTEL_CYAN = (173, 216, 230)
PASTEL_MAGENTA = (244, 154, 194)
PASTEL_YELLOW = (255, 255, 204)
PASTEL_BLUE = (173, 216, 230)
PASTEL_ORANGE = (255, 223, 186)

# Все возможные тетромино (формы блоков)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 0], [1, 1, 1]],  # T
]

SHAPE_COLORS = [PASTEL_CYAN, PASTEL_YELLOW, PASTEL_GREEN, PASTEL_RED, PASTEL_BLUE, PASTEL_ORANGE, PASTEL_MAGENTA]

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Основные переменные
clock = pygame.time.Clock()
grid = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
game_over = False
current_shape = None
current_color = None
current_pos = None
fall_time = 0
fall_speed = 500  # Время в миллисекундах между падениями

# Функция для рисования сетки
def draw_grid():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != 0:  # Если ячейка не пустая, рисуем блок
                draw_block(col, row, SHAPE_COLORS[grid[row][col] - 1])
            pygame.draw.rect(screen, WHITE, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Функция для рисования блока
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Функция для генерации новой фигуры
def new_shape():
    shape = random.choice(SHAPES)
    color = random.choice(SHAPE_COLORS)
    return shape, color, [SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2, 0]

# Проверка на столкновение с уже установленными блоками
def check_collision(shape, pos):
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val:
                x = pos[0] + c
                y = pos[1] + r
                if x < 0 or x >= SCREEN_WIDTH // BLOCK_SIZE or y >= SCREEN_HEIGHT // BLOCK_SIZE or grid[y][x]:
                    return True
    return False

# Остановка фигуры на поле
def lock_shape(shape, color, pos):
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val:
                grid[pos[1] + r][pos[0] + c] = SHAPE_COLORS.index(color) + 1

# Удаление полных строк
def clear_lines():
    global grid
    lines_cleared = 0
    new_grid = []
    for row in grid:
        if all(row):
            lines_cleared += 1
        else:
            new_grid.append(row)
    grid = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(lines_cleared)] + new_grid

# Проверка на окончание игры
def check_game_over():
    return any(grid[0])

# Функция вращения фигуры с проверкой

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

def try_rotate(shape, pos):
    rotated_shape = rotate_shape(shape)
    if not check_collision(rotated_shape, pos):
        return rotated_shape
    return shape

# Основной игровой цикл
def game_loop():
    global current_shape, current_color, current_pos, game_over, fall_time

    current_shape, current_color, current_pos = new_shape()

    while not game_over:
        screen.fill(BLACK)
        draw_grid()

        # 🔥 **Обработка событий должна быть в этом цикле!**
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(current_shape, [current_pos[0] - 1, current_pos[1]]):
                        current_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(current_shape, [current_pos[0] + 1, current_pos[1]]):
                        current_pos[0] += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(current_shape, [current_pos[0], current_pos[1] + 1]):
                        current_pos[1] += 1
                elif event.key == pygame.K_UP:
                    current_shape = try_rotate(current_shape, current_pos)

        # 🔥 **Обновление падения фигурки**
        fall_time += clock.get_time()
        clock.tick(60)  

        if fall_time >= fall_speed:
            fall_time = 0
            if not check_collision(current_shape, [current_pos[0], current_pos[1] + 1]):
                current_pos[1] += 1
            else:
                lock_shape(current_shape, current_color, current_pos)
                clear_lines()
                if check_game_over():
                    game_over = True
                else:
                    current_shape, current_color, current_pos = new_shape()

        # 🔥 **Рисуем текущую фигуру**
        for r, row in enumerate(current_shape):
            for c, val in enumerate(row):
                if val:
                    draw_block(current_pos[0] + c, current_pos[1] + r, current_color)

        pygame.display.flip()  # Обновляем экран

    # Когда игра заканчивается:
    screen.fill(BLACK)
    game_over_text = GAME_OVER_FONT.render("GAME OVER", True, PASTEL_RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

        
        
                    

def clear_lines():
    global grid
    lines_cleared = 0
    new_grid = []
    for row in grid:
        if all(row):  # Если строка заполнена
            lines_cleared += 1
        else:
            new_grid.append(row)
    grid = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(lines_cleared)] + new_grid

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

def try_rotate(shape, pos):
    rotated_shape = rotate_shape(shape)
    if not check_collision(rotated_shape, pos):
        return rotated_shape
    return shape


def check_game_over():
    return any(grid[0])

if __name__ == "__main__":
    game_loop()
    pygame.quit()