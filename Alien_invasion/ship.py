import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Класс для управления кораблем."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загружает изображение корабля и получает его прямоугольник
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется внизу по центру экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохраняет точную горизонтальную позицию корабля как число с плавающей точкой
        self.x = float(self.rect.x)

        # Флаги движения; начинаем с неподвижного корабля
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """Центрирует корабль на экране."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Обновляет позицию корабля на основе флагов движения."""
        # Обновляет значение x корабля, а не прямоугольника
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        # Обновляет объект прямоугольника из self.x
        self.rect.x = self.x

    def blitme(self):
        """Рисует корабль в его текущей позиции."""
        self.screen.blit(self.image, self.rect)