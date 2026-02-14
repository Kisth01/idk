import pygame.font


class Button:
    """Класс для создания кнопок в игре."""

    def __init__(self, ai_game, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Установка размеров и свойств кнопки
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Создание прямоугольника кнопки и его центрирование
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки подготавливается только один раз
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Преобразует сообщение в отрендеренное изображение и центрирует текст на кнопке."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Рисует пустую кнопку, а затем отображает сообщение."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)