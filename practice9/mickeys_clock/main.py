from datetime import datetime
import pygame
from clock import MickeyClock

WIDTH, HEIGHT = 600, 600
CENTER = (WIDTH // 2, HEIGHT // 2)

BG_COLOR = (245, 247, 250)
RING_COLOR = (30, 30, 35)
TEXT_COLOR = (20, 20, 20)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 32, bold=True)

    mickey_clock = MickeyClock(CENTER, "images/mickey.png")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # Простой циферблат для ориентира
        pygame.draw.circle(screen, (255, 255, 255), CENTER, 230)
        pygame.draw.circle(screen, RING_COLOR, CENTER, 230, 4)

        mickey_clock.draw(screen)
        pygame.draw.circle(screen, RING_COLOR, CENTER, 8)

        now = datetime.now()
        time_str = f"{now.minute:02d}:{now.second:02d}"
        time_surf = font.render(time_str, True, TEXT_COLOR)
        screen.blit(time_surf, time_surf.get_rect(center=(CENTER[0], 55)))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()