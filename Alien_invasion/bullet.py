import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления пулями, выпущенными из корабля."""

    def __init__(self, ai_game):
        """Создает объект пули в текущей позиции корабля."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Создание прямоугольника пули в (0, 0) и установка правильной позиции
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Сохранение позиции пули как числа с плавающей точкой
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает пулю вверх по экрану."""
        # Обновление точной позиции пули
        self.y -= self.settings.bullet_speed
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Отрисовывает пулю на экране."""
        pygame.draw.rect(self.screen, self.color, self.rect)