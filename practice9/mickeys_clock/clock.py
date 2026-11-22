from datetime import datetime
from pathlib import Path
import pygame


class MickeyClock:
    def __init__(self, center, image_path):
        self.center = center
        base_dir = Path(__file__).resolve().parent
        full_path = base_dir / image_path
        self.raw_image = pygame.image.load(str(full_path)).convert_alpha()

        # Правая рука — минутная стрелка, левая — секундная
        self.minute_sprite = pygame.transform.smoothscale(self.raw_image, (150, 150))
        self.second_sprite = pygame.transform.smoothscale(self.raw_image, (120, 120))

    @staticmethod
    def get_time_values():
        now = datetime.now()
        return now.minute, now.second

    @staticmethod
    def _rotate_hand(sprite, angle_deg, center):
        # В Pygame положительный угол крутит против часовой, поэтому ставим минус
        rotated = pygame.transform.rotate(sprite, -angle_deg)
        rect = rotated.get_rect(center=center)
        return rotated, rect

    def draw(self, surface):
        minutes, seconds = self.get_time_values()

        # 6 градусов на каждую секунду и на каждую минуту
        second_angle = seconds * 6
        minute_angle = (minutes + seconds / 60) * 6

        min_surf, min_rect = self._rotate_hand(self.minute_sprite, minute_angle, self.center)
        sec_surf, sec_rect = self._rotate_hand(self.second_sprite, second_angle, self.center)

        surface.blit(min_surf, min_rect)
        surface.blit(sec_surf, sec_rect)