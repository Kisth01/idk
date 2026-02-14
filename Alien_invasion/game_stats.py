class GameStats:
    """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Рекордный счет никогда не сбрасывается
        self.high_score = 0

    def reset_stats(self):
        """Инициализирует статистику, которая может меняться во время игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1