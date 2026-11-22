import pygame
from ball import MovingBall

WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)
BALL_RADIUS = 25
STEP_SIZE = 20
HUD_COLOR = (90, 95, 105)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    ball = MovingBall(
        x=WIDTH // 2,
        y=HEIGHT // 2,
        radius=BALL_RADIUS,
        step=STEP_SIZE,
        screen_width=WIDTH,
        screen_height=HEIGHT,
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                ball.handle_key(event.key)

        screen.fill(BG_COLOR)
        ball.draw(screen)

        hint = font.render(
            f"Use Arrow Keys to move  |  Pos: ({ball.x}, {ball.y})",
            True,
            HUD_COLOR,
        )
        screen.blit(hint, (16, 14))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()