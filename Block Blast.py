import pygame
import random
import sys
import time

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_SIZE = 10
CELL_SIZE = 45
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_OFFSET_Y = 100
SIDEBAR_WIDTH = 200
BLOCK_COLORS = [
    (255, 89, 94),   # Красный
    (255, 202, 58),  # Желтый
    (138, 201, 38),  # Зеленый
    (25, 130, 196),  # Синий
    (106, 76, 147),  # Фиолетовый
    (255, 157, 129), # Оранжевый
    (0, 200, 200),   # Бирюзовый
]

# Настройки окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Blast - Медленный режим")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)
title_font = pygame.font.SysFont(None, 48, bold=True)

class Block:
    def __init__(self, shape=None, color=None):
        if shape is None:
            self.shape = self.generate_random_shape()
        else:
            self.shape = shape
            
        if color is None:
            self.color = random.choice(BLOCK_COLORS)
        else:
            self.color = color
            
        self.x = 0
        self.y = 0
        self.size = len(self.shape)
        
    @staticmethod
    def generate_random_shape():
        shapes = [
            # Одноклеточные
            [[1]],
            
            # Двухклеточные
            [[1, 1]],
            
            # Трехклеточные
            [[1, 1, 1]],
            [[1, 1],
             [1, 0]],
            [[1, 1],
             [0, 1]],
            
            # Четырехклеточные
            [[1, 1, 1, 1]],
            [[1, 1],
             [1, 1]],
            [[1, 1, 1],
             [1, 0, 0]],
            [[1, 1, 1],
             [0, 0, 1]],
            [[1, 1, 0],
             [0, 1, 1]],
            [[1, 1, 1],
             [0, 1, 0]],
            
            # Пятиклеточные
            [[1, 1, 1, 1, 1]],
            [[1, 1, 1],
             [1, 0, 0],
             [1, 0, 0]],
            [[1, 1, 1],
             [0, 1, 0],
             [0, 1, 0]],
            [[0, 1, 0],
             [1, 1, 1],
             [0, 1, 0]],
            [[1, 1],
             [1, 1],
             [1, 0]],
        ]
        return random.choice(shapes)
    
    def rotate(self):
        # Поворачиваем блок на 90 градусов
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows-1-i] = self.shape[i][j]
        
        self.shape = rotated
        self.size = max(len(self.shape), len(self.shape[0]))
    
    def draw(self, x, y, cell_size=CELL_SIZE):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] == 1:
                    rect_x = x + j * cell_size
                    rect_y = y + i * cell_size
                    
                    # Рисуем блок с тенью
                    pygame.draw.rect(screen, self.color, 
                                   (rect_x, rect_y, cell_size-2, cell_size-2))
                    pygame.draw.rect(screen, (255, 255, 255), 
                                   (rect_x, rect_y, cell_size-2, cell_size-2), 1)

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.next_blocks = [Block() for _ in range(3)]
        self.current_block = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.select_next_block()
        self.last_move_time = time.time()
        
        # НАСТРОЙКИ СКОРОСТИ - ИЗМЕНЯЙТЕ ЭТИ ПАРАМЕТРЫ:
        self.base_fall_speed = 0.8  # Базовая скорость падения (было 0.1)
        self.move_delay = 0.2       # Задержка движения (было 0.1)
        self.fall_speed = self.base_fall_speed
        
        # Для авто-падения
        self.last_fall_time = time.time()
        
    def select_next_block(self):
        if self.next_blocks:
            self.current_block = self.next_blocks.pop(0)
            self.current_block.x = GRID_SIZE // 2 - self.current_block.size // 2
            self.current_block.y = 0
            self.next_blocks.append(Block())
            
            # Проверяем, можно ли разместить новый блок
            if not self.can_place_block():
                self.game_over = True
    
    def can_place_block(self, dx=0, dy=0, rotated_shape=None):
        shape = rotated_shape if rotated_shape else self.current_block.shape
        
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    new_x = self.current_block.x + j + dx
                    new_y = self.current_block.y + i + dy
                    
                    # Проверяем границы и пересечения
                    if (new_x < 0 or new_x >= GRID_SIZE or 
                        new_y < 0 or new_y >= GRID_SIZE or 
                        self.grid[new_y][new_x] != 0):
                        return False
        return True
    
    def place_block(self):
        # Размещаем блок на поле
        for i in range(len(self.current_block.shape)):
            for j in range(len(self.current_block.shape[0])):
                if self.current_block.shape[i][j] == 1:
                    grid_y = self.current_block.y + i
                    grid_x = self.current_block.x + j
                    if 0 <= grid_y < GRID_SIZE and 0 <= grid_x < GRID_SIZE:
                        self.grid[grid_y][grid_x] = self.current_block.color
        
        # Проверяем заполненные строки и столбцы
        self.check_lines()
        
        # Выбираем следующий блок
        self.select_next_block()
    
    def check_lines(self):
        lines_to_clear = []
        columns_to_clear = []
        
        # Проверяем строки
        for y in range(GRID_SIZE):
            if all(self.grid[y][x] != 0 for x in range(GRID_SIZE)):
                lines_to_clear.append(y)
        
        # Проверяем столбцы
        for x in range(GRID_SIZE):
            if all(self.grid[y][x] != 0 for y in range(GRID_SIZE)):
                columns_to_clear.append(x)
        
        # Очищаем строки и столбцы
        cleared = len(lines_to_clear) + len(columns_to_clear)
        
        for y in lines_to_clear:
            for x in range(GRID_SIZE):
                self.grid[y][x] = 0
        
        for x in columns_to_clear:
            for y in range(GRID_SIZE):
                self.grid[y][x] = 0
        
        # Начисляем очки
        if cleared > 0:
            points = cleared * 10 * self.level
            self.score += points
            self.lines_cleared += cleared
            
            # Повышаем уровень каждые 10 очищенных линий
            self.level = 1 + self.lines_cleared // 10
            
            # МОЖНО УБРАТЬ УСКОРЕНИЕ С УРОВНЕМ:
            # self.fall_speed = self.base_fall_speed * (0.9 ** (self.level - 1))
            
            return True
        return False
    
    def move_block(self, dx, dy):
        if self.current_block and not self.game_over:
            if self.can_place_block(dx, dy):
                self.current_block.x += dx
                self.current_block.y += dy
                return True
            elif dy > 0:  # Если движение вниз невозможно, размещаем блок
                self.place_block()
        return False
    
    def rotate_block(self):
        if self.current_block and not self.game_over:
            # Сохраняем оригинальную форму
            original_shape = [row[:] for row in self.current_block.shape]
            
            # Поворачиваем
            self.current_block.rotate()
            
            # Если нельзя разместить повернутый блок, возвращаем оригинал
            if not self.can_place_block():
                self.current_block.shape = original_shape
                self.current_block.size = max(len(original_shape), len(original_shape[0]))
    
    def drop_block(self):
        if self.current_block and not self.game_over:
            while self.move_block(0, 1):
                pass
    
    def update(self):
        if not self.game_over and self.current_block:
            current_time = time.time()
            
            # Автоматическое падение
            if current_time - self.last_fall_time > self.fall_speed:
                self.move_block(0, 1)
                self.last_fall_time = current_time
    
    def draw(self):
        # Фон
        screen.fill((30, 30, 40))
        
        # Заголовок
        title = title_font.render("BLOCK BLAST - МЕДЛЕННО", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
        
        # Индикатор скорости
        speed_text = small_font.render(f"Скорость: {self.fall_speed:.1f} сек/клетка", True, (200, 200, 200))
        screen.blit(speed_text, (20, SCREEN_HEIGHT - 40))
        
        # Отрисовка сетки
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect_x = GRID_OFFSET_X + x * CELL_SIZE
                rect_y = GRID_OFFSET_Y + y * CELL_SIZE
                
                # Клетка сетки
                pygame.draw.rect(screen, (50, 50, 60), 
                               (rect_x, rect_y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (70, 70, 80), 
                               (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 1)
                
                # Заполненная клетка
                if self.grid[y][x] != 0:
                    pygame.draw.rect(screen, self.grid[y][x], 
                                   (rect_x + 1, rect_y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
                    pygame.draw.rect(screen, (255, 255, 255), 
                                   (rect_x + 1, rect_y + 1, CELL_SIZE - 2, CELL_SIZE - 2), 1)
        
        # Отрисовка текущего блока
        if self.current_block and not self.game_over:
            for i in range(len(self.current_block.shape)):
                for j in range(len(self.current_block.shape[0])):
                    if self.current_block.shape[i][j] == 1:
                        grid_x = self.current_block.x + j
                        grid_y = self.current_block.y + i
                        
                        if 0 <= grid_y < GRID_SIZE:
                            rect_x = GRID_OFFSET_X + grid_x * CELL_SIZE
                            rect_y = GRID_OFFSET_Y + grid_y * CELL_SIZE
                            
                            # Полупрозрачный блок
                            s = pygame.Surface((CELL_SIZE-2, CELL_SIZE-2), pygame.SRCALPHA)
                            color = list(self.current_block.color) + [180]  # Добавляем альфа-канал
                            s.fill(color)
                            screen.blit(s, (rect_x + 1, rect_y + 1))
                            
                            pygame.draw.rect(screen, (255, 255, 255), 
                                           (rect_x + 1, rect_y + 1, CELL_SIZE - 2, CELL_SIZE - 2), 1)
        
        # Панель статистики
        stats_bg = pygame.Rect(GRID_OFFSET_X + GRID_SIZE * CELL_SIZE + 20, GRID_OFFSET_Y, 
                             SIDEBAR_WIDTH - 40, 200)
        pygame.draw.rect(screen, (40, 40, 50), stats_bg, border_radius=10)
        pygame.draw.rect(screen, (60, 60, 70), stats_bg, 2, border_radius=10)
        
        # Очки
        score_text = font.render(f"Очки: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (stats_bg.x + 20, stats_bg.y + 20))
        
        # Уровень
        level_text = font.render(f"Уровень: {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (stats_bg.x + 20, stats_bg.y + 60))
        
        # Очищенные линии
        lines_text = font.render(f"Линии: {self.lines_cleared}", True, (255, 255, 255))
        screen.blit(lines_text, (stats_bg.x + 20, stats_bg.y + 100))
        
        # Следующие блоки
        next_text = font.render("Следующие:", True, (255, 255, 255))
        screen.blit(next_text, (stats_bg.x + 20, stats_bg.y + 150))
        
        for i, block in enumerate(self.next_blocks):
            block_x = stats_bg.x + 20 + i * 60
            block_y = stats_bg.y + 190
            block.draw(block_x, block_y, 35)
        
        # Управление
        controls_bg = pygame.Rect(GRID_OFFSET_X + GRID_SIZE * CELL_SIZE + 20, 
                                GRID_OFFSET_Y + 320, SIDEBAR_WIDTH - 40, 250)
        pygame.draw.rect(screen, (40, 40, 50), controls_bg, border_radius=10)
        pygame.draw.rect(screen, (60, 60, 70), controls_bg, 2, border_radius=10)
        
        controls = [
            "Управление:",
            "← → - Движение",
            "↑ - Поворот",
            "↓ - Быстрее вниз",
            "Пробел - Сбросить",
            "R - Новая игра",
            "+ - Быстрее",
            "- - Медленнее",
            "ESC - Выход"
        ]
        
        for i, text in enumerate(controls):
            control_text = small_font.render(text, True, (200, 200, 200))
            screen.blit(control_text, (controls_bg.x + 20, controls_bg.y + 20 + i * 30))
        
        # Игра окончена
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            game_over_text = title_font.render("ИГРА ОКОНЧЕНА!", True, (255, 50, 50))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                       SCREEN_HEIGHT // 2 - 50))
            
            final_score = font.render(f"Финальный счет: {self.score}", True, (255, 255, 255))
            screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, 
                                    SCREEN_HEIGHT // 2 + 20))
            
            restart_text = font.render("Нажмите R для новой игры", True, (200, 200, 200))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                     SCREEN_HEIGHT // 2 + 70))

def main():
    game = Game()
    running = True
    move_left = False
    move_right = False
    move_down = False
    
    # Для регулировки скорости
    speed_adjustment = 0.1
    
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif event.key == pygame.K_r:
                    game = Game()  # Новая игра
                
                # РЕГУЛИРОВКА СКОРОСТИ В РЕАЛЬНОМ ВРЕМЕНИ
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # Ускорить (минимальная скорость 0.1 сек)
                    if game.fall_speed > 0.1:
                        game.fall_speed -= speed_adjustment
                        game.move_delay = max(0.05, game.move_delay - 0.05)
                
                elif event.key == pygame.K_MINUS:
                    # Замедлить (максимальная скорость 2.0 сек)
                    if game.fall_speed < 2.0:
                        game.fall_speed += speed_adjustment
                        game.move_delay += 0.05
                
                elif not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.move_block(-1, 0)
                        move_left = True
                    elif event.key == pygame.K_RIGHT:
                        game.move_block(1, 0)
                        move_right = True
                    elif event.key == pygame.K_DOWN:
                        move_down = True
                    elif event.key == pygame.K_UP:
                        game.rotate_block()
                    elif event.key == pygame.K_SPACE:
                        game.drop_block()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False
                elif event.key == pygame.K_DOWN:
                    move_down = False
        
        # Непрерывное движение влево/вправо
        if current_time - game.last_move_time > game.move_delay:
            if move_left:
                game.move_block(-1, 0)
            if move_right:
                game.move_block(1, 0)
            
            # Ускоренное падение при зажатой стрелке вниз
            if move_down and current_time - game.last_fall_time > game.fall_speed / 3:
                game.move_block(0, 1)
                game.last_fall_time = current_time
            
            game.last_move_time = current_time
        
        # Обновление игры (автоматическое падение)
        game.update()
        
        # Отрисовка
        game.draw()
        pygame.display.flip()
        clock.tick(60)  # FPS остается 60 для плавной анимации
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()